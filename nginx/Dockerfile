FROM nginx:1.26-alpine3.19

RUN apk add --no-cache gettext \
    && rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/nginx_template.conf
COPY start_nginx.sh /start_nginx.sh

RUN chmod +x /start_nginx.sh

CMD ["/start_nginx.sh"]
