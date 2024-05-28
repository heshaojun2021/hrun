FROM nginx:alpine

COPY ./static/ /usr/share/nginx/html/static/
COPY ./dist/ /usr/share/nginx/html/dist/
COPY ./default.conf /etc/nginx/conf.d/

VOLUME /var/log/
EXPOSE 80 81
