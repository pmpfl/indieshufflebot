import tgbot
import requests
import os
import json
from twx.botapi import ReplyKeyboardMarkup


def _get_songs(service, count=1, page=1):
    payload = {'key': os.environ['INDIESHUFFLE_KEY'], 'count': count, 'page': page}
    r = requests.get(('http://www.indieshuffle.com/mobile/%s' % service), params=payload)
    return r.text


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._emoji_music = u'\U0001F3B5'
        self._emoji_save = u'\U0001F3B4'
        self._genre_keyboard = [['all'], ['electronic'], ['surf-rock'], ['indie-pop'], ['rac'], ['remale-vocalist'], ['covers']]

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!'),
            ('latest', self.latest, 'Latests songs! <gender>'),
            ('popular', self.popular, 'Popular music! <gender>'),
        ]

    def tsong(self, bot, message, text):
        song = json.loads(_get_songs('songsoftheday'))['posts'][0]
        msg = '\n ' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist'] + '\n \n' + song['url']
        bot.tg.send_message(message.chat.id, msg)

    def latest(self, bot, message, text):
        if text:
            songs = json.loads(_get_songs('', count=5))['posts']
            msg = ''
            for song in songs:
                if (text == 'all'):
                    msg += '\n ' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist'] + '\n'
                    #msg += '\n ' + self._emoji_save + ' - /song ' + str(song['id']) + '\n'
                    msg += song['url'] + '\n'
                    continue
                for tag in song['tags']:
                    if text.lower() in tag['slug'].lower():
                        msg += '\n ' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist'] + '\n'
                        break
            bot.tg.send_message(message.chat.id, msg, disable_web_page_preview=True)
        else:
            reply_markup = ReplyKeyboardMarkup.create(
                keyboard=self._genre_keyboard,
                resize_keyboard=True,
                one_time_keyboard=True)
            rep = bot.tg.send_message(
                message.chat.id,
                'Please select the genre: ',
                reply_to_message_id=message.message_id,
                reply_markup=reply_markup
            ).wait()
            self.need_reply(self.latest, message, out_message=rep, selective=True)

    def popular(self, bot, message, text):
        if text:
            songs = json.loads(_get_songs('track/popular/', count=5))['posts']
            msg = ''
            for song in songs:
                if (text == 'all'):
                    msg += '\n ' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist'] + '\n'
                    msg += song['url'] + '\n'
                    continue
                for tag in song['tags']:
                    if text.lower() in tag['slug'].lower():
                        msg += '\n ' + self._emoji_music + ' ' + song['sub_title'] + ' by ' + song['artist'] + '\n'
                        msg += song['url'] + '\n'
                        break
            bot.tg.send_message(message.chat.id, msg, disable_web_page_preview=True)
        else:
            reply_markup = ReplyKeyboardMarkup.create(
                keyboard=self._genre_keyboard,
                resize_keyboard=True,
                one_time_keyboard=True)
            rep = bot.tg.send_message(
                message.chat.id,
                'Please select the genre: ',
                reply_to_message_id=message.message_id,
                reply_markup=reply_markup
            ).wait()
            self.need_reply(
                self.popular, message, out_message=rep, selective=True)
