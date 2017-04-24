FROM crossbario/autobahn-python-armhf

RUN pip install pyopenssl service_identity rpi_ws281x

COPY ./app /app

CMD ["python", "-u", "client.py"]
