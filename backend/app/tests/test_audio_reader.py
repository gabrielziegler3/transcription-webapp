import os
import unittest
import torch
import torchaudio

from src.audio_reader import AudioReader


class TestAudioReader(unittest.TestCase):
    def setUp(self) -> None:
        self.audio_reader = AudioReader()
        self.test_filepath = '/tmp/test.wav'

        # Create a pure tone signal with frequency 1000 Hz
        self.sample_rate = 48000  # original sample rate
        self.freq = 1000  # frequency of signal
        self.duration = 1  # in seconds

        t = torch.linspace(0, self.duration, int(
            self.duration * self.sample_rate), dtype=torch.float32)  # time variable
        # pure tone signal
        signal = 0.5 * torch.sin(2 * torch.pi * self.freq * t)

        # Convert signal to 2d tensor
        signal = signal.unsqueeze(0)

        # Save the pure tone signal as a wav file
        torchaudio.save(self.test_filepath, signal, self.sample_rate)

    def test_audio_reader_resampling(self):
        # Use the AudioReader to read and resample the wav file
        audio_reader = AudioReader(sampling_rate=16000)  # desired sample rate
        resampled_signal = audio_reader.read_audio(self.test_filepath)

        # Check that the signal was read and resampled correctly
        self.assertIsNotNone(
            resampled_signal, "Failed to read and resample the audio signal")
        self.assertEqual(
            resampled_signal.shape[1], 16000, "The resampled signal does not have the correct length")
        self.assertEqual(audio_reader.duration, self.duration,
                         "The duration of the audio signal is not correct")

    def tearDown(self) -> None:
        os.remove(self.test_filepath)
