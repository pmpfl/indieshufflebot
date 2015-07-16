#!/usr/bin/env python
# coding=utf-8

import tgbot
import os
from requests.packages import urllib3
from bot.indieshuffle import IndieShuPlugin

urllib3.disable_warnings()


def main():
    tg = tgbot.TGBot(
        os.environ['TELEGRAM_KEY'],
        plugins=[
            IndieShuPlugin(),
        ]
    )
    tg.print_commands()
    tg.run()

if __name__ == '__main__':
    main()
