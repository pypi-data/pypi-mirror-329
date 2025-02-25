# This file is placed in the Public Domain.


"threads"


import queue
import threading
import time
import typing


from .errors import later


class Thread(threading.Thread):

    bork = False

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self.name = thrname
        self.queue = queue.Queue()
        self.result = None
        self.starttime = time.time()
        self.stopped = threading.Event()
        self.queue.put((func, args))

    def run(self) -> None:
        func, args = self.queue.get()
        try:
            self.result = func(*args)
        except Exception as ex:
            if Thread.bork:
                raise ex
            later(ex)
            if args and "ready" in dir(args[0]):
                args[0].ready()

    def join(self, timeout=None) -> typing.Any:
        super().join(timeout)
        return self.result


def launch(func, *args, **kwargs) -> Thread:
    nme = kwargs.get("name", name(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


def name(obj) -> str:
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


def __dir__():
    return (
        'Repeater',
        'Timer',
        'launch'
    )
