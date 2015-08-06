import tgbot
import requests
import os
import urllib
import json
from twx.botapi import InputFileInfo, InputFile, ChatAction
from tgbot import TGCommandBase


def _get_songs(service, count=1, page=1):
    payload = {'key': os.environ['INDIESHUFFLE_KEY'], 'count': count, 'page': page}
    r = requests.get(('http://www.indieshuffle.com/mobile/%s' % service), params=payload)
    return r.text


def _prepare_reply(song):
    emoji_music = u'\U0001F3B5'
    emoji_save = u'\U0001F3B4'
    msg = '\n \n' + emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
    msg += '\n \n' + emoji_save + ' /song' + str(song['id'])
    msg += '\n \n' + song['url']
    return msg


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()

    def list_commands(self):
        return [
            TGCommandBase('tsong', self.tsong, 'Song of the day'),
            TGCommandBase('song', self.song, 'Download song', prefix=True),
            TGCommandBase('latest', self.latest, 'Latests songs!'),
            TGCommandBase('popular', self.latest, 'Latests songs!')
        ]

    def save_song(self, song):
        data = {}
        data['url'] = song['songs'][0]['url']
        data['name'] = song['songs'][0]['title']
        self.save_data(str(song['id']), obj=json.dumps(data))

    def song(self, bot, message, text):
        bot.tg.send_chat_action(message.chat.id, ChatAction.TEXT)
        song = json.loads(self.read_data(text)) if self.read_data(text) else None
        if song is not None:
            path = os.environ['OPENSHIFT_TMP_DIR'] if os.environ['OPENSHIFT_TMP_DIR'] else '/tmp/'
            filename = '%s%s.mp3' % (path, song['name'])
            urllib.urlretrieve(song['url'], filename)
            fp = open(filename, 'rb')
            file_info = InputFileInfo(filename, fp, 'audio/mp3')
            file_input = InputFile('document', file_info)
            bot.tg.send_document(message.chat.id, document=file_input, on_success=self.success_song(filename))
        else:
            bot.tg.send_message(message.chat.id, 'I couldn\'t find your music').wait()

    def success_song(self, filename):
        os.remove(filename)

    def tsong(self, bot, message, text):
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        self.save_song(song)
        msg = _prepare_reply(song)
        bot.tg.send_message(message.chat.id, msg).wait()

    def latest(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True).wait()

    def popular(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('track/popular/', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True).wait()
