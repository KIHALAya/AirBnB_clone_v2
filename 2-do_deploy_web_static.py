#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']


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

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
