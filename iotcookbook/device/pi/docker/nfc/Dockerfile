FROM crossbario/autobahn-python-armhf

# install component specific dependencies
RUN pip install pyopenssl service_identity rpi_ws281x

# copy the component into the image
RUN rm -rf /app/*
COPY ./app /app

# start the component by default
CMD ["python", "-u", "client.py"]
