# EditForm and GridFilter Demos

KnockoutJS and ExtJS based demos which show functionality often found in line-of-business applications.

## EditForm

A simple editable Form with Oracle backend that synchronizes in real-time.

## GridFilter

A grid view that allows to filter a dataset on Oracle backend.

## Frontend

All the HTML5 assets for the frontend resides in `knockout` and `extjs` folders. You can start a demo by opening the `index.html` in your browser.

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

## TODO

Implement a version based on [Slickgrid](https://github.com/mleibman/SlickGrid) and themed with [jQUIT](http://jquit.com/).
