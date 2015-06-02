Wordpress REST API
------------------

 * [API Reference](http://developer.wordpress.com/docs/api/)


Configure a **REST Remote** in WebMQ with *RPC Base URI*

    http://wordpress.com

and *REST Base URL*

    https://public-api.wordpress.com/rest/v1/

Then perform some RPCs:

    sess.prefix("wp", "http://wordpress.com#");
    sess.call("wp:read", "sites/en.blog.wordpress.com").then(ab.log, ab.log);
    sess.call("wp:read", "sites/en.blog.wordpress.com/posts/7").then(ab.log, ab.log);
    sess.call("wp:read", "sites/en.blog.wordpress.com/posts/7/likes").then(ab.log, ab.log);
    

Flask REST Example
------------------

Configure a **REST Remote** in WebMQ with *RPC Base URI*

    http://example.com/wiki

and *REST Base URL*

    http://127.0.0.1:8005

Start this Flask/REST example

    python __init__.py

and perform some RPCs:

    sess.prefix("wiki", "http://example.com/wiki#");
    sess.call("wiki:read", "articles").then(ab.log, ab.log);
    sess.call("wiki:create", "articles", {'title': 'Foobar', 'text': 'This is an article.'}).then(ab.log, ab.log);
    sess.call("wiki:update", "articles/1ewlme", {'title': 'Foobar', 'text': 'This is an article !!!'}).then(ab.log, ab.log);
    sess.call("wiki:delete", "articles/1ewlme").then(ab.log, ab.log);
    