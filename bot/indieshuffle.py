import tgbot
import requests
from lxml import html


class IndieShuPlugin(tgbot.TGPluginBase):
    def list_commands(self):
        return [
            ('tsong', self.tsong, 'Song of the day!!!!!'),
            ('latest', self.latest, 'Latests songs!'),
            ('popularthisweek', self.popularthisweek, 'Popular this week!'),
            ('popularthismonth', self.popularthismonth, 'Popular this month!'),
        ]

    def tsong(self, tg, message, text):
        r = requests.get('http://www.indieshuffle.com/')
        tree = html.fromstring(r.text)
        song = tree.xpath('//a[starts-with(text(),"SONG OF THE DAY")]//following::div[@class="right_icons"]/a/@href')
        if not song:
            reply = 'not found :('
        else:
            reply = song[0]
        tg.send_message(message.chat.id, reply, reply_to_message_id=message.message_id)

    def latest(self, tg, message, text):
        r = requests.get('http://www.indieshuffle.com/')
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="right_icons"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            tg.send_message(message.chat.id, song)

    def popularthisweek(self, tg, message, text):
        r = requests.get('http://www.indieshuffle.com/popular/week/')
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="right_icons"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            tg.send_message(message.chat.id, song)

    def popularthismonth(self, tg, message, text):
        r = requests.get('http://www.indieshuffle.com/popular/month/')
        tree = html.fromstring(r.text)
        songs = tree.xpath('//div[@class="right_icons"]//following::a[contains(@href, "soundcloud")]/@href')
        for song in songs:
            tg.send_message(message.chat.id, song)
