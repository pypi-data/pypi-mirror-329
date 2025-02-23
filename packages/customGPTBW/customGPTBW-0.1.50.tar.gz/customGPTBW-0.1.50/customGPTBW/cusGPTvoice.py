

class Voice():
    def __init__(self,voice=""):
        import models
        import kokoro
        import torch
        print("Please run the following code to make use of this function --")
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