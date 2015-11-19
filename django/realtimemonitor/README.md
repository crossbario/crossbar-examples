Install base requirements.
``` bash
pip install -r requirements.txt
```

On Mac OS X 10.11.1+ add the following:
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography

Generate the db

    python manage.py migrate

Add a superuser

    python manage.py createsuperuser

Start the application in a seperate terminal

    python manage.py runserver 0:800

Start crossbar in a seperate terminal

    crossbar start

Start the client and compare the outcome with the [webpage](http://localhost:8000) at http://localhost:8000

    python client.py

Have fun!

There is also a [tutorial covering this example](http://crossbar.io/docs/Adding-Real-Time-to-Django-Applications/) in the Crossbar.io documentation.
