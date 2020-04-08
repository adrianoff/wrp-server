FROM nginx:alpine

RUN apk update && apk add wget && apk add bash && rm -rf /var/cache/apk/*


WORKDIR "/usr/src/wrp-server"

EXPOSE 80
EXPOSE 443