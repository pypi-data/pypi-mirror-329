# This file is placed in the Public Domain.


"timer"


from .thread import launch
from .timer  import Timer


class Repeater(Timer):

    def run(self) -> None:
        launch(self.start)
        super().run()


def __dir__():
    return (
        'Repeater',
    )
