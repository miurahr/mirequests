#!/usr/bin/env python

import requests
from . import mirrors
from . import exceptions


__all__ = ['get', 'exceptions']

_blacklist = ['http://mirrors.tuna.tsinghua.edu.cn']


def _in_blacklist(url):
    for b in _blacklist:
        if url.startswith(b):
            return True
    return False


def get(url, stream=False):
    r = requests.get(url, stream=stream, allow_redirects=False)
    if r.status_code == 302:
        # tsinghua.edu.cn is problematic and it prohibit service to specific geo location.
        # we will use another redirected location for that.
        newurl = r.headers['Location']
        if _in_blacklist(newurl):
            mml = mirrors.Metalink(url, blacklist=_blacklist)
            newurl = mml.altlink()
        r = requests.get(newurl, stream=stream)
    return r

