import torch
import logging
from pathlib import Path

from transformers import AutoModelForCTC, AutoProcessor
from typing import Union
from src.logger import LogHandler


N_JOBS = 10
torch.set_num_threads(N_JOBS)
logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())
logger.info(f"Setting torch to use {N_JOBS} threads!")


class ASR:
    def __init__(self):
        self.device = "cpu"
        self.sampling_rate = 16_000
        self.ACOUSTIC_MODEL_PATH = Path("/app/app/ml_models/acoustic")
        self.PROCESSOR_MODEL_PATH = Path("/app/app/ml_models/processor")
        self.load_model()
        logger.debug("ASR Model loaded!")

    def load_model(self) -> None:
        if not self.ACOUSTIC_MODEL_PATH.exists() or not self.PROCESSOR_MODEL_PATH.exists():
            logger.error("Path to models does not exist. Exiting...")
            return
        self.model = AutoModelForCTC.from_pretrained(
            self.ACOUSTIC_MODEL_PATH).to(self.device)
        self.processor = AutoProcessor.from_pretrained(
            self.PROCESSOR_MODEL_PATH)

    def predict(self, signal: torch.Tensor) -> Union[str, None]:
        inputs = self.processor(signal, sampling_rate=self.sampling_rate,
                                return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        logger.debug("logits predicted")
        transcription = self.processor.batch_decode(
            logits.cpu().numpy()).text[0]

        logger.debug("transcription predicted")

        return transcription
