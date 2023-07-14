import torch
import torchaudio
import logging

from typing import Optional
from src.logger import LogHandler

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logger.addHandler(LogHandler())


class AudioReader:
    def __init__(self, sampling_rate: int = 16_000):
        """
        Initialize the AudioReader.

        Args:
            sampling_rate: Desired sampling rate for audio signals.
        """
        self.sampling_rate = sampling_rate
        self._duration = 0

    def read_audio(self, content: bytes) -> Optional[torch.Tensor]:
        """
        Read audio content.

        Args:
            content: Byte content of the audio.

        Returns:
            torch.Tensor if successful, None otherwise.
        """
        try:
            signal, sr = torchaudio.load(content, normalize=True)
        except Exception as e:
            logger.error(f"Failed to read audio of size {len(content)} bytes")
            logger.error(e, exc_info=True)
            return None

        self.duration = signal.size()[-1] / sr

        if sr != self.sampling_rate:
            logger.info(f"Resampling from {sr} to {self.sampling_rate}")
            signal = torchaudio.transforms.Resample(
                sr, self.sampling_rate)(signal)

        logger.info(f"Signal shape {signal.shape}")

        return signal

    @property
    def duration(self) -> float:
        """Get the duration of the audio signal."""
        return self._duration

    @duration.setter
    def duration(self, value: float):
        """Set the duration of the audio signal."""
        self._duration = value
