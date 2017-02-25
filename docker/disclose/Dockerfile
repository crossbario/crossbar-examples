FROM crossbario/crossbar

# scratch the example node directory contained in the image
RUN rm -rf /node

# copy over our own node directory from the host into the image
COPY ./crossbar/ /node/
RUN chown -R crossbar:crossbar /node
