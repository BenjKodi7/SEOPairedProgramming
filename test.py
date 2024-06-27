import unittest
from main import connectSpotifyAPI, getPlaylistID, getUserData, makeSQLDB, promptChat

class test(unittest.TestCase):

    def test_connectSpotifyAPI(self):
        self.assertEqual(connectSpotifyAPI(1), 0)

    def test_getPlaylistID(self):
        self.assertEqual(getPlaylistID(1), 0)

    def test_getUserData(self):
        self.assertEqual(getUserData(1), 0)

    def test_makeSQLDB(self):
        self.assertEqual(makeSQLDB(1), 0)

    def test_promptChat(self):
        self.assertEqual(promptChat(1), 0)
 

