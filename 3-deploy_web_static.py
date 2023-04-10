#!/usr/bin/python3
from fabric.api import env
from fabric.api import local
from fabric.api import run 
from fabric.api import put
from datetime import datetime
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
    # get date to create file
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second)

    # if dir is not available, create dir, return None if unsuccessful
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    
    # create the archive file
    if local("tar -czvf {} web_static".format(file)).failed is True:
        return None

    # finally return the file
    return file


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
    if os.path.isfile(archive_path) is False:
        return False

    # get file from path
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # copy file to temp
    if put(archive_path, "/tm/{}".format(file)).failed is True:
        return False

    # remove 
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False

    # remove the temp file
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    # move file and contents
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False

    # return true if all processes check
    return True


def deploy():
    # archive and get the archived file
    file = do_pack()
    if file is None:
        return False
    # deploy the file to server
    return do_deploy(file)
