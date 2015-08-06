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
        self.plugin = IndieShuPlugin()
        self.bot = self.fake_bot('', plugins=[self.plugin])
        self.received_id = 1

    def receive_message(self, text, sender=None, chat=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        if chat is None:
            chat = sender

        self.bot.process_update(
            Update.from_dict({
                'update_id': self.received_id,
                'message': {
                    'message_id': self.received_id,
                    'text': text,
                    'chat': chat,
                    'from': sender,
                }
            })
        )

        self.received_id += 1

    def test_song(self):
        self.receive_message('/song  1')
        self.assertReplied(self.bot, 'I couldn\'t find your music')
        with HTTMock(_request_mock):
            self.test_tsong()
            self.receive_message('/song  1')
        #self.assertReplied(self.bot, 'Downloading test...')

    def test_tsong(self):
        with HTTMock(_request_mock):
            self.receive_message('/tsong')
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song1'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)

    def test_latest(self):
        with HTTMock(_request_mock):
            self.receive_message('/latest 1')
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song1'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)

    def test_popular(self):
        with HTTMock(_request_mock):
            self.receive_message('/popular 1')
        msg_reply = '\n \n' + self._emoji_music + ' test by test'
        msg_reply += '\n \n' + self._emoji_save + ' /song1'
        msg_reply += '\n \nhttp://www.indieshuffle.com/'
        self.assertReplied(self.bot, msg_reply)
