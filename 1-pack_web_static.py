#!/usr/bin/env python3
"""Fabric script to generate a .tgz archive from the contents of web_static"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Create a compressed archive of web_static"""

    local("mkdir -p versions")

    now = datetime.utcnow()
    archive_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None
