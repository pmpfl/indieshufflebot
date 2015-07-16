#!/usr/bin/env python
# coding=utf-8

import tgbot
import config
from requests.packages import urllib3
from bot.indieshuffle import IndieShuPlugin

urllib3.disable_warnings()


def main():
    tg = tgbot.TGBot(
        config.telegramkey,
        plugins=[
            IndieShuPlugin(),
        ]
    )
    tg.print_commands()
    tg.run()

if __name__ == '__main__':
    main()
