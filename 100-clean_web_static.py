#!/usr/bin/env bash
"""Fabric script to remove outdated versions
   on the AirBnB clone
"""
import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
import time

env.hosts = ["34.229.189.65", "100.26.166.148"]


def do_pack():
    timestr = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(timestr))
        return ("versions/web_static_{}.tgz".format(timestr))
    except FabricException:
        # Handle Fabric-related exceptions
        return None
    except OSError:
        # Handle file operation-related exceptions
        return None


def do_deploy(archive_path):
    """ Function for the deployment of archives to the
        server
    """
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        new_comp = archive_path.split("/")[-1]
        new_folder = ("/data/web_static/releases/" + new_comp.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_folder))
        run("sudo tar -xzf /tmp/{} -C {}".
            format(new_comp, new_folder))
        run("sudo rm /tmp/{}".format(new_comp))
        run("sudo mv {}/web_static/* {}/".format(new_folder, new_folder))
        run("sudo rm -rf {}/web_static".format(new_folder))
        run('sudo rm -rf /data/web_static/current')
        run("sudo ln -s {} /data/web_static/current".format(new_folder))
        return True
    except FabricException:
        # Handle Fabric-related exceptions
        return False
    except OSError:
        # Handle file operation-related exceptions
        return False


def deploy():
    """Function to deploy"""
    try:
        archive_address = do_pack()
        val = do_deploy(archive_address)
        return val
    except FabricException:
        # Handle Fabric-related exceptions
        return False
    except OSError:
        # Handle file operation-related exceptions
        return False


def do_clean(number=0):
    """Function to remove old archives"""
    if number == 0 or number == 1:
        with cd.local('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +1 | xargs -d '\n' rm -rf")
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +1 | xargs -d '\n' rm -rf")
    else:
        with cd.local('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +{} | xargs -d '\n' rm -rf".format(number))
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +{} | xargs -d '\n' rm -rf".format(number))
