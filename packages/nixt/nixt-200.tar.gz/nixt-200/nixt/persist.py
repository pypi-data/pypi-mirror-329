# This file is placed in the Public Domain.


"disk persistence"


import datetime
import os
import json
import pathlib
import threading
import typing


from .objects import dumps, fqn, loads, update


p    = os.path.join
lock = threading.RLock()


class DecodeError(Exception):

    pass


class Cache:

    objs = {}

    @staticmethod
    def add(path, obj) -> None:
        Cache.objs[path] = obj

    @staticmethod
    def get(path) -> typing.Any:
        return Cache.objs.get(path, None)

    @staticmethod
    def typed(matcher) -> [typing.Any]:
        for key in Cache.objs:
            if matcher not in key:
                continue
            yield Cache.objs.get(key)


def cdir(pth) -> None:
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def ident(obj) -> str:
    return p(fqn(obj),*str(datetime.datetime.now()).split())


def read(obj, pth):
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            try:
                obj2 = loads(ofile.read())
                update(obj, obj2)
            except json.decoder.JSONDecodeError as ex:
                raise DecodeError(pth) from ex
    return pth


def write(obj, pth):
    with lock:
        cdir(pth)
        txt = dumps(obj, indent=4)
        Cache.objs[pth] = obj
        with open(pth, 'w', encoding='utf-8') as ofile:
            ofile.write(txt)
    return pth


def __dir__():
    return (
        'Cache',
        'DecodeError',
        'cdir',
        'read',
        'write'
    )
