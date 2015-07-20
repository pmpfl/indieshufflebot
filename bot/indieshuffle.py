import tgbot
import requests
import os
import json
from twx.botapi import ReplyKeyboardMarkup


def _get_songs(service, count=1, page=1):
    payload = {'key': os.environ['INDIESHUFFLE_KEY'], 'count': count, 'page': page}
    r = requests.get(('http://www.indieshuffle.com/mobile/%s' % service), params=payload)
    parsedjson = json.loads(r.text)
    return parsedjson['posts']


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._genre_keyboard = [['all'], ['electronic'], ['surf-rock'], ['indie-pop'], ['rac'], ['remale-vocalist'], ['covers']]

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!'),
            ('latest', self.latest, 'Latests songs!'),
            ('popular', self.popular, 'Popular music!'),
        ]

    def tsong(self, bot, message, text):
        song = _get_songs('songsoftheday')
        reply = song[0]['url']
        bot.tg.send_message(
            message.chat.id,
            reply,
            reply_to_message_id=message.message_id)

    def latest(self, bot, message, text):
        reply_markup = ReplyKeyboardMarkup.create(
            keyboard=self._genre_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True)
        rep = bot.tg.send_message(
            message.chat.id,
            'Please select the genre: ',
            reply_to_message_id=message.message_id,
            reply_markup=reply_markup
        ).wait()
        self.need_reply(
            self.latest_try, message, out_message=rep, selective=True)

    def latest_try(self, bot, message, text):
        songs = _get_songs('', count=10)
        found = False
        for song in songs:
            if (text == 'All'):
                found = True
                bot.tg.send_message(
                    message.chat.id,
                    song['url'],
                    reply_to_message_id=message.message_id)
                continue
            for tag in song['tags']:
                if text.lower() in tag['slug'].lower():
                    found = True
                    bot.tg.send_message(
                        message.chat.id,
                        song['url'],
                        reply_to_message_id=message.message_id)
                    break
        if not found:
            bot.tg.send_message(
                message.chat.id,
                'not found :(',
                reply_to_message_id=message.message_id)

    def popular(self, bot, message, text):
        reply_markup = ReplyKeyboardMarkup.create(
            keyboard=self._genre_keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True)
        rep = bot.tg.send_message(
            message.chat.id,
            'Please select the genre: ',
            reply_to_message_id=message.message_id,
            reply_markup=reply_markup
        ).wait()
        self.need_reply(
            self.popular_try, message, out_message=rep, selective=True)

    def popular_try(self, bot, message, text):
        songs = _get_songs('track/popular/', count=10)
        found = False
        for song in songs:
            if (text == 'all'):
                found = True
                bot.tg.send_message(
                    message.chat.id,
                    song['url'],
                    reply_to_message_id=message.message_id)
                continue
            for tag in song['tags']:
                if text.lower() in tag['slug'].lower():
                    found = True
                    bot.tg.send_message(
                        message.chat.id,
                        song['url'],
                        reply_to_message_id=message.message_id)
                    break
        if not found:
            bot.tg.send_message(
                message.chat.id,
                'not found :(',
                reply_to_message_id=message.message_id)
