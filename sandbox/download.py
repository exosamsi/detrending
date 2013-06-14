#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import gevent
from gevent import monkey
monkey.patch_all()

import os
import glob
import logging
# logging.basicConfig(level=logging.INFO)
import kplr
import requests

client = kplr.API()
KPLR_DATA_DIR = os.environ.get("KPLR_DATA_DIR")


def _do_fetch(d, grp):
    local = os.path.join(grp, d._filename)
    if os.path.exists(local):
        return

    r = requests.get(d.url)
    if r.status_code != requests.codes.ok:
        return

    logging.info("Saving: '{0}'".format(local))
    with open(local, "wb") as f:
        f.write(r.content)


def get_lightcurves(kepid, grp):
    d = os.path.join(KPLR_DATA_DIR, "sandbox1", grp, kepid)
    try:
        os.makedirs(d)
    except os.error:
        pass
    star = client.star(kepid)
    jobs = [gevent.spawn(_do_fetch, ds, d) for ds in star.data]
    gevent.joinall(jobs)


if __name__ == "__main__":
    for f in glob.glob("specs/*systematicsIds.txt"):
        grp = f[:-7]
        print("Group: {0}".format(grp))
        for i in open(f):
            print(i.strip())
            get_lightcurves(i.strip(), grp)
