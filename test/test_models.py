# test/test_models.py
import unittest
import os
os.environ["OPENAI_API_KEY"] = "test"
os.environ["MUREKA_API_KEY"] = "test"

from backend.app import create_app, db
from backend.app.models import Song

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        # use an in‑memory SQLite for tests
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_song_save_and_query(self):
        with self.app.app_context():
            s = Song(
                title="Test",
                artist="Artist",
                topic="Topic",
                additional_context="Ctx",
                lyrics="Lyrics",
                audio=b"1234"
            )
            db.session.add(s)
            db.session.commit()

            # the newest song should be the one we just added
            newest = Song.query.order_by(Song.created.desc()).first()
            self.assertEqual(newest.title, "Test")
            self.assertEqual(newest.audio, b"1234")


if __name__ == '__main__':
    unittest.main()
