# Autocomplete Demo

Autocomplete search in 1 Mio. database records.

## Frontend

All the HTML5 assets for the frontend reside in this folder. You can start the demo by opening the `index.html` in your browser.

## Backend

All the Oracle PL/SQL and SQL backend code resides in the `sql` folder.

The schema objects are automatically installed when setting up the Oracle demo schema from the Tavendo WebMQ administration console.

To install manually, you can

	make install

and to uninstall

	make uninstall

This requires the enviroment variable `WEBMQ_ORACLE` to be set, e.g.

	export WEBMQ_ORACLE=webmqdemo/webmqdemo@192.168.56.101/orcl

where

	export WEBMQ_ORACLE=<Schema Name>/<Password>@<Oracle IP or Hostname>/<Oracle SID>

on Unix, and via system configuration dialog on Windows.
