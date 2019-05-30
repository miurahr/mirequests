#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ElementTree


_default_blacklist = ['http://mirrors.tuna.tsinghua.edu.cn']


class Metalink:
    '''Download .meta4 metalink version4 xml file and parse it.'''

    def __init__(self, url, candidate=None):
        self.mirrors = {}
        self.url = url
        self.candidate = candidate
        m = requests.get(url + '.meta4')
        mirror_xml = ElementTree.fromstring(m.text)
        for f in mirror_xml.iter("{urn:ietf:params:xml:ns:metalink}file"):
            for u in f.iter("{urn:ietf:params:xml:ns:metalink}url"):
                pri = u.attrib['priority']
                self.mirrors[pri] = u.text

    def altlink(self, priority=None, blacklist=None):
        if len(self.mirrors) == 0:
            # no alternative
            if self.candidate is not None:
                return self.candidate
            else:
                return self.url
        if priority is None:
            if blacklist is not None:
                for ind in range(len(self.mirrors)):
                    mirror = self.mirrors[str(ind + 1)]
                    if mirror in blacklist:
                        continue
                    return mirror
            else:
                for ind in range(len(self.mirrors)):
                    mirror = self.mirrors[str(ind + 1)]
                    if mirror == self.candidate:
                        continue
                    return mirror
        else:
            return self.mirrors[str(priority)]


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
