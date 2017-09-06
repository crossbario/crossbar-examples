FROM crossbario/crossbar-fabric:latest

RUN apt-get install nodejs npm nodejs-legacy

ENV DEBIAN_FRONTEND noninteractive

RUN    apk --update upgrade \
    && apk add nodejs npm nodejs-legacy \
    && apk del .build-deps
