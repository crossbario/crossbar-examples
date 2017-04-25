FROM crossbario/autobahn-python-armhf

# install component specific dependencies
RUN pip install pyopenssl service_identity netifaces RPi.GPIO Adafruit_LED_Backpack

# copy the component into the image
RUN rm -rf /app/*
COPY ./app /app

# start the component by default
CMD ["python", "-u", "client.py"]
