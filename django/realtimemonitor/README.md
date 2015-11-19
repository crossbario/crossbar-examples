Install base requirements.
``` bash
pip install -r requirements.txt
```

On Mac OS X 10.11.1+ add the following:
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography


Note: The SQLite database file `db.sqlite3` here is needed (for now), since it is preinitialized with necessary database tables already.

There is also a [tutorial covering this example](http://crossbar.io/docs/Adding-Real-Time-to-Django-Applications/) in the Crossbar.io documentation.
