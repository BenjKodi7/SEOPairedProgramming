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

# Ask user to enter the URL of their playlist and store it


# Create a function, getPlaylistID, that takes a playlist URL and uses a REGEX to 
# return the ID by itself. Store the ID (Testable Function)


# Use the stored ID with the "Get Playlist Items" Spotify API Endpoint to 
# access all of the songs (Testable Function)


# Parse through the reponse.json() and retrieve all of the song titles, artists, and genres
# 3 Seperate functions. Input - json dictionary Output - List of titles, artists, and genres


# Store the songs respectively with their titles, artists and genres into an SQL Database


# Give ChatGPT this database as input and ask it to tell the user about their:
    # Musical preferences
    # Personal insights
    # Personality
# All based on the inputted music


