# Use an official Nginx image based on Alpine
FROM nginx:1.26-alpine

# install netcat
RUN apk add --no-cache netcat-openbsd

## logrotate stuff
RUN apk --no-cache add logrotate
COPY ./docker/nginx/logrotate.conf /etc/logrotate.d/nginx
RUN echo "0 0 * * * /usr/sbin/logrotate /etc/logrotate.d/nginx" >> /etc/crontabs/root

# Copy the entrypoint script
COPY ./docker/nginx/entrypoint.sh--generated /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
