import json
import re
import os
import requests
import pandas as pd  # pip install pandas
import sqlalchemy as db  # pip install aslalchemy
import sqlite3
import openai
from openai import OpenAI

# Gain Access to Spotify API --------------------------------------------------

AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

"""
 - REMEMBER TO CHANGE sudo nano ~/.bashrc
    - CHANGE TO DEFAULT SO THAT USER CAN INPUT THEIR OWN
    - Maybe hardcode?
 - Put into README.md that user must install imports
 - Maybe we can tell them to input their 5 fav albums
"""

# Connects to the Spotify API and returns the auth. response data -----


def connectSpotifyAPI():

    # Get client credentials from environment variables
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    # Make sure to run envir. var. (source ~/.bashrc)

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

        # Checks if client credentials are correctly loaded
        print("Client ID: Found")
        print("Client Secret: Found")

        # Return response
        return auth_response.json()
    else:
        print("Post request failed :(")
        print("Status Code: ", auth_response.status_code)
        return None


# Takes a URL and uses REGEX to return ID in URL ----------------------
def getPlaylistID(playlistURL: str) -> str:
    matches = re.findall(r'album/(\w+)', playlistURL)
    if matches:
        return matches[0]
    else:
        print("Failed to find ID in URL")
        return None


# Ask user to enter the playlist URL
# Returns the songs/artists in json format
def getUserData(auth_response_data):

    # playlist_ID_of_User = input("Enter the URL of your " +
    #                             "desired Spotify playlist: ")
    testURL = ("https://open.spotify.com/album/"
               "392p3shh2jkxUxY2VHvlH8?si=Yy8_QKeqQHClHOKzvAsIMw")

    # playlistID = getPlaylistID(playlist_ID_of_User)
    playlistID = getPlaylistID(testURL)

    # print(playlistID)   # test that getPlaylistID works correctly

    if playlistID is None:
        return None

    # Use the stored ID with the "Get Playlist Items" Spotify API Endpoint to
    # access all of the songs (Testable Function) --------------------

    # Check if 'access_token' is in the response
    if 'access_token' in auth_response_data:
        access_token = auth_response_data['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Get Playlist Items (GET) request
        response = requests.get(f"{BASE_URL}playlists/{playlistID}/tracks",
                                headers=headers)

        # Get Album Items (GET) request
        response = requests.get(f"{BASE_URL}albums/{playlistID}/tracks",
                                headers=headers)

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

            # print(tracks_df) # Test to see if outputted correctly

            # print(response.status_code)
            # utopia_url = ("https://open.spotify.com/album/"
            #               "18NOKLkZETa4sWwLMIm0UZ?si=JQNJKMDGQEGaHXCOsgLGqQ")
            # json_data = json.loads(response.text)

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
        error_description = auth_response_data.get('error_description',
                                                   'No error description')

        print("Error: 'access_token' not found in the response.")
        print("Response contains error: ", error)
        print("Error description: :", error_description)


# Parse through the reponse.json() and retrieve all of
        # the song titles, artists, and genres
# 3 Seperate functions:
        # Input - json dictionary
        # Output - List of titles, artists, and genres --------------------


# Store the songs respectively with their titles,
        # artists and genres into an SQL Database ------------------------
def makeSQLDB(trackData):
    # Convert the list of artists to a JSON string
    trackData['artists'] = trackData['artists'].apply(json.dumps)

    # Create Engine Object
    engine = db.create_engine('sqlite:///track_list.db')

    # Write DataFrame to SQL database
    trackData.to_sql('tracks', con=engine, if_exists='replace', index=False)

    # Read data back from SQL database and print it
    with engine.connect() as connection:
        query = db.text("SELECT * FROM tracks;")
        result = connection.execute(query)
        query_result = result.fetchall()
        df = pd.DataFrame(query_result, columns=['name', 'artists'])

        # Deserialize the JSON string back to a list
        df['artists'] = df['artists'].apply(json.loads)

    print("DF = ", df)


# Give ChatGPT this database as input and
    # ask it to tell the user about their: ---------------

    # Musical preferences
    # Personal insights
    # Personality
# All based on the inputted music -----------------------------------------

# Formats a prompt for the ChatGPT API based of the user's playlist data.
# Function Returns ChatGPT's insights.
def promptChat():

    # connect with the myTable database
    connection = sqlite3.connect("track_list.db")

    # cursor object
    crsr = connection.cursor()

    # execute the command to fetch all the data from the table emp
    crsr.execute("SELECT name, artists FROM tracks")

    # store all the fetched data in the ans variable
    tracks = crsr.fetchall()

    prompt_str = "\nTell me about myself based on my songs:\n"
    prompt_rest = ""
    print(prompt_str)

    count = 1
    for song, artists in tracks:
        # convert `artists`` into readable format
        matches = re.findall(r'"\s*([^"]+?)\s*"', artists)
        readable_artist = ', '.join(matches)
        prompt_rest += f"{count}. {song} by {readable_artist}\n"
        count += 1

    prompt_rest += ("\nI want to know what these songs say about my: \n"
                    "1. Musical preferences\n2. Personal insights"
                    "\n3. Personality\n")

    print(prompt_rest)

    # ChatGPT Stuff

    my_api_key = os.environ.get('OPENAI_KEY')
    openai.api_key = my_api_key
    # print(my_api_key)

    client = OpenAI(api_key=my_api_key)

    # Specify the model to use and the messages to send
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
             "You are a musical genius that's good at reading people."},
            {"role": "user", "content": prompt_rest}
        ]
    )

    return completion.choices[0].message.content

# Main (Only run when necessary)


if __name__ == "__main__":

    # Gain Access to Spotify API
    requestResponse = connectSpotifyAPI()

    if requestResponse is not None:

        # Get User's playlist data
        # Add a loop
        # input("Add another playlist?: ")
        playlistData = getUserData(requestResponse)

        if playlistData is not None:
            print("\n Next step: Convert data into SQL Data Base \n")
            # Update SQL DB if DB already exists
            makeSQLDB(playlistData)

            read = promptChat()

            print(read)

        # Make an SQL Data Base out of the playlist data

    print("\n-------------------------Program Ended--------------------------")
