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


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._test_download = {}
        self._emoji_music = u'\U0001F3B5'
        self._emoji_save = u'\U0001F3B4'

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!'),
            ('latest', self.latest, 'Latests songs! <number song default 5>'),
            ('popular', self.popular, 'Popular music! <gender>'),
            ('song', self.song, 'Download song. <id>'),
        ]

    def song(self, bot, message, text):
        url = self._test_download[text]['url']
        if url:
            filename = '%s.mp3' % self._test_download[text]['name']
            bot.tg.send_message(message.chat.id, 'Downloading %s...' % filename)
            mp3_url = requests.get(url, allow_redirects=False).headers.get('location')
            urllib.urlretrieve(mp3_url, filename)
            fp = open(filename, 'rb')
            file_info = InputFileInfo(filename, fp, 'audio/mp3')
            file_input = InputFile('document', file_info)
            bot.tg.send_message(message.chat.id, 'Uploading...')
            bot.tg.send_document(message.chat.id, document=file_input, on_success=self.success_song(filename))
        else:
            bot.tg.send_message(message.chat.id, 'Please provide the music id correct')

    def success_song(self, filename):
        os.remove(filename)
        print 'removed ' + filename

    def tsong(self, bot, message, text):
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        self._test_download[str(song['id'])] = {'url': song['songs'][0]['url'], 'name': song['songs'][0]['title'] }
        msg = '\n \n' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
        msg += '\n \n' + self._emoji_save + ' /song ' + str(song['id'])
        msg += '\n \n' + song['url']
        bot.tg.send_message(message.chat.id, msg)

    def latest(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('', count=num))['posts']
        for song in songs:
            self._test_download[str(song['id'])] = {'url': song['songs'][0]['url'], 'name': song['songs'][0]['title'] }
            msg += '\n \n' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
            msg += '\n \n' + self._emoji_save + ' /song ' + str(song['id']) + '\n \n Tags:'
            for tag in song['tags']:
                msg += ' ' + tag['slug']
            msg += '\n \n' + song['url']
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True)

    def popular(self, bot, message, text):
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('track/popular/', count=num))['posts']
        for song in songs:
            self._test_download[str(song['id'])] = {'url': song['songs'][0]['url'], 'name': song['songs'][0]['title'] }
            msg += '\n \n' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
            msg += '\n \n' + self._emoji_save + ' /song ' + str(song['id']) + '\n \n Tags:'
            for tag in song['tags']:
                msg += ' ' + tag['slug']
            msg += '\n \n' + song['url']
        ret = msg if msg else 'no latest songs'
        bot.tg.send_message(message.chat.id, ret, disable_web_page_preview=True)
