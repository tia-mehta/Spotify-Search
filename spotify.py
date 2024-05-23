#import dotenv

import json
from dotenv import load_dotenv
import os
import base64
from requests import get, post
#loading environment variables specified in .env file
load_dotenv()
#gets the values for the environment variables specified in .env file 
client_id = os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")

#print(client_id, client_secret)
#function to obtain accress token from spotify account service using client credentials
# sends a POST request Spotify Accounts Service with the specified URL, headers, and data
# loads the results in json format and extracts the access token to obtain token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data= data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
#returns an authorization header dictionary with value as the bearer token
def get_auth_header(token):
    return{"Authorization" : "Bearer " + token}
# searches for a specific artist given the access token and artist name.
# queries the API with, HTTP GET request, and parses json result to return the artist 
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #builds the query string with the parameters and limits set to 1
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers= headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result)== 0:
        print("Artist does not exist")
        return None
    return json_result[0]
# function that returns the top 10 tracks of any given artist
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"  
    headers = get_auth_header(token)
    result = get(url, headers= headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


token = get_token()
result = search_for_artist(token, "Drake")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
#prints the top 10 tracks of artist 
for i,  song in enumerate(songs):
    print(f"{i+1}. {song['name']}")

