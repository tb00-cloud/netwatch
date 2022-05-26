#! /bin/bash

echo "starting Nginx"
nginx -c /etc/nginx/customnginx.conf  

echo "starting Backend"
python3 -m backend