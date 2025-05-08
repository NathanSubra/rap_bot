import unittest
from ..backend.app import db
from ..backend.app.models import Song


class TestStringMethods(unittest.TestCase):

    def test_song_save(self):
        song = Song(
            title="testTitle",
            artist="testArtist",
            topic="testTopic",
            # sub_genre=data.get('sub_genre'),
            additional_context="testContext",
            lyrics="testLyrics",
            audio=None
        )
        db.session.add(song)
        db.session.commit()
        self.assertEqual(Song.query.order_by(Song.created.desc()).first(), song)
