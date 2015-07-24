from tgbot import plugintest
from twx.botapi import Update
from bot.indieshuffle import IndieShuPlugin
from httmock import HTTMock
import json


def _request_mock(url, request):
    return json.dumps({'posts': [{'url': 'http://www.indieshuffle.com/', 'sub_title': 'test', 'artist': 'test', "tags": [{"slug": "covers"}]}]})


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
        self.assertReplied(self.bot, ('\n ' + self._emoji_music + ' test by test\n \nhttp://www.indieshuffle.com/'))

    def test_latest(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/latest',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'Please select the genre: ')
        with HTTMock(_request_mock):
            self.bot.process_update(
                Update.from_dict({
                    'update_id': 1,
                    'message': {
                        'message_id': 1,
                        'text': 'all',
                        'chat': {
                            'id': 1,
                        },
                    }
                })
            )
        self.assertReplied(self.bot, ('\n ' + self._emoji_music + ' test by test\nhttp://www.indieshuffle.com/\n'))

    def test_popular(self):
        self.bot.process_update(
            Update.from_dict({
                'update_id': 1,
                'message': {
                    'message_id': 1,
                    'text': '/popular',
                    'chat': {
                        'id': 1,
                    },
                }
            })
        )
        self.assertReplied(self.bot, 'Please select the genre: ')
        with HTTMock(_request_mock):
            self.bot.process_update(
                Update.from_dict({
                    'update_id': 1,
                    'message': {
                        'message_id': 1,
                        'text': 'all',
                        'chat': {
                            'id': 1,
                        },
                    }
                })
            )
            self.assertReplied(self.bot, ('\n ' + self._emoji_music + ' test by test\nhttp://www.indieshuffle.com/\n'))
