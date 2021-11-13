# this file resides in a folder called nginx which is a child of DJango (project root folder)
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY ./static /usr/share/nginx/html/static