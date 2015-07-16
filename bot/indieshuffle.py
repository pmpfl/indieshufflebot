import tgbot
import requests
from twx.botapi import ReplyKeyboardMarkup
from lxml import html


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._url = 'http://www.indieshuffle.com'

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!!!!!'),
            ('latest', self.latest, 'Latests songs!'),
            ('popular', self.popular, 'Popular music!'),
            ('popularthisweek', self.popularthisweek, 'Popular this week!'),
            ('popularthismonth', self.popularthismonth, 'Popular this month!'),
        ]

    def tsong(self, bot, message, text):
        r = requests.get(self._url + '/song-of-the-day')
        tree = html.fromstring(r.text)
        song = tree.xpath('//a[starts-with(text(),"SONG OF THE DAY")]//before::/div[@class="right_icons"]/a/@href')
        if not song:
            reply = 'not found :('
        else:
            reply = song[0]
        bot.tg.send_message(message.chat.id, reply , reply_to_message_id=message.message_id)

    def latest(self, bot, message, text):
        r = requests.get(self._url)
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="songMidContent"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            bot.tg.send_message(message.chat.id, song)

    def popular(self, bot, message, text):
        reply_markup = ReplyKeyboardMarkup.create(
            keyboard=[['Week'], ['Month']],
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True)
        rep = bot.tg.send_message(
            message.chat.id,
            'Please select the time: ',
            reply_to_message_id=message.message_id,
            reply_markup=reply_markup
        ).wait()
        self.need_reply(
            self.popular_try, message, out_message=rep, selective=True)

    def popular_try(self, bot, message, text):
        if text == 'Week':
            self.popularthisweek(bot, message, text)
            return
        if text == 'Month':
            self.popularthismonth(bot, message, text)
            return
        bot.tg.send_message(message.chat.id, ':(')

    def popularthisweek(self, bot, message, text):
        r = requests.get(self._url + '/popular/week/')
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="right_icons"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            bot.tg.send_message(message.chat.id, song)

    def popularthismonth(self, bot, message, text):
        r = requests.get(self._url + '/popular/month/')
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="right_icons"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            bot.tg.send_message(message.chat.id, song)
