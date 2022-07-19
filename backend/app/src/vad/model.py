import torch
import logging

from pathlib import Path
from src.vad.utils import get_speech_timestamps, OnnxWrapper, init_jit_model
from src.logger import LogHandler


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())


class VAD:
    def __init__(self):
        self.min_speech_duration_ms = 350
        self.threshold = 0.4
        self.sampling_rate = 16_000
        self.MODEL_DIR = Path("/app/app/ml_models/vad/")
        self.model = self.load_model(onnx=True)

    def load_model(self, onnx=True):
        logger.debug("Loading VAD model")

        if onnx:
            try:
                model = OnnxWrapper(str(self.MODEL_DIR / 'silero_vad.onnx'))
                logger.debug("ONNX VAD loaded successfully")
            except Exception as e:
                logger.error("Error when loading VAD model from ONNX")
                logger.error(e, exc_info=True)
                raise e
        else:
            try:
                model, _ = init_jit_model(str(self.MODEL_DIR / 'silero_vad.jit'))
                logger.debug("JIT VAD loaded successfully")
            except Exception as e:
                logger.error("Error when loading VAD model from JIT")
                logger.error(e, exc_info=True)
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
