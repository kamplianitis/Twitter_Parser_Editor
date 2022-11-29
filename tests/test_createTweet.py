from datetime import date
import twitter_parser_editor
from unittest import TestCase
from unittest import mock
from nose.tools import *


class TestCreateTweet(TestCase):
    def setUp(self):
        twitter_parser_editor.changesList = []
        twitter_parser_editor.change_lines = 400
        twitter_parser_editor.curr_tweet_id = 400

    def test_createTweet(self, mocked_input):
        tweet_text = "Please share your thoughts:\t"
        expected_changes_list = [401, "create", {"text": tweet_text, "created_at": date.strftime("%d/%m/%Y %H:%M:%S")}]
        original_input = mock.builtins.input
        mock.builtins.input = lambda _: tweet_text
        twitter_parser_editor.createTweet()
        self.assertSequenceEqual(expected_changes_list, twitter_parser_editor.changesList, msg="CREATE_TWEET_TEXT: OK")
        self.assertEqual(twitter_parser_editor.change_lines, 401, msg="CREATE_TWEET_LINES: OK")
        self.assertEqual(twitter_parser_editor.curr_tweet_id, 401, msg="CREATE_TWEET_ID: OK")

if __name__ == '__main__':
    unittest.main()
