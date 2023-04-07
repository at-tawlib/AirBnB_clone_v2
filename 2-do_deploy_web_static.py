#!/usr/bin/python3
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['35.175.105.33', '52.86.214.98']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes an archive to webservers
    Arguments:
        archive_path: path of the archive file
    Return:
        False if file does not exist at path
        True if all operations have been done
    """
    # check if file exists
    try:
        if not (path.exists(archive_path)):
            return False

        # upload the archive to the /tmp/ directory of the server
        put(archive_path, '/tmp/')

        # get timestamp and use to create target dir
        timestamp = archive_path[-18:-4]
        run("sudo mkdir -p /data/web_static/releases/web_static_{}/"
            .format(timestamp))

        # Uncompress the archive
        run('sudo tar -xzf  /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}'
            .format(timestamp, timestamp))

        # Delete the archive from the web server
        run("sudo rm /tmp/web_static_{}.tgz".format(timestamp))

        # move contents to the host
        run("sudo mv /data/web_static/releases/web_static_{}/web_static/* \
                /data/web_static/releases/web_static_{}"
            .format(timestamp, timestamp))

        # delete useless dirs
        run("sudo rm -rf /data/web_static/releases/web_static_{}/web_static"
            .format(timestamp))

        # Delete the symbolic link from the web server
        run("sudo rm -rf /data/web_static/current")

        # create new symbolic link on the web server
        run("sudo ln -s /data/web_static/releases/web_static_{}/ \
            /data/web_static/current".format(timestamp))
    except Exception:
        return False

    # return after everything runs successfully
    return True
