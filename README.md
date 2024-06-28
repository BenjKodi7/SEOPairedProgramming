# Paired Programming Project

### Project Requirements:
- API integration
- Creation, Querying, and Updating of Databases
- A call to the ChatGPT API and incorporation of the received response
- Adherence to PEP8 style
- A clear testing plan and appropriate unit tests
- Github Continuous Integration Automation for Style Checkers and Unit Tests


## Tune Teller AI
#### Tune Teller AI provides a fun and engaging way for users to learn what AI thinks about their personality based on their music taste

### Set Up:

#### Installing Libraries

 - pip install re
 - pip install os
 - pip install requests
 - pip install pandas
 - pip install sqlalchemy
 - pip install sqlite3
 - pip install openai

 #### Spotify API Credentials and Access Token:
   Provided below

#### OpenAI API Key
   Make an OpenAI Account and Follow the Instructions below to make an API Key \
   https://platform.openai.com/docs/api-reference/introduction
   
#### API Security Concerns:

In order to keep your Spotify credentials confidential, 
we need to hide the Client ID, Secret, and OpenAI API Key..

Open ".bashrc" so the variables are set every time the terminal re-starts: "sudo nano ~/.bashrc"

Scroll with a scrollwheel or use your arrow keys to get to the bottom of the file and add the variables (Provided Sample Spotify Credentials below):

export SPOTIFY_CLIENT_ID="4ec20579f49049ca9197877b90005e2a" \
export SPOTIFY_CLIENT_SECRET="f3047a0f01ea4195b5da9de036382a81" \
export OPENAI_KEY="Input your OpenAI API Key here"

Press "ctrl" (For Windows) or "command + x" (For Mac) to exit

Run the file so the environments are set for this terminal session: "source ~/.bashrc"

#### Running the File: 
Lastly, run this command "python3 main.py" in the terminal and you should be prompted to add the URL of your preferred Spotify Playlist.

Follow the directions prompted in the terminal to see your ChatGPT response.

### DISCLAIMER:
Playlist entries capped at 100 tracks each
