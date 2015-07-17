import tgbot
import requests
from twx.botapi import ReplyKeyboardMarkup
from lxml import html


def _url(append):
    return 'http://www.indieshuffle.com%s' % (append.replace(" ", "-"))


def _send_songs(url, bot, message):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    songs = tree.xpath('//div[@class="songMidContent"]//following::td/div/a/@href')
    for song in songs:
        bot.tg.send_message(
            message.chat.id,
            _url(song),
            reply_to_message_id=message.message_id)


class IndieShuPlugin(tgbot.TGPluginBase):
    def __init__(self):
        super(IndieShuPlugin, self).__init__()
        self._time_keyboard = [['Week'], ['Month']]
        self._genre_keyboard = [['All'], ['Electronic'], ['Indie rock'], ['House'], ['Remixes'], ['Female Vocalist'], ['Ambient'], ['Folk']]

    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!!!!!'),
            ('latest', self.latest, 'Latests songs!'),
            ('popular', self.popular, 'Popular music!'),
            ('popularthisweek', self.popularthisweek, 'Popular this week!'),
            ('popularthismonth', self.popularthismonth, 'Popular this month!'),
        ]

    def tsong(self, bot, message, text):
        r = requests.get(_url('/song-of-the-day'))
        tree = html.fromstring(r.text)
        song = tree.xpath('//a[starts-with(text(),"SONG OF THE DAY")]//following::td/div/a/@href')
        if not song:
            reply = 'not found :('
        else:
            reply = _url(song[0])
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
        url = _url('')
        if text != '' and text != 'All':
            url = _url('/songs/' + text)
        _send_songs(url, bot, message)

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
        bot.tg.send_message(
            message.chat.id,
            ':(',
            reply_to_message_id=message.message_id)

    def popularthisweek(self, bot, message, text):
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
            self.popularthisweek_try, message, out_message=rep, selective=True)

    def popularthisweek_try(self, bot, message, text):
        url = _url('/popular/week/')
        if text != '' and text != 'All':
            url = _url('/popular/week/' + text)
        _send_songs(url, bot, message)

    def popularthismonth(self, bot, message, text):
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
            self.popularthismonth_try, message, out_message=rep, selective=True)

    def popularthismonth_try(self, bot, message, text):
        url = _url('/popular/month/')
        if text != '' and text != 'All':
            url = _url('/popular/month/' + text)
        _send_songs(url, bot, message)
