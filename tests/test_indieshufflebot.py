from tgbot import plugintest
from twx.botapi import Update
from bot.indieshuffle import IndieShuPlugin
from httmock import HTTMock
import json


def _request_mock(url, request):
    return json.dumps({'posts': [{'url': 'http://www.indieshuffle.com/', 'id': '1','sub_title': 'test', 'artist': 'test', "tags": [{"slug": "covers"}], "songs": [{"url": "http://www.indieshuffle.com/", "title": "test"}]}]})


class IndieShuffle_Test(plugintest.PluginTestCase):

    def setUp(self):
        self._emoji_music = u'\U0001F3B5'
        self._emoji_save = u'\U0001F3B4'
        self.bot = self.fake_bot('', plugins=[IndieShuPlugin()])

    def test_tsong(self):
        with HTTMock(_request_mock):
            self.bot.process_update(
                Update.from_dict({
                    'update_id': 1,
                    'message': {
                        'message_id': 1,
                        'text': '/tsong',
                        'chat': {
                            'id': 1,
                        },
                    }
                })
            )
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song 1'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)

    def test_latest(self):
        with HTTMock(_request_mock):
            self.bot.process_update(
                Update.from_dict({
                    'update_id': 1,
                    'message': {
                        'message_id': 1,
                        'text': '/latest 1',
                        'chat': {
                            'id': 1,
                        },
                    }
                })
            )
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song 1\n \n Tags: covers'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)

    def test_popular(self):
        with HTTMock(_request_mock):
            self.bot.process_update(
                Update.from_dict({
                    'update_id': 1,
                    'message': {
                        'message_id': 1,
                        'text': '/popular 1',
                        'chat': {
                            'id': 1,
                        },
                    }
                })
            )
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song 1\n \n Tags: covers'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)
