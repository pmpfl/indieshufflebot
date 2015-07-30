import tgbot

import requests
import os
import urllib
import json
from twx.botapi import InputFileInfo, InputFile


def _get_songs(service, count=1, page=1):
    payload = {'key': os.environ['INDIESHUFFLE_KEY'], 'count': count, 'page': page}
    r = requests.get(('http://www.indieshuffle.com/mobile/%s' % service), params=payload)
    return r.text


def _prepare_reply(song):
    emoji_music = u'\U0001F3B5'
    emoji_save = u'\U0001F3B4'
    msg = '\n \n' + emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
    msg += '\n \n' + emoji_save + ' /song ' + str(song['id']) + '\n \n Tags:'
    for tag in song['tags']:
        msg += ' ' + tag['slug']
    msg += '\n \n' + song['url']
    return msg


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._test_download = {}
        self._tsong = ''

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!'),
            ('latest', self.latest, 'Latests songs!'),
            ('popular', self.popular, 'Popular music!'),
            ('song', self.song, 'Download song. <id>'),
        ]

    def song(self, bot, message, text):
        url = self._test_download[text]['url'] if text in self._test_download.keys() else ''
        if url:
            filename = '%s.mp3' % self._test_download[text]['name']
            # change it to save db
            bot.tg.send_message(message.chat.id, 'Downloading %s...' % filename)
            urllib.urlretrieve(url, filename)
            fp = open(filename, 'rb')
            file_info = InputFileInfo(filename, fp, 'audio/mp3')
            file_input = InputFile('document', file_info)
            bot.tg.send_document(message.chat.id, document=file_input, on_success=self.success_song(filename))
        else:
            bot.tg.send_message(message.chat.id, 'Please provide the music id correct')

    def success_song(self, filename):
        os.remove(filename)
        print 'removed ' + filename

    def tsong(self, bot, message, text):
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        self.save_song(song)
        msg = _prepare_reply(song)
        bot.tg.send_message(message.chat.id, msg)

    def latest(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True)

    def popular(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('track/popular/', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True)

    def save_song(self, song):
        self._test_download[str(song['id'])] = {'url': song['songs'][0]['url'], 'name': song['songs'][0]['title']}

    def alertsong(self, bot, message, text):
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        msg = 'Heyyy \n The song of day is: \n'
        if song[id] != self._tsong:
            msg = _prepare_reply(song)
            bot.tg.send_message(message.chat.id, msg, disable_web_page_preview=True)
