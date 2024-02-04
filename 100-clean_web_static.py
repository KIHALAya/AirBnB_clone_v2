#!/usr/bin/python3
"""Fabric script to delete out-of-date archives"""

from fabric.api import local, env, run
from fabric.operations import lcd, cd

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """Delete out-of-date archives"""

    number = int(number)
    if number < 0:
        return

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))
