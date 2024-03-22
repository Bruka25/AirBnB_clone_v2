#!/usr/bin/python3
"""Python module for creating compressed tar file
   with the archives stored in the folder versions
"""

import os.path
from datetime import datetime
from fabric.api import local


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
