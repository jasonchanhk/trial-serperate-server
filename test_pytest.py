import json

class TestAPICase():
    def test_post_lyrics(self, api):
        mock_data = json.dumps({'song-name': 'hello', 'artist-name': 'adele'})
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/lyrics', data=mock_data, headers=mock_headers)
        assert res.status == '308 PERMANENT REDIRECT'
