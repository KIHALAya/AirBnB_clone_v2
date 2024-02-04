#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

if ! command -v nginx &> /dev/null
then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "/^location \/hbnb_static\/ {/a\        alias /data/web_static/current/;" /etc/nginx/sites-available/default
sudo service nginx restart
exit 0
