#!/usr/bin/python3
from fabric.api import *
from time import strftime
from datetime import date, datetime
from os import path

env.hosts = ['35.175.105.33', '52.86.214.98']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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

        # extract only file name
        file = archive_path.split("/")[-1]
        file_name = file.split(".")[0]

        # upload the file to the /tmp/ directory of the server
        put(archive_path, '/tmp/{}'.format(file))

        run("rm -rf /data/web_static/releases/{}/".format(file_name))

        # get timestamp and use to create target dir
        timestamp = archive_path[-18:-4]
        run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(file_name))

        # Uncompress the archive
        run('sudo tar -xzf  /tmp/{} -C \
/data/web_static/releases/{}/'
            .format(file, file_name))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(file))

        # move contents to the host
        run("sudo mv /data/web_static/releases/{}/web_static/* \
                /data/web_static/releases/{}/"
            .format(file_name, file_name))

        # delete useless dirs
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name))

        # Delete the symbolic link from the web server
        run("sudo rm -rf /data/web_static/current")

        # create new symbolic link on the web server
        run("sudo ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(file_name))
    except Exception:
        return False

    # return after everything runs successfully
    return True


def deploy():
    # archive and get the archived file
    file = do_pack()
    if file is None:
        return False
    # deploy the file to server
    return do_deploy(file)
