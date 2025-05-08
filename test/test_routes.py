import os
os.environ["OPENAI_API_KEY"] = "test"
os.environ["MUREKA_API_KEY"] = "test"

import unittest
import json
from backend.app import create_app, db
from backend.app.models import Song

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        # The button reads "Spit Bars 🔥"
        self.assertIn(b'Spit Bars', resp.data)

    def test_library_page(self):
        resp = self.client.get('/library')
        self.assertEqual(resp.status_code, 200)
        # The H1 reads "🎵 My Library"
        self.assertIn(b'My Library', resp.data)

    def test_save_and_list_song(self):
        payload = {
            "title": "T1",
            "artist": "A1",
            "topic": "Top",
            "additional_context": "",
            "lyrics": "L1",
            "audio": None
        }
        save_resp = self.client.post('/songs', json=payload)
        # POST /songs returns 201 Created
        self.assertEqual(save_resp.status_code, 201)
        data = save_resp.get_json()
        self.assertIn('id', data)

        list_resp = self.client.get('/api/songs')
        self.assertEqual(list_resp.status_code, 200)
        songs = list_resp.get_json()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0]['title'], 'T1')

    def test_delete_song(self):
        # create one
        s = Song(title="X", artist="Y", topic="Z",
                 additional_context="", lyrics="", audio=None)
        with self.app.app_context():
            db.session.add(s)
            db.session.commit()
            sid = s.id

        del_resp = self.client.delete(f'/songs/{sid}')
        # DELETE returns 204 No Content
        self.assertEqual(del_resp.status_code, 204)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Song, sid))

if __name__ == '__main__':
    unittest.main()
