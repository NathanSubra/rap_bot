# Placeholder TTS—returns silence so the front‑end audio tag still works.
class RapVocalizer:
    def synthesize(self, text: str, artist: str = None) -> bytes:
        return b""
