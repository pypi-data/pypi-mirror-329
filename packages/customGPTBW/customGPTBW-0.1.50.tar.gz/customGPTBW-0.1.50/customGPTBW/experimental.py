from tqdm import tqdm
import tensorflow as tf
import threading
import multiprocessing as mp
from functools import partial
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import time

class Timer():
    def __init__(self) -> None:
        self.starting_time = None

    def timer(self,func,*args,**kwargs):
        starting_time = time.time()
        result = func(*args,**kwargs)
        print(f"Time taken to execute {func.__name__} is {time.time() - starting_time:.4f}s")

    def start(self):
        self.starting_time = time.time()

    def end(self):
        print(f"Time taken to execute is {time.time() - self.starting_time:.4f}s")

def tokenize_batch(batch, tokenizer, max_length):
    return tokenizer(batch, padding='max_length', truncation=True, return_tensors='tf', max_length=max_length)

def split_into_chunks(lst, n_chunks):
    n = len(lst)
    n_chunks = min(n, n_chunks)
    k, m = divmod(n, n_chunks)
    return [lst[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n_chunks)]

def tokenize(ds_obj, mod_obj, max_length=512, batch_size=8, num_cores=96):
    if ds_obj.gpt_sentence is None:
        raise ValueError("Please run dataset_loadqa() and datasetgpt() first before processing.")

    sentences = ds_obj.gpt_sentence

    # Split into parallel batches
    batches = split_into_chunks(sentences, num_cores)

    # Prepare a partial function that already has the tokenizer and max_length parameters set.
    tokenize_func = partial(tokenize_batch, tokenizer=mod_obj.tokenizer, max_length=max_length)

    # Process batches in parallel
    with mp.Pool(num_cores) as pool:
        batch_results = pool.map(tokenize_func, batches)

    # Aggregate results
    all_inputs, all_masks = [], []
    for result in batch_results:
        all_inputs.extend(result['input_ids'])
        all_masks.extend(result['attention_mask'])

    input = {"input_ids":tf.convert_to_tensor(all_inputs),"attention_mask":tf.convert_to_tensor(all_masks)}
    dataset = ds_obj.create_tf_dataset(input)
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    ds_obj.tf_dataset = dataset
    
def multi_run(tasks:list):
    threads = []
    for func in tasks:
        t = threading.Thread(target=func)
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
