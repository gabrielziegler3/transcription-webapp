import torch

from pathlib import Path
from src.logger import logger
from src.vad.utils import get_speech_timestamps




class VAD:
    def __init__(self):
        self.model = self.load_model(onnx=True)
        self.min_speech_duration = 350
        self.threshold = 0.4
        self.sampling_rate = 16_000
        self.MODEL_DIR = Path("/backend/ml_models/vad/")

    def load_model(self, onnx=True):
        logger.debug("Loading VAD model")
        try:
            model, _ = torch.hub.load(repo_or_dir=self.MODEL_DIR,
                                      model='silero_vad',
                                      force_reload=False,
                                      onnx=onnx)
            logger.debug("VAD loaded successfully")
        except Exception as e:
            logger.error("Error when loading VAD model")
            logger.error(e)
            raise e

        return model

    def predict(self, signal: torch.Tensor, return_seconds=True) -> list:
        logger.debug("Predicting VAD")
        timestamps = get_speech_timestamps(audio=signal,
                                           model=self.model,
                                           threshold=self.threshold,
                                           sampling_rate=self.sampling_rate,
                                           min_speech_duration_ms=self.min_speech_duration_ms,
                                           return_seconds=return_seconds)

        return timestamps
