import base64
import pathlib, os
from flask import Blueprint, request, jsonify, render_template
from flask import Response, send_file
from .models import Song
from . import db
from .services.generator import RapGenerator
from .services.tts import RapVocalizer
from .services.mureka_music import MurekaMusic

# NEW


TEMPLATE_DIR = pathlib.Path(__file__).resolve().parents[2] / "front_end" / "templates"
STATIC_DIR = TEMPLATE_DIR.parent / "static"

bp = Blueprint(
    "routes",
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static"
)

# bp = Blueprint('routes', __name__)
generator = RapGenerator()
tts = RapVocalizer()

generator = RapGenerator()
# vocalizer = UberduckTTS()
musicgen = MurekaMusic()


@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/library")                   # HTML page
def library_page():
    return render_template("library.html")


@bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json(force=True)
    artist = data.get('artist', 'Unknown')
    # sub_genre = data.get('sub_genre', 'hip hop')
    topic = data.get('topic', 'life')
    additional_context = data.get('additional_context', None)

    lyrics = generator.generate(artist, #sub_genre,
                                topic,
                                additional_context=additional_context)
    # audio = vocalizer.synthesize(lyrics)
    # audio_bytes = tts.synthesize(lyrics)
    audio_bytes = musicgen.generate(
        lyrics,
        prompt=data.get("prompt")  # optional extra control
    )
    return jsonify({'lyrics': lyrics,
                    'audio': base64.b64encode(audio_bytes).decode('utf-8'),
                    "mime": "audio/mpeg"})

@bp.route('/songs', methods=['POST'])
def save_song():
    data = request.get_json(force=True)
    song = Song(
        title=data.get('title', f"{data.get('artist','Unknown')} track"),
        # title=data.get('title'),
        artist=data.get('artist'),
        topic=data.get('topic'),
        #sub_genre=data.get('sub_genre'),
        additional_context=data.get('additional_context'),
        lyrics=data.get('lyrics'),
        audio=base64.b64decode(data['audio']) if data.get('audio') else None
    )
    db.session.add(song)
    db.session.commit()
    return jsonify({'id': song.id}), 201

# @bp.route('/library')
# def library():
#     songs = Song.query.order_by(Song.created.desc()).all()
#     return jsonify([{
#         'id': s.id, 'title': s.title, 'artist': s.artist,
#         'created': s.created.isoformat()
#     } for s in songs])


@bp.route("/api/songs")                 # JSON feed used by JS
def songs_api():
    songs = Song.query.order_by(Song.created.desc()).all()
    return jsonify([
        {
            "id": s.id,
            "title":  s.title,
            "artist": s.artist,
            "created": s.created.isoformat(),
            "lyrics": (s.lyrics[:220] + "…") if len(s.lyrics) > 220 else s.lyrics,
            "has_audio": bool(s.audio)
        } for s in songs
    ])

# @bp.route('/songs/<int:sid>/audio')
# def song_audio(sid):
#     s = Song.query.get_or_404(sid)
#     return Response(s.audio, mimetype="audio/mpeg")   # MP3 from Mureka

@bp.route("/songs/<int:sid>/audio")     # stream MP3 back
def song_audio(sid):
    s = Song.query.get_or_404(sid)
    # if not s.audio:
    #     abort(404)
    return Response(s.audio, mimetype="audio/mpeg")

@bp.route("/songs/<int:sid>", methods=["DELETE"])
def delete_song(sid):
    song = Song.query.get_or_404(sid)
    db.session.delete(song)
    db.session.commit()
    return "", 204        # 204 No Content
