import json
import re
import os
import requests
import pandas as pd     # pip install pandas
import sqlalchemy as db # pip install aslalchemy

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

# Gain Access to Spotify API ---------------------------------------------------

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

"""
 - REMEMBER TO CHANGE sudo nano ~/.bashrc TO DEFAULT SO THAT USER CAN INPUT THEIR OWN
 - Put into README.md that user must install imports
 - Maybe we can tell them to input their 5 fav albums
"""

# Connects to the Spotify API and returns the authentication response data -----
def connectSpotifyAPI():

    # Get client credentials from environment variables
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

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

    # Check that the status code of the POST request is valid
    if auth_response.status_code == 200:
        # Return response
        return auth_response.json()
    else:
        print("Post request failed :(")
        print("Status Code: ", auth_response.status_code)
        return None


# Takes a URL and uses REGEX to return ID in URL -------------------------------
def getPlaylistID(playlistURL: str) -> str:
    matches = re.findall('album/(\w+)', playlistURL)
    if matches:
        return matches[0]
    else:
        print("Failed to find ID in URL")
        return None


# Ask user to enter the URL of their playlist and return the songs and artists in a json format
def getUserData(auth_response_data):

    #playlist_ID_of_User = input("Enter the URL of your desired Spotify playlist: ")
    testURL = "https://open.spotify.com/album/392p3shh2jkxUxY2VHvlH8?si=Yy8_QKeqQHClHOKzvAsIMw"

    #playlistID = getPlaylistID(playlist_ID_of_User)
    playlistID = getPlaylistID(testURL)

    print(playlistID)       # test that getPlaylistID works correctly

    if playlistID is None:
        return None

    # Use the stored ID with the "Get Playlist Items" Spotify API Endpoint to 
    # access all of the songs (Testable Function) -----------------------------------------

    # Check if 'access_token' is in the response
    if 'access_token' in auth_response_data:
        access_token = auth_response_data['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}


        # Get Playlist Items (GET) request
        # response = requests.get(f"{BASE_URL}playlists/{playlistID}/tracks", headers=headers)

        # Get Album Items (GET) request
        response = requests.get(f"{BASE_URL}albums/{playlistID}/tracks", headers = headers)

        if response.status_code == 200:

            albumData = response.json()

            # Create a list to store track details
            tracks = []

            for item in albumData['items']:
                track_name = item['name']
                artist_names = [artist['name'] for artist in item['artists']]
                tracks.append({'name': track_name, 'artists': artist_names})

            # Convert to DataFrame
            tracks_df = pd.DataFrame(tracks)

            print(tracks_df)

            '''
            print(response.status_code)
            utopia = "https://open.spotify.com/album/18NOKLkZETa4sWwLMIm0UZ?si=JQNJKMDGQEGaHXCOsgLGqQ"
            json_data = json.loads(response.text)
            '''
            return tracks_df

        else:
            print("Attempt to retrieve album tracks failed :(")
            print("Status Code: ", response.status_code)
            return None

        
        '''
        albumDataDF = pd.DataFrame.from_dict(albumData)
        print(albumDataDF)

        items = albumDataDF['items']['name']
        print(type(items))
        itemDF = pd.Series(items)

        print("Items DF: \n", itemDF)

        '''

        '''
        # Song names (and features)

        songNames = []

        for track_name in json_data['items']:
            songNames.append(track_name['name'])
        # Song artists
            
        artists = []
        for track_name in json_data['items']:
            artists.append(track_name['artists'][0]['name'])

        return [songNames, artists]

        '''
    else:
        error = auth_response_data.get('error', 'No error key')
        error_description = auth_response_data.get('error_description', 'No error description')

        print("Error: 'access_token' not found in the response.")
        print("Response contains error: ", error)
        print("Error description: :", error_description)


# Parse through the reponse.json() and retrieve all of the song titles, artists, and genres
# 3 Seperate functions. Input - json dictionary Output - List of titles, artists, and genres -----------------------------------------


# Store the songs respectively with their titles, artists and genres into an SQL Database -----------------------------------------
def makeSQLDB(trackData):
    # Convert the list of artists to a JSON string
    trackData['artists'] = trackData['artists'].apply(json.dumps)

    # Create Engine Object
    engine = db.create_engine('sqlite:///track_list.db')

    # Write DataFrame to SQL database
    trackData.to_sql('tracks', con=engine, if_exists='replace', index=False)

    # Read data back from SQL database and print it
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM tracks;")).fetchall()
        df = pd.DataFrame(query_result, columns=['name', 'artists'])

        # Deserialize the JSON string back to a list
        df['artists'] = df['artists'].apply(json.loads)

    print("DF = ", df)


# Give ChatGPT this database as input and ask it to tell the user about their: -----------------------------------------
    # Musical preferences
    # Personal insights
    # Personality
# All based on the inputted music -----------------------------------------


# Main 
if __name__ == "__main__":

    # Gain Access to Spotify API
    requestResponse = connectSpotifyAPI()

    if requestResponse is not None:

        # Get User's playlist data
        playlistData = getUserData(requestResponse)

        if playlistData is not None:
            print("Next step: Convert data into SQL Data Base")
            makeSQLDB(playlistData)
        
        # Make an SQL Data Base out of the playlist data

    print("Program Ended")
    print("-----------------------------------------------------")
        
