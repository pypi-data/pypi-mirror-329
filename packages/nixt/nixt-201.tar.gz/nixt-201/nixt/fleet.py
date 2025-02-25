# This file is placed in the Public Domain.


"list of bots"


class Fleet:

    bots = {}

    @staticmethod
    def add(bot) -> None:
        Fleet.bots[repr(bot)] = bot

    @staticmethod
    def announce(txt) -> None:
        for bot in Fleet.bots.values():
            bot.announce(txt)

    @staticmethod
    def display(evt) -> None:
        for tme in sorted(evt.result):
            text = evt.result[tme]
            Fleet.say(evt.orig, evt.channel, text)

    @staticmethod
    def first() -> None:
        bots =  list(Fleet.bots.values())
        res = None
        if bots:
            res = bots[0]
        return res

    @staticmethod
    def get(orig) -> None:
        return Fleet.bots.get(orig, None)

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Fleet.get(orig)
        if bot:
            bot.say(channel, txt)

    @staticmethod
    def wait() -> None:
        for bot in Fleet.bots.values():
            if "wait" in dir(bot):
                bot.wait()


def __dir__():
    return (
        'Fleet',
    )
