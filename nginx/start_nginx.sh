#!/bin/sh
envsubst '$DOMAIN_NAME' < /etc/nginx/conf.d/nginx_template.conf > /etc/nginx/conf.d/nginx.conf
rm -f /etc/nginx/conf.d/nginx_template.conf
nginx -g 'daemon off;'
