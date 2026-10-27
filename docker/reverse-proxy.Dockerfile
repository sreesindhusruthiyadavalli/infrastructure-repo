FROM nginx:1.27-alpine

COPY proxy-lab/nginx/default.conf.template /opt/nginx/default.conf.template
COPY proxy-lab/nginx/40-configure-resolver.sh /docker-entrypoint.d/40-configure-resolver.sh

RUN chmod +x /docker-entrypoint.d/40-configure-resolver.sh