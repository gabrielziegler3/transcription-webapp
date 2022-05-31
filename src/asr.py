import torch

from transformers import AutoModelForCTC, AutoProcessor
from typing import Optional


class ASR:
    def __init__(self):
        self.model_id = "patrickvonplaten/hubert-xlarge-ls960-ft-4-gram"
        self.device = "cpu"
        self.load_model()
        self.sampling_rate = 16_000
        print("ASR Model loaded!")

    def load_model(self):
        self.model = AutoModelForCTC.from_pretrained(self.model_id).to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id)

    def predict(self, signal: torch.Tensor) -> Optional[str]:
        inputs = self.processor(signal, sampling_rate=self.sampling_rate,
                                return_tensors="pt")
        print("Inputs processed")
        inputs = {k: v.to(self.device) for k,v in inputs.items()}

        print("inputs:")
        print(inputs)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        print("logits predicted")
        transcription = self.processor.batch_decode(logits.cpu().numpy()).text[0]

        print("transcription predicted")

        return transcription
