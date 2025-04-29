# backend/app/services/mureka_music.py
from __future__ import annotations

import os, time, requests

_API = "https://api.mureka.ai"

class MurekaMusic:
    """
    Fire-and-forget helper that:
      1. POSTs /v1/song/generate
      2. Polls /v1/song/query/<task_id> until 'succeeded'
      3. Downloads the first generated track and returns raw bytes
    """

    def __init__(self, model="auto", poll_every=2, timeout=180):
        self.model       = model
        self.poll_every  = poll_every
        self.timeout     = timeout
        self._headers    = {
            "Authorization": f"Bearer {os.getenv('MUREKA_API_KEY')}",
            "Content-Type": "application/json",
        }

    def _poll_task(self, task_id: str) -> dict:
        url = f"{_API}/v1/song/query/{task_id}"
        elapsed = 0
        while elapsed < self.timeout:
            resp = requests.get(url, headers=self._headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            if data["status"] == "succeeded":
                return data
            if data["status"] in {"failed", "timeouted", "cancelled"}:
                raise RuntimeError(f"Mureka task {task_id} ended as {data['status']}: "
                                   f"{data.get('failed_reason', '')}")
            time.sleep(self.poll_every)
            elapsed += self.poll_every
        raise TimeoutError(f"Mureka task {task_id} exceeded {self.timeout}s")

    def generate(self, lyrics: str, prompt: str | None = None) -> bytes:
        payload = {"lyrics": lyrics, "model": self.model}
        if prompt:
            payload["prompt"] = prompt

        # 1️⃣  kick off generation
        resp = requests.post(f"{_API}/v1/song/generate",
                             json=payload, headers=self._headers, timeout=60)
        resp.raise_for_status()
        task_id = resp.json()["id"]

        # 2️⃣  wait for completion
        task = self._poll_task(task_id)

        # 3️⃣  grab the audio URL (first choice)
        audio_url = task["choices"][0]["url"]          # docs show it under choices[]
        audio = requests.get(audio_url, timeout=120)
        audio.raise_for_status()
        return audio.content                           # usually MP3
