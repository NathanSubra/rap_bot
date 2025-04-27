import base64
import pathlib, os
from flask import Blueprint, request, jsonify, render_template
from .models import Song
from . import db
from .services.generator import RapGenerator
from .services.tts import RapVocalizer

TEMPLATE_DIR = pathlib.Path(__file__).resolve().parents[2] / "frontend" / "templates"

bp = Blueprint(
    "routes",
    __name__,
    template_folder=str(TEMPLATE_DIR)
)

# bp = Blueprint('routes', __name__)
generator = RapGenerator()
tts = RapVocalizer()


@bp.route("/")
def index():
    return render_template("index.html")


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
    audio_bytes = tts.synthesize(lyrics)
    return jsonify({'lyrics': lyrics,
                    'audio': base64.b64encode(audio_bytes).decode('utf-8')})

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

@bp.route('/library')
def library():
    songs = Song.query.order_by(Song.created.desc()).all()
    return jsonify([{
        'id': s.id, 'title': s.title, 'artist': s.artist,
        'created': s.created.isoformat()
    } for s in songs])
