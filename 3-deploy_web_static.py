#!/usr/bin/python3
"""Fabric script for the full deployment of the archive
   to the servers
"""
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["34.229.189.65", "100.26.166.148"]


def do_pack():
    """Function for creating compressed zipped file"""
    date = datetime.utcnow()
    tar_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                             date.month,
                                                             date.day,
                                                             date.hour,
                                                             date.minute,
                                                             date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return tar_file


def do_deploy(archive_path):
    """Function that distributes an archive to
       the server
       archive_path: File path to the archive
                     files
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
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
    return True


def deploy():
    """Function for the full deployment to a web server"""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
