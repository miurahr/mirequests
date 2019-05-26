#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ElementTree


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
