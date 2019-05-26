#!/usr/bin/env python

import requests
from . import mirrors
from . import exceptions


__all__ = ['get', 'exceptions']

_default_blacklist = ['http://mirrors.tuna.tsinghua.edu.cn']


def _in_blacklist(url, blacklist=None):
    if blacklist is None:
        blacklist = _default_blacklist
    for b in blacklist:
        if url.startswith(b):
            return True
    return False


def get(url, params=None, blacklist=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    original_allow_redirects = kwargs['allow_redirects']
    kwargs['allow_redirects'] = False
    r = requests.request('get', url, params=params, **kwargs)
    if not original_allow_redirects:
        return r
    if r.status_code == 302:
        # tsinghua.edu.cn is problematic and it prohibit service to specific geo location.
        # we will use another redirected location for that.
        newurl = r.headers['Location']
        if _in_blacklist(newurl, blacklist):
            mml = mirrors.Metalink(url, blacklist=blacklist)
            newurl = mml.altlink()
        kwargs['allow_redirects'] = True
        r = requests.request('get', newurl, params=params, **kwargs)
    return r

