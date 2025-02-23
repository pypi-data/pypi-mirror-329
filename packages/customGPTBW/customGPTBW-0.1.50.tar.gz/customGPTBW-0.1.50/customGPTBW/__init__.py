import sys
import os
from huggingface_hub import login, create_repo, upload_file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cusGPTdataset import Dataset
from cusGPTmodel import ModelGPT
try:
    from cusGPTvoice import Voice
except:
    print("WARNING: The voice function is not working as expected... Please wait until it's fixed")

class Trainer():
    def __init__(self,mix_pre=False,use_default=False,ds_name=None) -> None:
        self.dataset = Dataset(ds_name=ds_name)
        self.model = ModelGPT(mix_pre,use_default)
        self.login_hf_code = None

    def login_hf(self,token):
        self.login_hf_code = token
        login(token)

    def data(self,file_name,first_n=None,start_from=0,name="WICKED4950/MentalHeathEsther",local=False,answer_only=True,batch_size=8,maskq=False,toe_len=512):
        if self.model.tokenizer == None:
            raise Exception("You have to load the model first because this functions uses the tokneizer of that model")
        else:
            self.dataset(file_name=file_name,tokenizer = self.model.tokenizer,first_n=first_n,start_from=start_from,name=name,local=local,answer_only=answer_only,batch_size=batch_size,maskq=maskq,toe_len=toe_len)

    def initVoice(self,voice_name=""):
        global voice
        voice = Voice(voice_name)

    def train(self,epochs=1,val_dataset=None, lr=5e-5, final_lr=5e-5,loss_avg=1500,change_batch=500,split_training=False,val_split=0,val_log=500,batch_acc=1,use_v2=False):
        if self.dataset.return_tf() == None:
            raise ValueError("You have to first load and process the data to train the model!")
        else:
            if use_v2:
                self.model.train_modelV2(self.dataset.return_tf(),val_dataset, epochs,lr, final_lr, loss_avg, change_batch=change_batch,split_training=split_training, val_split=val_split,val_log=val_log,batch_acc=batch_acc)
            else:
                self.model.train_model(self.dataset.return_tf(),val_dataset, epochs,lr, final_lr, loss_avg, change_batch=change_batch,split_training=split_training, val_split=val_split,val_log=val_log,batch_acc=batch_acc)
            print("training done!")

    def push_model(self,name="saved_model",resp_name=None):
        if self.login_hf_code == None:
            raise ValueError("You have to log in into your hf account using .login_tf('Code here')")
        if resp_name == None:
            raise Exception("You have to give a name for the place to save the model")
        self.model.save_model(name)
        self.model.push_model(resp_name)


def dataset_obj(ds_name):
    return Dataset(ds_name=ds_name)