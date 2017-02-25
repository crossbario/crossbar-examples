FROM crossbario/crossbar

# copy over our own node directory from the host into the image
# set user "root" before copy and change owner afterwards
USER root
COPY ./crossbar /mynode
RUN chown -R crossbar:crossbar /mynode

ENTRYPOINT ["crossbar", "start", "--cbdir", "/mynode/.crossbar"]
