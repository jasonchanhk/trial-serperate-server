from flask import Blueprint, request, jsonify
from ..helpers.lyrics import click_on_page, render_lyrics
from ..helpers.youtube import search_youtube_url

lyrics_routes = Blueprint('lyrics', __name__)

@lyrics_routes.route('/', methods=["POST"])
def home():
        song_name = request.json["songName"]
        artist_name = request.json["artistName"]

        source = click_on_page(song_name, artist_name)
        english_lyrics = render_lyrics(source, "english")
        spanish_lyrics = render_lyrics(source, "spanish")

        # to be moved to James fetch
        embed_url = search_youtube_url(song_name, artist_name)

        return jsonify({"embed": embed_url, "spanish": spanish_lyrics, "english": english_lyrics}), 200
