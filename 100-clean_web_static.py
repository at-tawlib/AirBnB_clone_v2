#!/usr/bin/python3
import os
from fabric.api import *
"""
Script to delete out of date archives
"""

env.hosts = ['35.175.105.33', '52.86.214.98']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    Args:
        number(int) : number of archives to keep
    """
    number = 1 if int(number) == 0 else int(number)

    # sort archives
    archives = sorted(os.listdir("versions"))

    # start deleting old archives
    for i in range(number):
        archives.pop()

    with lcd("versions"):
        for archive in archives:
            local("rm ./{}".format(archive))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [x for x in archives if "web_static_" in x]
        for i in range(number):
            archives.pop()

        for archive in archives:
            run("rm -rf ./{}".format(archive))
