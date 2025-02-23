from tqdm import tqdm
import tensorflow as tf
import shutil

class Dataset():
    def __init__(self,ds_name=None):
        self.questions = None
        self.answers = None
        self.gpt_sentence = None
        self.tf_dataset = None
        self.type = 0
        if ds_name == None:
            self.dt_save_path = "encoded_dataset"
        else:
            self.dt_save_path = ds_name


    def dataset_load(self,file_name,first_n=None,start_from=0,name="WICKED4950/MentalHeathEsther",local=True):
      if local:
          import json
          with open(f"{file_name}.json") as f:
              data = json.load(f)
          if first_n == None:
              first_n = len(list(data.keys()))
          self.questions = list(data.keys())[start_from:first_n]
          self.answers = list(data.values())[start_from:first_n]
      else:
          try:
              from datasets import load_dataset
          except:
              raise RuntimeError("You didn't run the pip install at the start of the program")
          dataset = load_dataset(name, data_files=file_name)
          train_data_dict = dataset['train'].to_dict()
          if first_n == None:
              first_n = len(train_data_dict["question"])
          self.questions = train_data_dict["question"][start_from:first_n]
          self.answers = train_data_dict["answer"][start_from:first_n]
          self.type = 1

    def datasetprocess(self,user_start="<|SOH|>",bot_start="<|SOB|>",answer_only=False):
        if answer_only:
            if self.questions == None:
                raise ValueError("Please do the dataset_loadqa() to get the dataset running and then process it")
            if user_start == "<|SOH|>" and bot_start=="<|SOB|>":
                self.gpt_sentence = self.answers
            else:
                correct_lab_list = []
                for sentence in self.answer:
                    sentence = sentence.replace("<|SOH|>", user_start)
                    sentence = sentence.replace("<|SOB|>", bot_start)
                self.gpt_sentence = correct_lab_list
        else:
            if self.questions == None:
                raise ValueError("Please do the dataset_loadqa() to get the dataset running and then process it")

            sentence = [f"{user_start}{question}{bot_start}{answer}{user_start}" for question,answer in zip(self.questions,self.answers)]
            self.gpt_sentence = sentence
        self.type = 2

    def mask_qa(self,tokenizer ,conversations ,len_=1024,batch_size=8):
        all_input_ids = []
        all_attention_masks = []
        all_labels = []
        tokenized_output = tokenizer(
                conversations,
                return_tensors='tf',
                padding='max_length',  # Pad to the maximum length
                truncation=True,       # Truncate if longer than max_length
                max_length=len_  # Set the maximum sequence length
            )
        
        soh = tokenizer.encode("<|SOH|>", add_special_tokens=False)[0]
        sob = tokenizer.encode("<|SOB|>", add_special_tokens=False)[0]
        for index in tqdm(range(tokenized_output["input_ids"].shape[0]), desc="Processing conversations", unit="conversation"):

            input_ids = tokenized_output["input_ids"][index]
            attention_mask = tokenized_output["attention_mask"][index]
            # Create the labels
            labels = input_ids.numpy().copy()  # Make sure it's a NumPy array for easier manipulation


            labels[0] = -100  # Start by masking the first token
            inp_cpy = input_ids.numpy()
            last = len(input_ids.numpy()) - 2
            for idx, token in enumerate(input_ids.numpy()):
                if attention_mask[idx] == 0:
                    break
                if token == soh:  # If it's a question start token, mask the subsequent tokens
                    try:
                        while inp_cpy[idx] != sob:
                            labels[idx + 1] = -100
                            idx += 1
                            if idx == last:
                                break
                    except:
                        pass


            # Append input_ids, attention_mask, and labels to their respective lists
            all_input_ids.append(input_ids)
            all_attention_masks.append(attention_mask)
            all_labels.append(labels)

        dataset = self.create_tf_dataset(tf.concat(tf.convert_to_tensor(all_input_ids), axis=0),tf.concat(tf.convert_to_tensor(all_attention_masks), axis=0),tf.concat(tf.convert_to_tensor(all_labels), axis=0))
        dataset = dataset.shuffle(buffer_size=75000)  # Shuffle with buffer size of 1000
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
        self.tf_dataset = dataset
        self.type = 3

    def create_tf_dataset(self,inputs,attention_mask=None,labels=None):
        if labels == None:
            if attention_mask == None:
                input_ids = inputs['input_ids']
            else:
                input_ids = inputs
            if attention_mask == None:
                attention_mask = inputs['attention_mask']
            return tf.data.Dataset.from_tensor_slices(({
                'input_ids': input_ids,
                'attention_mask': attention_mask
            }, input_ids))
        else:
            return tf.data.Dataset.from_tensor_slices(({
                'input_ids': inputs,
                'attention_mask': attention_mask
            }, labels))

    def tokenize(self, tokenizer, max_length=256, batch_size=8):
        if self.gpt_sentence is None:
            raise ValueError("Please run dataset_loadqa() and datasetgpt() first before processing.")

        # Tokenize the GPT sentences
        inputs = tokenizer(self.gpt_sentence, padding=True, truncation=True, return_tensors='tf', max_length=max_length)


        # Create the dataset and apply shuffle and batching
        dataset = self.create_tf_dataset(inputs)
        dataset = dataset.shuffle(buffer_size=75000)  # Shuffle with buffer size of 1000
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
        self.tf_dataset = dataset
        self.type = 3

    def clear_save(self):
        try:
            shutil.rmtree(self.dt_save_path)
            self.tf_dataset = None
        except FileNotFoundError:
            print("Brother! There is no dataset to delete... But I forgive you and not going to throw a error")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __call__(self,file_name,tokenizer,first_n=None,start_from=0,name="WICKED4950/MentalHeathEsther",local=False,answer_only=True,batch_size=8,maskq=False,toe_len=512):
        self.tokenizer = tokenizer
        try:
            self.tf_dataset = tf.data.Dataset.load(self.dt_save_path)
            self.return_tf()
        except:
            self.dataset_load(file_name=file_name,first_n=first_n,start_from=start_from,name=name,local=local)
            self.datasetprocess(answer_only=answer_only)
            if maskq:
                self.datasetprocess(answer_only=answer_only)
                self.mask_qa(conversations=self.gpt_sentence,tokenizer=tokenizer,len_=toe_len,batch_size=batch_size)
            else:
                self.tokenize(tokenizer=tokenizer,max_length=toe_len,batch_size=batch_size)
            tf.data.Dataset.save(self.tf_dataset, self.dt_save_path)


    def __len__(self):
        try:
            return len(self.gpt_sentence)
        except:
            return 0

    @property
    def __class__(self):
        return Dataset

    def return_tf(self):
        return self.tf_dataset