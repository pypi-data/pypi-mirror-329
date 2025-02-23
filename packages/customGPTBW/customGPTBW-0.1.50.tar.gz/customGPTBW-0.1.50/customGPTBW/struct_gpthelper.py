try:
    import tensorflow as tf
    from transformers import TFAutoModelForCausalLM, AutoTokenizer, AutoConfig
    from tqdm import tqdm
    import psutil
    import shutil
    import numpy as np
    import sys
except Exception as e:
    raise ImportError(f"Some of the modules are not imported correctly!\n{e}")
class Dataset():
    def __init__(self):
        self.questions = None
        self.answers = None
        self.gpt_sentence = None
        self.tf_dataset = None
        self.type = 0
        self.dt_save_path = "encoded_dataset"


    def dataset_loadqa(self,file_name,first_n=None,start_from=0,name="WICKED4950/MentalHeathEsther",local=True):
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
          dataset = load_dataset(name, data_files=f"{file_name}.csv")
          train_data_dict = dataset['train'].to_dict()
          if first_n == None:
              first_n = len(train_data_dict["question"])
          self.questions = train_data_dict["question"][start_from:first_n]
          self.answers = train_data_dict["answer"][start_from:first_n]
          self.type = 1

    def datasetgptraw(self,user_start="<|SOH|>",bot_start="<|SOB|>",answer_only=False):
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

    def mask_qu_multiple(self,tokenizer ,conversations ,len=1024,batch_size=8):
        all_input_ids = []
        all_attention_masks = []
        all_labels = []

        for conversation in tqdm(conversations, desc="Processing conversations", unit="conversation"):
            tokenized_output = tokenizer(
                conversation,
                return_tensors='tf',
                padding='max_length',  # Pad to the maximum length
                truncation=True,       # Truncate if longer than max_length
                max_length=len  # Set the maximum sequence length
            )
            input_ids = tokenized_output.input_ids
            attention_mask = tokenized_output.attention_mask

            # Create the labels
            labels = input_ids.numpy().copy()  # Make sure it's a NumPy array for easier manipulation

            # Mask out the question parts in the labels
            words = tokenizer.convert_ids_to_tokens(input_ids[0].numpy())
            labels[0][0] = -100  # Start by masking the first token

            for idx, token in enumerate(words):
                if token == "<|SOH|>":  # If it's a question start token, mask the subsequent tokens
                    try:
                        while words[idx] != "<|SOB|>":
                            labels[0][idx + 1] = -100
                            idx += 1
                    except:
                        pass

            # Convert labels back to TensorFlow tensors
            labels = tf.convert_to_tensor(labels)

            # Append input_ids, attention_mask, and labels to their respective lists
            all_input_ids.append(input_ids)
            all_attention_masks.append(attention_mask)
            all_labels.append(labels)

        dataset = self.create_tf_dataset(tf.concat(all_input_ids, axis=0),tf.concat(all_attention_masks, axis=0),tf.concat(all_labels, axis=0))
        dataset = dataset.shuffle(buffer_size=75000)  # Shuffle with buffer size of 1000
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE).cache()
        self.tf_dataset = dataset
        self.type = 3

    def create_tf_dataset(self,inputs,attention_mask=None,labels=None):
        if labels == None:
            input_ids = inputs['input_ids']
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

    def dataset_gpt(self, tokenizer, max_length=256, batch_size=8):
        if self.gpt_sentence is None:
            raise ValueError("Please run dataset_loadqa() and datasetgpt() first before processing.")

        # Tokenize the GPT sentences
        inputs = tokenizer(self.gpt_sentence, padding=True, truncation=True, return_tensors='tf', max_length=max_length)


        # Create the dataset and apply shuffle and batching
        dataset = self.create_tf_dataset(inputs)
        dataset = dataset.shuffle(buffer_size=75000)  # Shuffle with buffer size of 1000
        dataset = dataset.batch(batch_size)
        dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE).cache()
        self.tf_dataset = dataset
        self.type = 3

    def clear_save(self):
        try:
            shutil.rmtree("encoded_dataset")
            self.tf_dataset = None
        except FileNotFoundError:
            raise FileNotFoundError("Brother! There is no dataset to delete...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __call__(self,file_name,tokenizer,first_n=None,start_from=0,name="WICKED4950/MentalHeathEsther",local=False,answer_only=True,batch_size=8,maskq=False):
        self.tokenizer = tokenizer
        try:
            self.tf_dataset = tf.data.Dataset.load(self.dt_save_path)
            self.return_tf()
        except:
            self.dataset_loadqa(file_name=file_name,first_n=first_n,start_from=start_from,name=name,local=local)
            self.datasetgptraw(answer_only=answer_only)
            if maskq:
                self.datasetgptraw(answer_only=answer_only)
                self.mask_qu_multiple(conversations=self.gpt_sentence,tokenizer=tokenizer,len=512,batch_size=batch_size)
            else:
                self.dataset_gpt(tokenizer=tokenizer,max_length=512,batch_size=batch_size)
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

class ModelGPT():

    def error_handler(func):
        def wrapped(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                pass
        return wrapped
    
    def __init__(self,mix_pre=False,use_default=False):
        self.model = None
        self.tokenizer = None
        self.saved_model_name = None
        self.context = []
        tf.config.optimizer.set_jit(True)
        try:
            if use_default:
                tf.config.threading.set_intra_op_parallelism_threads(24)
                tf.config.threading.set_inter_op_parallelism_threads(2)
                raise ValueError("skip")
            resolver = tf.distribute.cluster_resolver.TPUClusterResolver()
            tf.config.experimental_connect_to_cluster(resolver)
            tf.tpu.experimental.initialize_tpu_system(resolver)
            self.strategy = tf.distribute.TPUStrategy(resolver)
            print("TPU connected")
        except ValueError:
            self.strategy = tf.distribute.MultiWorkerMirroredStrategy()
            print("Using default strategy")
        if mix_pre:
            policy = tf.keras.mixed_precision.Policy('mixed_bfloat16')
            tf.keras.mixed_precision.set_global_policy(policy)

    def load_gptmodel(self,name="gpt2",grad_check=False):
        from huggingface_hub import login, create_repo, upload_file
        login("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")
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        with self.strategy.scope():
            if grad_check:
                config = AutoConfig.from_pretrained(name)
                config.gradient_checkpointing = True
                self.model = TFAutoModelForCausalLM.from_pretrained(name, config=config)
            else:
                self.model = TFAutoModelForCausalLM.from_pretrained(name)

    def add_tokens(self,new_token_list):
        self.tokenizer.add_tokens(new_token_list)
        with self.strategy.scope():
            self.model.resize_token_embeddings(len(self.tokenizer))

    def freeze(self,value,shift=0,mix=False):
        if mix:
            for i, layer in enumerate(self.model.transformer.h):#self.model.get_layer(index=0).decoder.layers
                layer.trainable = False
                if ((i+shift)%value) ==0:
                    # Set the entire layer to not trainable
                    layer.trainable = True
        else:
            for i, layer in enumerate(self.model.transformer.h):
                layer.trainable = False
            for i, layer in enumerate(reversed(self.model.transformer.h)):
                if i == value:
                    break
                layer.trainable = True

        # Verify the frozen status of the layers
        """for i, layer in enumerate(self.model.transformer.h):
            print(f"Layer {i} {'Frozen' if not layer.trainable else 'Trainable'}")"""


    @error_handler
    def train_model(self, dataset_, epochs=1, lr=5e-5, decay_rate=1.00, decay_steps=1000, loss_avg=1500, distr=True, change_batch=500, split_training=False, val_split=0.1,val_log=500):
        val = True
        strategy = self.strategy

        @tf.function
        def train_step(batch):
            input_ids = batch[0]['input_ids']
            attention_mask = batch[0]['attention_mask']
            labels = batch[1]

            with tf.GradientTape() as tape:
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss

            gradients = tape.gradient(loss, self.model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
            return loss

        @tf.function
        def val_step(batch):
            input_ids = batch[0]['input_ids']
            attention_mask = batch[0]['attention_mask']
            labels = batch[1]

            outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            return loss

        if val_split == 0:
            val = False
        dataset_size = len(dataset_)
        val_size = int(dataset_size * val_split)
        train_size = dataset_size - val_size
        if val_log > dataset_size:
            val_log = dataset_size
        train_dataset = dataset_.take(train_size)
        val_dataset = dataset_.skip(train_size)


        # Learning Rate Scheduler
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=lr,
            decay_steps=decay_steps,
            decay_rate=decay_rate,
            staircase=False  # Smooth decay (not step-wise)
        )

        def val_func(strategy,dist_val_dataset):
            all_val_loss = []
            for batch in dist_val_dataset:
                per_replica_losses = strategy.run(val_step, args=(batch,))
                loss = strategy.reduce(tf.distribute.ReduceOp.MEAN, per_replica_losses, axis=None)

                if tf.math.is_nan(loss):
                    continue

                all_val_loss.append(loss.numpy())
                val_losses = all_val_loss[-loss_avg:]

                # Print the loss and overwrite it on each iteration
                avg_val_loss = float(sum(val_losses) / len(val_losses))
                sys.stdout.write(f'\r Calculating.... Validation Loss: {avg_val_loss:.4f}')  # Overwrite the previous print
                sys.stdout.flush()

            # After the loop, print the final loss
            print(f"\nFinal Validation Loss: {avg_val_loss:.4f}")

            
        with strategy.scope():
            # Distribute datasets
            dist_train_dataset = strategy.experimental_distribute_dataset(train_dataset)
            if val:
                dist_val_dataset = strategy.experimental_distribute_dataset(val_dataset)

            optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
            all_batch_count = 0
            for epoch in range(epochs):
                all_train_loss = []
                all_val_loss = []

                # Training Loop
                progress_bar = tqdm(dist_train_dataset, desc=f"Epoch {epoch + 1} [Training]", unit="batch")
                i = 0
                j = 0
                for batch in progress_bar:
                    if split_training:
                        if (j % change_batch) == 0:
                            print("switching")
                            self.freeze(4, shift=i, mix=True)
                            i += 1
                        j += 1
                    
                    all_batch_count = all_batch_count + 1
                    if ((all_batch_count%val_log) == 0) and (val_log != dataset_size) and (val == True):
                        val_func(strategy=strategy,dist_val_dataset=dist_val_dataset)
                    per_replica_losses = strategy.run(train_step, args=(batch,))
                    loss = strategy.reduce(tf.distribute.ReduceOp.MEAN, per_replica_losses, axis=None)

                    if tf.math.is_nan(loss):
                        continue

                    all_train_loss.append(loss.numpy())
                    train_losses = all_train_loss[-loss_avg:]

                    memory_used = psutil.virtual_memory().used / (1024 ** 3)  # in GB
                    cpu_percent = psutil.cpu_percent(interval=0)  # in percentage

                    progress_bar.set_postfix(loss=(sum(train_losses) / len(train_losses)), memory=f"{memory_used:.2f} GB", cpu=f"{cpu_percent}%", inst_loss=(train_losses[-1]))
                
                if (val_log == dataset_size) and (val == True):
                    val_func(strategy=strategy,dist_val_dataset=dist_val_dataset)



    def save_model(self,name="path_to_save_your_model"):
        self.saved_model_name = name
        self.model.save_pretrained(name)
        self.tokenizer.save_pretrained(name)

    def upload(self,rep_name,path = None):
        if path == None:
            path = self.saved_model_name
        from huggingface_hub import login, create_repo, upload_file
        import os
        # Log in to Hugging Face
        login("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")
        # Upload model files
        files = os.listdir(path)
        model_files = []
        for file_ in files:
            model_files.append(f"/content/{path}/{file_}")
        repo_path = rep_name

        for model_file in model_files:
            upload_file(
                path_or_fileobj=model_file,
                path_in_repo=model_file.split("/")[-1],
                repo_id=repo_path,
                repo_type="model",
            )
    def push_model(self,name,token):
        from huggingface_hub import login, create_repo, upload_file
        repo_url = create_repo(name, token)
        print(f"Repository created at: {repo_url}")
        self.upload(name)

    def get_context(self):
        return "".join(f"<|SOH|>{msg[0]}<|SOB|>{msg[1]}" for msg in self.context)

    def generate_text(self, prompt, sos="<|SOH|>", eos="<|SOB|>", recall_sent=4,sys_prom=None,show_rawinp=False,ret_sq=1,temperature=0.5,top_k=2):
        if prompt == "!clear":
            self.context = []
            return "Context cleared."

        input_text = "".join(f"{sos}{msg[0]}{eos}{msg[1]}" for msg in self.context[-recall_sent:])
        if sys_prom == None:
            pass
        else:
            input_text = "<|SYS|>"+sys_prom+input_text
        input_text += f"{sos}{prompt}{eos}"
        if show_rawinp:
            print(input_text)

        raw_responses = self.raw_pred(input_text, max_length=512,ret_sq=ret_sq,temperature=temperature,top_k=top_k)
        raw_responses = [raw_response.replace(" <|SOH|> ","<|SOH|>") for raw_response in raw_responses]
        raw_responses = [raw_response.replace("<|SOH|> ","<|SOH|>") for raw_response in raw_responses]
        raw_responses = [raw_response.replace(" <|SOH|>","<|SOH|>") for raw_response in raw_responses]
        raw_responses = [raw_response.replace(" <|SOB|> ","<|SOB|>") for raw_response in raw_responses]
        raw_responses = [raw_response.replace(" <|SOB|> ","<|SOB|>") for raw_response in raw_responses]
        raw_responses = [raw_response.replace(" <|SOB|> ","<|SOB|>") for raw_response in raw_responses]
        responses = [raw_response.split("<|SOB|>")[-1] for raw_response in raw_responses]
        responses = [raw_response.replace("<|SOH|>","") for raw_response in responses]
        if ret_sq != 1:
            count = 0
            for i in responses:
                print(count,i)
                count = count + 1
            index = input(": ")
            if index == "":
                index = 0
            try:
                self.context.append((prompt, responses[int(index)]))
            except:
                self.context.append((prompt, index))
        else:
            self.context.append((prompt, responses[0]))

        return responses

    def raw_pred(self, input, max_length=20, temperature=0.5,ret_sq=1,top_k=3):
        input_ids = self.tokenizer.encode(input, return_tensors='tf')

        # Create attention mask
        attention_mask = tf.ones_like(input_ids)

        with self.strategy.scope():
            outputs = self.model.generate(
                input_ids,
                attention_mask=attention_mask,  # Explicit attention mask
                max_length=input_ids.shape[1] + max_length,
                top_k=top_k,
                do_sample=True,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.encode("<|SOH|>", add_special_tokens=False)[0],  # Custom EOS token ID
                num_return_sequences=ret_sq  # Specify how many sequences to generate
            )

        # Decode generated output
        generated_text = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        return generated_text

class Voice():
    def __init__(self,voice=""):
        print("""!git clone https://huggingface.co/hexgrad/Kokoro-82M
        %cd Kokoro-82M
        !apt-get -qq -y install espeak-ng > /dev/null 2>&1
        !pip install -q phonemizer torch transformers scipy munch""")


        # 2️⃣ Build the model and load the default voicepack
        from models import build_model
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.MODEL = build_model('kokoro-v0_19.pth', device)
        self.VOICEPACK = torch.load(f'voices/af{voice}.pt', weights_only=True).to(device)

    def say(self,text):
        from kokoro import generate
        from IPython.display import display, Audio
        audio, out_ps = generate(self.MODEL, text, self.VOICEPACK)
        display(Audio(data=audio, rate=24000, autoplay=True))