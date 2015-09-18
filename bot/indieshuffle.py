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


def _prepare_reply(song, title=''):
    emoji_music = u'\U0001F3B5'
    emoji_save = u'\U0001F3B4'
    msg = title
    msg += '\n \n' + emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist']
    msg += '\n \n' + emoji_save + ' /song' + str(song['id'])
    msg += '\n \n' + song['url']
    return msg


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self.alert_tsong_key = 'TSONGALERT'
        self.alert_latest_key = 'LASTESTALERT'

    def list_commands(self):
        return [
            TGCommandBase('tsong', self.tsong, 'Song of the day'),
            TGCommandBase('song', self.song, 'Download song', prefix=True),
            TGCommandBase('alerttsongon', self.alerttsongon, 'Turn on alert todays song alert'),
            TGCommandBase('alerttsongoff', self.alerttsongoff, 'Turn off  alert todays song alert'),
            TGCommandBase('alertlateston', self.alertlateston, 'Turn on latest song alert',),
            TGCommandBase('alertlatestoff', self.alertlatestoff, 'Turn off latest song alert',),
            TGCommandBase('latest', self.latest, 'Latests songs!'),
            TGCommandBase('popular', self.latest, 'Latests songs!')
        ]

    def save_song(self, song):
        try:
            data = {}
            data['url'] = song['songs'][0]['url']
            data['name'] = song['songs'][0]['title']
            self.save_data(str(song['id']), obj=json.dumps(data))
        except:
            print "Error on save_song"

    def song(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        bot.send_chat_action(message.chat.id, ChatAction.TEXT)
        song = json.loads(self.read_data(text)) if self.read_data(text) else None
        if song is not None:
            path = os.environ['OPENSHIFT_TMP_DIR'] if os.environ['OPENSHIFT_TMP_DIR'] else '/tmp/'
            filename = '%s%s.mp3' % (path, song['name'])
            urllib.urlretrieve(song['url'], filename)
            fp = open(filename, 'rb')
            file_info = InputFileInfo(filename, fp, 'audio/mp3')
            file_input = InputFile('document', file_info)
            bot.send_document(message.chat.id, document=file_input, on_success=self.success_song(filename))
        else:
            bot.send_message(message.chat.id, 'I couldn\'t find your music').wait()

    def alerttsongon(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, self.alert_tsong_key, obj=True)
        bot.send_message(message.chat.id, '/alerttsongoff to trun it off')

    def alerttsongoff(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, self.alert_tsong_key, obj=False)
        bot.send_message(message.chat.id, '/alerttsongon to trun it off')

    def alertlateston(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, self.alert_latest_key, obj=True)
        bot.send_message(message.chat.id, '/alertlatestoff to trun it off')

    def alertlatestoff(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        self.save_data(message.chat.id, self.alert_latest_key, obj=False)
        bot.send_message(message.chat.id, '/alertlateston to trun it off')

    def success_song(self, filename):
        os.remove(filename)

    def tsong(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        self.save_song(song)
        msg = _prepare_reply(song)
        bot.send_message(message.chat.id, msg).wait()

    def latest(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.send_message(message.chat.id, ret, disable_web_page_preview=True).wait()

    def popular(self, bot, message, text):
        self.save_data("user", key2=message.chat.id, obj=message.chat.id)
        msg = ''
        num = text if text else '5'
        songs = json.loads(_get_songs('track/popular/', count=num))['posts']
        for song in songs:
            self.save_song(song)
            msg += _prepare_reply(song)
        ret = msg if msg else 'no latest songs'
        bot.send_message(message.chat.id, ret, disable_web_page_preview=True).wait()

    def cron_go(self, bot, action, param):
        print action
        if action == 'indie.alertsong':
            self._cron_alertsong(bot)

    def _send_to_users(self, bot, name, song, type):
        msg = _prepare_reply(song, name)
        for chat in self.iter_data_key_keys(key1="user"):
            if self.read_data(chat, type):
                bot.send_message(chat, msg).wait()

    def _cron_alertsong(self, bot):
        tsong = json.loads(_get_songs('songsoftheday'))['posts'][0]
        lsongs = json.loads(_get_songs('', count=2))['posts']
        lsong = lsongs[1]
        print tsong['id']
        print lsong['id']
        print lsongs[1]['id']
        if tsong['id'] == lsong['id']:
            lsong = lsongs[1]
        tsongdb = self.read_data("tosong")
        if tsongdb != tsong['id']:
            self.save_data("tosong", obj=tsong['id'])
            self.save_song(tsong)
            self._send_to_users(bot, "SONG OF THE DAY!", tsong, self.alert_tsong_key)
        lsongdb = self.read_data("lasong")
        print lsongdb
        if lsongdb != lsong['id']:
            self.save_data("lasong", obj=lsong['id'])
            self.save_song(lsong)
            self._send_to_users(bot, "NEW SONG ADDED!", lsong, self.alert_latest_key)
