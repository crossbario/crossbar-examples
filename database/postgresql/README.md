# Crossbar.io PostgreSQL Bridge Services


## Requirements

PostgreSQL 9.4+ and Crossbar.io 0.13+.


## Installation

When running Crossbar.io under CPython:

    pip install psycopg2 txpostgres

When running Crossbar.io under PyPy:

    pip install psycopg2cffi txpostgres

> See also: [Database Programming with PostgreSQL](http://crossbar.io/docs/Database-Programming-with-PostgreSQL/)


### CALLER Support

Support for the CALLER role (invoking WAMP procedures somewhere from within PostgreSQL) depends on the [PostgreSQL HTTP client](https://github.com/pramsey/pgsql-http) extension.

> Note: You likely will need root access to the machine with the PostgreSQL installation, as installing binary extensions into a PostgreSQL server is a sensitive operation, and managed/hosted PostgreSQL environments often don't allow that.

To build and install, install the cURL development library (which the extension depends upon):

    sudo apt-get install libcurl4-openssl-dev

Make sure you have `pg_config` and `curl-config` on your `PATH`:

```console
oberstet@bvr-sql18:~$ which pg_config
/opt/pg95/bin/pg_config
oberstet@bvr-sql18:~$ which curl-config
/usr/bin/curl-config
oberstet@bvr-sql18:~$
```

Now build and install the extenion:

```console
cd /tmp
git clone https://github.com/pramsey/pgsql-http.git
cd pgsql-http
make
sudo env "PATH=$PATH" make install
```

After that, connect as superuser to the PostgreSQL database where the Crossbar.io bridge is installed and:

```sql
CREATE EXTENSION http;
```

To test the extension:


```console
oberstet@bvr-sql18:~$ psql -d mydb
psql (9.5.0)
Type "help" for help.

adr=> SELECT status, content_type, LENGTH(content) FROM http_get('http://crossbar.io');
 status | content_type | length
--------+--------------+--------
    200 | text/html    |  54765
(1 row)

adr=>
```
