NAME

::

    nixt - NIXT


SYNOPSIS

::

    >>> from nixt.objects import Object, dumps, loads
    >>> o = Object()
    >>> o.a = "b"
    >>> print(loads(dumps(o))
    {'a': 'b'}


INSTALL

::

    $ pip install nixt


DESCRIPTION

::

    NIXT contains all the python3 code to program objects in a functional
    way. It provides a base Object class that has only dunder methods, all
    methods are factored out into functions with the objects as the first
    argument. It is called Object Programming (OP), OOP without the
    oriented.

    NIXT allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.


COPYRIGHT

::

    NIXT is Public Domain.
