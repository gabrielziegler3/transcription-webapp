import torch
import torchaudio


class AudioReader:
    def __init__(self):
        self.sampling_rate = 16_000
        self.duration = 0

    def read_audio(self, content: bytes) -> torch.Tensor:
        signal, sr = torchaudio.load(content)

        self.duration = signal.size()[-1] / sr

        if sr != self.sampling_rate:
            print(f"Resampling from {sr} to {self.sampling_rate}")
            signal = torchaudio.transforms.Resample(sr, self.sampling_rate)(signal)

        print("Signal with shape:", signal.shape)

        return signal.squeeze(0)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: float):
        self._duration = value