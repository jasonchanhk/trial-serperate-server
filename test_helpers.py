from core.helpers.lyrics import render_lyrics
from core.helpers.youtube import search_youtube_url

class TestHelperCase():
    def test_click_on_page(self, source):
        assert type(source) is str 

    def test_render_lyrics(self, source):
        english_arr = render_lyrics(source, 'english')
        spanish_arr = render_lyrics(source, 'spanish')
        assert type(english_arr) is list 
        assert type(spanish_arr) is list 
    
    def test_search_youtube_url(self):
        embed_url = search_youtube_url('hello', 'adele')
        assert type(embed_url) is str 
