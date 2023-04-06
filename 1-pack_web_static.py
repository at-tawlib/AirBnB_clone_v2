#!/usr/bin/python3
# generate a .tgz archive from web_static folder contents
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """
    generates a .tgz archive
    return:
        the archive path if archive has been correctly generated
        else return None
    """

    name = strftime("%Y%m%d%H%M%S")
    try:
        # create dir if it does not exist
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/".format(name))

        return "versions/web_static_{}.tgz".format(name)
    except Exception as e:
        return None
