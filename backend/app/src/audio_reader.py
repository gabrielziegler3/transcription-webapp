import torch
import torchaudio
import logging

from typing import Union
from src.logger import LogHandler


logger = logging.getLogger(__file__)
logger.setLevel('DEBUG')
logger.addHandler(LogHandler())


class AudioReader:
    def __init__(self):
        self.sampling_rate = 16_000
        self.duration = 0

    def read_audio(self, content: bytes) -> Union[torch.Tensor, None]:
        try:
            signal, sr = torchaudio.load(content, normalize=True)
        except Exception as e:
            logger.error("Failed to read audio")
            logger.error(e, exc_info=True)
            return

        self.duration = signal.size()[-1] / sr

        if sr != self.sampling_rate:
            logger.info(f"Resampling from {sr} to {self.sampling_rate}")
            signal = torchaudio.transforms.Resample(sr, self.sampling_rate)(signal)

        logger.info(f"Signal shape {signal.shape}")

        return signal

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = value
