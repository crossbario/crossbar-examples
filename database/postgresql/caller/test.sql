select crossbar.call('com.example.add2', json_build_array(2, 3)::jsonb);

select max(crossbar.call('com.example.add2', json_build_array(a, a * 2)::jsonb)::text::int)
from generate_series(0,10000) as a;

SELECT current_setting('crossbar.router_url');

SELECT set_config('crossbar.router_url', 'http://127.0.0.1:8080/call', false);

select 10000./(31856./1000.), 10000./(15399./1000.)



select 10000./(15867./1000.)


select max(crossbar.call('com.example.add2', json_build_array(a, a * 2)::jsonb)::text::int)
from generate_series(0,100) as a;


CREATE OR REPLACE FUNCTION http_head (url TEXT)
RETURNS TEXT
LANGUAGE plpythonu
AS
$$
import requests
r = requests.head(url)
return r.status_code
$$;

CREATE OR REPLACE FUNCTION http_get_py (url TEXT)
RETURNS TEXT
LANGUAGE plpythonu
AS
$$
import requests
r = requests.get(url)
return r.text
$$;

CREATE OR REPLACE FUNCTION http_get_len (url TEXT, x INT)
RETURNS INT
LANGUAGE plpgsql
VOLATILE
AS
$$
DECLARE
    l_request   http_request;
    l_response  http_response;
BEGIN
    l_request.method = 'GET';
    l_request.uri := url;
    l_request.headers := ARRAY[http_header('x-foobar', x::text)];
    l_response := http(l_request);
    RETURN length(l_response.content);
END;
$$;

CREATE OR REPLACE FUNCTION http_get_len2 (url TEXT)
RETURNS INT
LANGUAGE plpgsql
VOLATILE
AS
$$
DECLARE
    l_request   http_request;
    l_response  http_response;
BEGIN
    l_request.method = 'GET';
    l_request.uri := url;
    l_response := http(l_request);
    RETURN length(l_response.content);
END;
$$;

SELECT http_get_len('http://127.0.0.1:8080/config');

WITH x AS (SELECT * FROM generate_series(0, 10000) AS val)
SELECT x.val FROM x

WITH x AS (SELECT * FROM generate_series(0, 100000) AS val)
SELECT MAX(http_get_len('http://127.0.0.1:8080/config', x.val)) FROM x

WITH x AS (SELECT * FROM generate_series(0, 100000) AS val)
SELECT MAX(http_get_len('http://127.0.0.1', x.val)) FROM x

WITH x AS (SELECT * FROM generate_series(0, 100000) AS val)
SELECT MAX(http_get_len2('http://127.0.0.1')) FROM x

WITH
x AS (SELECT * FROM generate_series(0, 100000) AS val),
y AS (SELECT content FROM http_get('http://127.0.0.1?x=' || now()::text), x)
--SELECT * FROM y
SELECT MAX(length(content)) FROM y

SELECT * FROM http_get('http://127.0.0.1') AS reqs FULL OUTER JOIN generate_series(0, 10) AS vals;

SELECT MAX(g), MAX(length(resp)) FROM
(
SELECT g, http_get('http://127.0.0.1?x=' || g::text)::text resp FROM generate_series(0, 100000) g
) q


SELECT MAX(g), MAX(length(resp)) FROM
(
SELECT g, http_get('http://127.0.0.1')::text resp FROM generate_series(0, 100000) g
) q



ect 100000./(45406./1000.)

WITH
    x AS (SELECT * FROM generate_series(0, 10000) AS val),
    y AS (SELECT content FROM http_get('http://127.0.0.1'))
SELECT MAX(length(content)) FROM y


select ARRAY[http_header('x-foobar', '23')::http_header]

select http_header('x-foobar', 23)
SELECT MAX(http_head('http://127.0.0.1/')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 10550 ms.

SELECT MAX(http_head('http://127.0.0.1:8080/dummy')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 18233 ms.

SELECT MAX(http_head('http://127.0.0.1:8080/ws')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 29590 ms.


SELECT length(content) FROM http_get('http://127.0.0.1');

SELECT http_get('http://127.0.0.1');

SELECT content FROM http_get('http://127.0.0.1:8080/config');



SELECT MAX(req) FROM http_get_len('http://127.0.0.1:8080/config') AS req, generate_series(0, 10000) AS x;

SELECT MAX(req) FROM (
SELECT x, req FROM http_get_len('http://127.0.0.1:8080/config') AS req, generate_series(0, 10000) AS x) AS s;


SELECT MAX(length(req.content)) FROM http_get('http://127.0.0.1') AS req, generate_series(0, 1000000) AS x;
-- Gesamtlaufzeit der Abfrage: 2308 ms.

SELECT 1000000./(2279./1000.)

SELECT MAX(length(req.content)) FROM http_get('http://127.0.0.1:8080/config') AS req, generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 41833 ms.

SELECT length(http_get('http://127.0.0.1'));

SELECT length(http_get('http://127.0.0.1'));


SELECT MAX(length(http_get_py('http://127.0.0.1'))) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 15476 ms.

SELECT MAX(length(http_get('http://127.0.0.1:8080/ws'))) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 41550 ms.

SELECT MAX(crossbar.call('com.example.add2', json_build_array(x, x * 2)::jsonb)::text::int)
FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 33880 ms.

select
    nginx as "Nginx HTTP/GET",
    crossbar as "Crossbar.io RPC",
    nginx::float/crossbar::float as "Performance Factor"
from
    (select 10000./(15476./1000.) as nginx, 10000./(33880./1000.) as crossbar)
as s
;


-- brummer1 : Crossbar.io <---> brummer2 : PostgreSQL


select length(crossbar.http_get('http://crossbar.io'));

select length(crossbar.http_get('http://127.0.0.1:8080/ws'));


select max(length(crossbar.http_get('http://127.0.0.1:8080/ws'))) from generate_series(0,1000) as a;;





