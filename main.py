import json
import re
import os
import requests
# import pandas as pd
# import sqlalchemy as db
"""
User enters playlist url of a public playlist. 
We access playlist id using Regex. (Testable Function)
Use Spotify API to access Playlist items (Testable Function)
Access all song titles and artists (put into database) (3 functions)
Get song titles 
Get song artists
Put them into the database
Ask ChatGPT to “tell me about myself” based on these songs and their artists (Testable function)
"""

# Gain Access to Spotify API -----------------------------

# Constants for Spotify API
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

# Get client credentials from environment variables
client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

"""
 - REMEMBER TO CHANGE sudo nano ~/.bashrc TO DEFAULT SO THAT USER CAN INPUT THEIR OWN
 - Put into README.md that user must install imports
 - Maybe we can tell them to input their 5 fav albums
"""

# Check if client credentials are correctly loaded
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")

# Make a POST request to get the access token
auth_response = requests.post(
    AUTH_URL,
    {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
)

# Print the status code and response
print("Status Code:", auth_response.status_code)
print("Response JSON:", auth_response.json())

# Parse the JSON response
auth_response_data = auth_response.json()

# Ask user to enter the URL of their playlist and store it--------------------------------

playlist_ID_of_User = input("Enter the URL of your desired Spotify playlist: ")

test_URL = "https://open.spotify.com/embed/playlist/1eSCRbeCHNCbDXhWhBpSLl?utm_source=generator"

# Create a function, getPlaylistID, that takes a playlist URL and uses a REGEX to 
# return the ID by itself. Store the ID (Testable Function) -------------------------------

def getPlaylistID(playlistURL: str) -> str:
    matches = re.findall('album/(\w+)', playlistURL)
    if matches:
        return matches[0]
    else:
        return "No playlist ID found"

# print(getPlaylistID(test_URL)) # Test Works

playlistID = getPlaylistID(playlist_ID_of_User)
print(playlistID)

# Use the stored ID with the "Get Playlist Items" Spotify API Endpoint to 
# access all of the songs (Testable Function) -----------------------------------------

# Check if 'access_token' is in the response
if 'access_token' in auth_response_data:
    access_token = auth_response_data['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}


    # Get Playlist Items (GET) request
    # response = requests.get(f"{BASE_URL}playlists/{playlistID}/tracks", headers=headers)

    # Get Album Items (GET) request
    response = requests.get(f"{BASE_URL}albums/{playlistID}/tracks", headers=headers)

    print(response.status_code)
    utopia = "https://open.spotify.com/album/18NOKLkZETa4sWwLMIm0UZ?si=JQNJKMDGQEGaHXCOsgLGqQ"
    json_data = json.loads(response.text)
 
    # Song names (and features)

    songNames = []

    for track_name in json_data['items']:
        songNames.append(track_name['name'])


    # Song artists
        
    artists = []
    for track_name in json_data['items']:
        artists.append(track_name['artists'][0]['name'])

else:
    print("Error: 'access_token' not found in the response.")
    error = auth_response_data.get('error', 'No error key')
    error_description = auth_response_data.get('error_description', 'No error description')
    print(f"Response contains error: {error}")
    print(f"Error description: {error_description}")


# Parse through the reponse.json() and retrieve all of the song titles, artists, and genres
# 3 Seperate functions. Input - json dictionary Output - List of titles, artists, and genres -----------------------------------------


# Store the songs respectively with their titles, artists and genres into an SQL Database -----------------------------------------


# Give ChatGPT this database as input and ask it to tell the user about their: -----------------------------------------
    # Musical preferences
    # Personal insights
    # Personality
# All based on the inputted music -----------------------------------------


