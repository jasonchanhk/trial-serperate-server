from pytube import Search

def search_youtube_url(song_name, artist_name):
    yt_search = Search(song_name + " " + artist_name)
    embed_url = yt_search.results[0].embed_url
    return embed_url
