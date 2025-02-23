import tensorflow as tf
from transformers import TFAutoModelForCausalLM, AutoTokenizer, AutoConfig
import sys
import psutil
from tqdm import tqdm


class ModelGPT():
    """
    The class that handles and holds the model and model related custom functions
    """

    def error_handler(func):
        """
        Just used for the training function so that it catches the last error when training the model and the last graph hits... Usefulll only when using the splited training.
        """
        def wrapped(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                pass
        return wrapped
    

    def __init__(self,mix_pre=False,use_default=False):
        """
        Create a instance of the ModelGPT class for handling functions and loaded model
        
        Args-
        - mix_pre -> Set this to true if you want to use 'mixed_bfloat16'
        - use_default -> Makes it so that the code uses the avaliable cpu rather than a tpu or gpu
        """
        self.model = None
        self.tokenizer = None
        self.saved_model_name = None
        self.context = []
        self.all_train_loss = []
        tf.config.optimizer.set_jit(True)
        try:
            if use_default:
                try:
                    tf.config.threading.set_intra_op_parallelism_threads(24)
                    tf.config.threading.set_inter_op_parallelism_threads(2)
                except:
                    pass
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
        """
        Used to load a gpt model from huggining face. You have to logged in the use private models and tokenizers
        
        Args-
        - name -> Give in the name of the resp from hugging face to load the model and the tokenizer
        - grad_check -> Set it to true if you want to load the gradentient check point comaptable model
        """
        from huggingface_hub import login, create_repo, upload_file

        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        with self.strategy.scope():
            if grad_check:
                config = AutoConfig.from_pretrained(name)
                config.gradient_checkpointing = True
                self.model = TFAutoModelForCausalLM.from_pretrained(name, config=config)
            else:
                self.model = TFAutoModelForCausalLM.from_pretrained(name)
    
    def load_custom_model(self,func,*args,**kwargs):
        """
        Used to load a custom model build and ready to be used (Must be a object compatable with every functions)
        
        Args-
        - model -> The model object on which the code can work on.
        """
        with self.strategy.scope():
            self.model = func(*args,**kwargs)
    
    def load_custom_tokenizer(self,name):
        """
        For now this function is used to load a tokenizer from hugging face alone without loading the model.
        
        Args-
        - name -> Name of the resp from which the function should load the tokenizer only.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def add_tokens(self,new_token_list):
        """
        Used to add new tokens into the model and the tokenizer. Both the tokeizer and the model should be loaded
        
        Args-
        - new_token_list -> Takes in a input of the type list containing string element to add the the tokenizer and model
        """
        self.tokenizer.add_tokens(new_token_list)
        with self.strategy.scope():
            self.model.resize_token_embeddings(len(self.tokenizer))

    def freeze(self,value,shift=0,mix=False):
        """
        Used to freeze and unfreeze blocks of models in patterns
        
        Args-
        - value -> Takes in a int to specifiy in which multiple the models layer will be unfreezed in
        - shift -> Used to add a integer value to add the the multiple to shift the unfreezen layer
        - mix -> Set this to True if you want to make it so that the function freeze blocks in patterns or the blocks will be unfreezed from the last
        """
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


    def train_model(self, dataset_,val_dataset=None ,epochs=1, lr=5e-5, final_lr=5e-5, loss_avg=1500, change_batch=500, split_training=False, val_split=0.1,val_log=500,batch_acc=1):
        """Used to train the loaded model
        
        Args-
        - dataset_ -> Main dataset to be used for the training (should be a tf.dataset)
        - val_dataset -> The validation dataset to be used
        - loss_avg -> Takes the loss of n number of the past loss from batch and calculates their average to be displayed
        - (NOT CREATED ANYMORE)"""

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
            clipped_gradients = [tf.clip_by_value(grad, -1.0, 1.0) for grad in gradients]
            optimizer.apply_gradients(zip(clipped_gradients, self.model.trainable_variables))
            return loss


        @tf.function
        def val_step(batch):
            input_ids = batch[0]['input_ids']
            attention_mask = batch[0]['attention_mask']
            labels = batch[1]

            outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            return loss 

        dataset_size = len(dataset_)
        self.dataset_size = dataset_size
        if val_split == 0:
            val = False
        if val_dataset != None:
            train_dataset = dataset_
        else:
            val_size = int(dataset_size * val_split)
            train_size = dataset_size - val_size
            train_dataset = dataset_.take(train_size)
            val_dataset = dataset_.skip(train_size)
        if val_log > dataset_size:
            val_log = dataset_size

        initial_lr = lr
        decay_rate = (final_lr / initial_lr) ** (1 / (dataset_size*epochs))
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=lr,
            decay_steps=1,
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
                val_losses = all_val_loss

                # Print the loss and overwrite it on each iteration
                avg_val_loss = float(sum(val_losses) / len(val_losses))
                sys.stdout.write(f'\r Calculating.... Validation Loss: {avg_val_loss:.4f}')  # Overwrite the previous print
                sys.stdout.flush()

            print("")
                

            
        with strategy.scope():
            # Distribute datasets
            dist_train_dataset = strategy.experimental_distribute_dataset(train_dataset)
            if val:
                dist_val_dataset = strategy.experimental_distribute_dataset(val_dataset)

            optimizer = tf.keras.optimizers.AdamW(learning_rate=lr_schedule)
            all_batch_count = 0
            for epoch in range(epochs):
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

                    self.all_train_loss.append(loss.numpy())
                    train_losses = self.all_train_loss[-loss_avg:]

                    memory_used = psutil.virtual_memory().used / (1024 ** 3)  # in GB
                    cpu_percent = psutil.cpu_percent(interval=0)  # in percentage

                    progress_bar.set_postfix(loss=(sum(train_losses) / len(train_losses)), memory=f"{memory_used:.2f} GB", cpu=f"{cpu_percent}%", inst_loss=(train_losses[-1]),perplexity=(tf.exp(sum(train_losses) / len(train_losses)).numpy()),current_lr=optimizer.learning_rate.numpy())
                
                if (val_log == dataset_size) and (val == True):
                    val_func(strategy=strategy,dist_val_dataset=dist_val_dataset)

        return self.all_train_loss


    def train_modelV2(self, dataset_,val_dataset=None ,epochs=1, lr=5e-5, final_lr=5e-5, loss_avg=1500, change_batch=500, split_training=False, val_split=0.1,val_log=500,batch_acc=1):
        val = True
        strategy = self.strategy

        @tf.function
        def train_step(batch):
            input_ids = batch[0]['input_ids']
            attention_mask = batch[0]['attention_mask']
            labels = batch[1]

            with tf.GradientTape() as tape:
                loss = self.model(input_ids, attention_mask=attention_mask, labels=labels).loss
            return loss , tape.gradient(loss, self.model.trainable_variables)
        
        @tf.function
        def apply_grad(list_gradients):
            avg_grads = [tf.math.add_n(grads) for grads in zip(*list_gradients)]
            avg_grads = [tf.math.divide(g, tf.cast(batch_acc, tf.float32)) for g in avg_grads]
            optimizer.apply_gradients(zip(avg_grads, self.model.trainable_variables))

        @tf.function
        def val_step(batch):
            return self.model(
                batch[0]['input_ids'], 
                attention_mask=batch[0]['attention_mask'], 
                labels=batch[1]
            ).loss

        dataset_size = len(dataset_)
        self.dataset_size = dataset_size
        if val_split == 0:
            val = False
        if val_dataset != None:
            train_dataset = dataset_
        else:
            val_size = int(dataset_size * val_split)
            train_size = dataset_size - val_size
            train_dataset = dataset_.take(train_size)
            val_dataset = dataset_.skip(train_size)
        if val_log > dataset_size:
            val_log = dataset_size

        initial_lr = lr
        decay_rate = (final_lr / initial_lr) ** (1 / (dataset_size*epochs))
        lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=lr,
            decay_steps=1,
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
                val_losses = all_val_loss

                avg_val_loss = float(sum(val_losses) / len(val_losses))
                sys.stdout.write(f'\r Calculating.... Validation Loss: {avg_val_loss:.4f}')
                sys.stdout.flush()

            print("")
                

            
        with strategy.scope():
            optimizer = tf.keras.optimizers.AdamW(learning_rate=lr_schedule)
            dist_train_dataset = strategy.experimental_distribute_dataset(train_dataset)
            if val:
                dist_val_dataset = strategy.experimental_distribute_dataset(val_dataset)

            all_batch_count = 0
            for epoch in range(epochs):
                all_val_loss = []

                # Training Loop
                progress_bar = tqdm(dist_train_dataset, desc=f"Epoch {epoch + 1} [Training]", unit="batch")
                i = 0
                j = 0
                list_gradients = []
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
                    per_replica_losses, per_replica_gradients = strategy.run(train_step, args=(batch,))
                    loss = strategy.reduce(tf.distribute.ReduceOp.MEAN, per_replica_losses, axis=None)
                    list_gradients.append([strategy.reduce(tf.distribute.ReduceOp.MEAN, g, axis=None) for g in per_replica_gradients])

                    if all_batch_count%batch_acc == 0:
                        strategy.run(apply_grad,args=(list_gradients,))
                        list_gradients = []
                    
                    if tf.math.is_nan(loss):
                        continue

                    self.all_train_loss.append(loss.numpy())
                    train_losses = self.all_train_loss[-loss_avg:]

                    progress_bar.set_postfix(loss=(sum(train_losses) / len(train_losses)), inst_loss=(train_losses[-1]),perplexity=(tf.exp(sum(train_losses) / len(train_losses)).numpy()),current_lr=optimizer.learning_rate.numpy())
                
                if (val_log == dataset_size) and (val == True):
                    val_func(strategy=strategy,dist_val_dataset=dist_val_dataset)

        return self.all_train_loss

    def save_model(self,name="path_to_save_your_model"):
        self.saved_model_name = name
        self.model.save_pretrained(name)
        self.tokenizer.save_pretrained(name)

    def upload(self,rep_name,path = None):
        if path == None:
            path = self.saved_model_name
        from huggingface_hub import login, create_repo, upload_file
        import os
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
    def push_model(self,name):
        from huggingface_hub import login, create_repo, upload_file
        repo_url = create_repo(name)
        print(f"Repository created at: {repo_url}")
        self.upload(name)

    @property
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