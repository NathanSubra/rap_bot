import os
from dotenv import load_dotenv        # pip install python-dotenv
from flask import Flask, request, render_template, url_for
import openai                         # pip install openai

load_dotenv()                         # pulls OPENAI_API_KEY from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


def generate_rap(artist: str, content: str) -> str:
    """Call the ChatGPT API and return rap lyrics."""
    system_msg = (
        "You are RapBot, a master lyricist. "
        "You will receive an artist's name."
        "You will also receive a short description of the song content."
        "Generate a song in the style of the artist about the content of the song."
        "When the user gives you a topic, answer ONLY with polished rap lyrics—"
        "no extra commentary, no stage directions."
        "If you do not receive an artist, generate a rap song about the content in any rapper style"
        "If you do not receive content, generate a rap song about anything in the style of the artist"
    )

    if artist == "":
        artist = "None"

    if content == "":
        content = "None"

    prompt_text = f"Artist: {artist}\nTopic / Content: {content}"

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",          # or any model you prefer
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": prompt_text},
        ],
        max_tokens=256,
        temperature=0.95,             # crank creativity up
    )
    return response.choices[0].message.content.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    rap = None
    #user_prompt = ""
    artist = ""
    content = ""

    if request.method == "POST":
        #user_prompt = request.form["prompt"].strip()
        artist = request.form.get("artist", "").strip()
        content = request.form.get("content", "").strip()

        if artist and content:
            rap = generate_rap(artist, content)

    return render_template("index.html", rap=rap, artist=artist, content=content)


@app.route("/library", methods=["GET"])
def library():
    return render_template("library.html")

if __name__ == "__main__":
    # Set debug=False in production
    app.run(debug=True, host="0.0.0.0", port=1234)
