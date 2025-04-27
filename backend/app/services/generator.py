import os, openai

_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RapGenerator:
    def __init__(self, model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")):
        self.model = model

    def generate(self, artist: str, #sub_genre: str,
                 topic: str,
                 additional_context: str = None,
                 max_tokens: int = 256) -> str:
        prompt = (
            f"Generate lyrics to a rap song in the style of {artist}. "
            #f"Sub-genre: {sub_genre}. "
            f"The topic of the song should be about: {topic}. "
            f"Use this as additional context for the lyrics: {additional_context if additional_context else ''} "
            "Keep it about 16–24 lines. Return only the lyrics."
        )

        resp = _client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a rap lyric generator."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0.85,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()