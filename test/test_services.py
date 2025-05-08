# test/test_services.py

import os
os.environ["OPENAI_API_KEY"] = "test"
os.environ["MUREKA_API_KEY"] = "test"

import unittest
from unittest.mock import patch, MagicMock
from backend.app.services.generator import RapGenerator
from backend.app.services.mureka_music import MurekaMusic

class ServiceTestCase(unittest.TestCase):
    @patch('backend.app.services.generator._client')
    def test_rap_generator(self, mock_client):
        # Build a fake response object
        fake_resp = MagicMock()
        fake_msg  = MagicMock()
        fake_msg.content = "yo this is a rap"
        fake_choice = MagicMock()
        fake_choice.message = fake_msg
        fake_resp.choices = [fake_choice]

        # Whenever our code calls _client.chat.completions.create, return this fake
        mock_client.chat.completions.create.return_value = fake_resp

        gen = RapGenerator()
        text = gen.generate("Artist", "Topic", "Ctx")
        self.assertIn("yo this is a rap", text)

    @patch('backend.app.services.mureka_music.requests.get')
    @patch('backend.app.services.mureka_music.requests.post')
    def test_mureka_music(self, mock_post, mock_get):
        # 1️⃣ Fake the POST /generate
        fake_post = MagicMock()
        fake_post.status_code = 200
        fake_post.json.return_value = {"id": "task123"}
        mock_post.return_value = fake_post

        # 2️⃣ Fake the GET /query/<task_id> (first call)
        fake_poll = MagicMock()
        fake_poll.status_code = 200
        fake_poll.json.return_value = {
            "status": "succeeded",
            "choices": [{"url": "http://fake/audio"}]
        }

        # 3️⃣ Fake the GET audio URL (second call)
        fake_audio = MagicMock()
        fake_audio.status_code = 200
        fake_audio.content = b'\x00\x01\x02'

        # Side‑effect: first get() → poll, second get() → audio
        mock_get.side_effect = [fake_poll, fake_audio]

        mm = MurekaMusic()
        data = mm.generate("anything")
        self.assertEqual(data, b'\x00\x01\x02')

        # And test that a 500 from POST raises
        fake_error = MagicMock()
        fake_error.status_code = 500
        mock_post.return_value = fake_error
        with self.assertRaises(Exception):
            MurekaMusic().generate("oops")

if __name__ == '__main__':
    unittest.main()
