FROM nginx:1.27-alpine

LABEL maintainer="kids-app"
LABEL description="The Little Work Plane English practice page"

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html/index.html
COPY audio/ /usr/share/nginx/html/audio/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
