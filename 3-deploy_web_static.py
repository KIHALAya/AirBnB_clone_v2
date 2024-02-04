#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""

from fabric.api import local, env
from os.path import exists
from datetime import datetime
from fabric.operations import run
from fabric.operations import put

env.hosts = ['<IP web-01>', '<IP web-02>']


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


def do_deploy(archive_path):
    """Distribute an archive to web servers"""

    if not exists(archive_path):
        return False

    try:

        put(archive_path, '/tmp/')
        filename = archive_path.split('/')[-1]
        foldername = '/data/web_static/releases/'
        + filename.split('.')[0] + '/'
        run('mkdir -p {}'.format(foldername))
        run('tar -xzf /tmp/{} -C {}'.format(filename, foldername))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(foldername, foldername))
        run('rm -rf {}web_static'.format(foldername))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(foldername))

        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """Create and distribute an archive to web servers"""

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
