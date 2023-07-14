import unittest

from fastapi.testclient import TestClient
from server import app
from io import BytesIO

def read_file(file_path):
    with open(file_path, "rb") as f:
        return BytesIO(f.read())

def validate_speech_timestamps(timestamps):
    assert isinstance(timestamps, list)
    assert len(timestamps) > 0
    for timestamp in timestamps:
        assert "start" in timestamp
        assert "end" in timestamp
        assert isinstance(timestamp["start"], (int, float))
        assert isinstance(timestamp["end"], (int, float))
        assert timestamp["start"] <= timestamp["end"]

class TestServer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_audio_path = "./tests/data/short_speech.ogg"
        self.invalid_audio_path = "./tests/data/badfile.wav"

    def test_server_is_up_and_running(self):
        response = self.client.get("/")
        assert response.status_code == 200

    def test_valid_audio(self):
        audio_file = read_file(self.valid_audio_path)

        response = self.client.post(
            "/get_speech_timestamps", files={"file": ("short_speech.ogg", audio_file, "audio/ogg")})

        assert response.status_code == 200
        assert "speech_timestamps" in response.json()

        validate_speech_timestamps(response.json()["speech_timestamps"])
