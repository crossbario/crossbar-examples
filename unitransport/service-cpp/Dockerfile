FROM crossbario/autobahn-cpp-gcc

ENV CBURL ws://localhost:8080/ws
ENV CBREALM realm1

COPY app/client /usr/local/app/

RUN /usr/local/app/client
