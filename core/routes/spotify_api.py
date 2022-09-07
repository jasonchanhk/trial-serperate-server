from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from dotenv import load_dotenv
from os import environ
import requests
import base64   
from urllib.parse import urlencode


load_dotenv()

client_id = environ.get('client_id')
client_secret=environ.get('client_secret')

spotify_api = Blueprint('spotify_api', __name__)

@spotify_api.route('/', methods=["POST"])
@cross_origin(origin='*')
def get_spotify_details():
    #The following bit of code relates to ensuring that data is received properly from 
    #the front end. 

    form = request.json
    song_name = form["songName"]
    artist_name = form["artistName"]
    from_language = form["fromLanguage"]
    to_language = form["toLanguage"]

    #The next block of code relates to generating an access token which means the spotify api
    # can actually be used. In other words, it is not enough to simply have an API key - 
    # you must use it to generate an access token which can then be used to get stuff from API.

    access_token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    headers = {
        "Authorization": "Basic " + f"{client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(access_token_url, 'grant_type=client_credentials', headers=headers)
    r_json = r.json()
    access_token = r_json.get("access_token")
    API_headers = {
        "Authorization": "Bearer " + f"{access_token}"
    }
    API_url = "https://api.spotify.com/v1/search?"

    data = {
        "q": f"{artist_name} {song_name}",
        "type": "track,artist",
        "limit": 3
    }

    encoded_data = urlencode(data)
    API_url += encoded_data
    spotify_request = requests.get(API_url, headers=API_headers)
    spotify_results_json = spotify_request.json()

    # The following code relates to ensuring that when a user types in a song and artist,
    # they actually get the correct result. For example, if a user looks for the song "Hello"
    # by Adele, the first result is some random cover by some nobody. It is the second result 
    # that is the song by Adele. The best way to ensure that the correct artist and track are
    # being selected is to call the first 3 results and then choose the artist with the highest
    # followers.

    artist_data = spotify_results_json["artists"]["items"]
    track_data = spotify_results_json["tracks"]["items"]
    follower_array = []
    for each in artist_data:
        follower_array.append(each["followers"]["total"])
    index_for_track_and_artist = follower_array.index(max(follower_array))

    #The next batch of code relates to extracting the relevant info needed to make an API call
    # to the spotify recommendations endpoint. Based on the info we extract here, we will get back 
    # 3 results which have been recommended by Spotify.

    artist_spotify_id = artist_data[index_for_track_and_artist]["id"]
    album_name = track_data[index_for_track_and_artist]["album"]["name"]
    album_url = track_data[index_for_track_and_artist]["album"]["images"][0]["url"]
    track_spotify_id = track_data[index_for_track_and_artist]["id"]
    artist_genres = artist_data[index_for_track_and_artist]["genres"]
    if len(artist_genres) > 3:
        artist_genres = artist_genres[:3]
    artist_genres = ", ".join(str(x) for x in artist_genres)
    
    return jsonify(artist_spotify_id, track_spotify_id, artist_genres, album_name, album_url)

@spotify_api.route('/recommendations', methods=["POST"])
@cross_origin(origin='*')
def get_spotify_recommendations():
    #The following bit of code relates to ensuring that data is received properly from 
    #the front end. 

    form = request.json
    song_name = form["songId"]
    artist_name = form["artistId"]
    genres = form["genres"]

    
    #The next block of code relates to generating an access token which means the spotify api
    # can actually be used. In other words, it is not enough to simply have an API key - 
    # you must use it to generate an access token which can then be used to get stuff from API.

    access_token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    headers = {
        "Authorization": "Basic " + f"{client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(access_token_url, 'grant_type=client_credentials', headers=headers)
    r_json = r.json()
    access_token = r_json.get("access_token")
    API_headers = {
        "Authorization": "Bearer " + f"{access_token}"
    }
    
    recommendations_url = "https://api.spotify.com/v1/recommendations?"

    recommendations_data = {
        "limit": 3,
        "market": "US",
        "seed_artists": f"{artist_name}",
        "seed_genres": f"{genres}",
        "seed_tracks": f"{song_name}"
    }
    

    encoded_recommendations_data = urlencode(recommendations_data)
    recommendations_url += encoded_recommendations_data
    
    recommendation_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    recommendations_request = requests.get(recommendations_url, headers=recommendation_headers)
    recommendations_request_json = recommendations_request.json()

    return jsonify(recommendations_request_json)


    
@spotify_api.route('/reccard', methods=["POST"])
@cross_origin(origin='*')
def get_spotify_reccard_details():

    details = request.json

    song_name = details["songName"]
    artist_name = details["artistName"]

    access_token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    headers = {
        "Authorization": "Basic " + f"{client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(access_token_url, 'grant_type=client_credentials', headers=headers)
    r_json = r.json()
    access_token = r_json.get("access_token")

    API_headers = {
        "Authorization": "Bearer " + f"{access_token}"
    }

    API_url = "https://api.spotify.com/v1/search?"

    data = {
        "q": f"{artist_name} {song_name}",
        "type": "track,artist",
        "limit": 3
    }

    encoded_data = urlencode(data)
    API_url += encoded_data
    spotify_request = requests.get(API_url, headers=API_headers)
    spotify_results_json = spotify_request.json()


    # The following code relates to ensuring that when a user types in a song and artist,
    # they actually get the correct result. For example, if a user looks for the song "Hello"
    # by Adele, the first result is some random cover by some nobody. It is the second result 
    # that is the song by Adele. The best way to ensure that the correct artist and track are
    # being selected is to call the first 3 results and then choose the artist with the highest
    # followers.

    artist_data = spotify_results_json["artists"]["items"]
    track_data = spotify_results_json["tracks"]["items"]

    return jsonify(artist_data, track_data)



@spotify_api.route('/artistinfo', methods=["POST"])
@cross_origin(origin='*')
def get_spotify_artist_genres():

    details = request.json
    artist_spotify_id = details["artistSpotify"]

    access_token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    headers = {
        "Authorization": "Basic " + f"{client_creds_b64.decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(access_token_url, 'grant_type=client_credentials', headers=headers)
    r_json = r.json()
    access_token = r_json.get("access_token")

    API_headers = {
        "Authorization": "Bearer " + f"{access_token}"
    }

    API_url = "	https://api.spotify.com/v1/artists/"

    API_url += artist_spotify_id

    spotify_request = requests.get(API_url, headers=API_headers)
    spotify_results_json = spotify_request.json()
    genres = spotify_results_json["genres"]
    if len(genres) > 3:
        genres = genres[:3]
    genres = ", ".join(str(x) for x in genres)



    return jsonify(genres)


   