DROP FUNCTION IF EXISTS test2 (JSONB);

CREATE OR REPLACE FUNCTION test2 (p_args JSONB) RETURNS JSONB
LANGUAGE plpythonu
AS
$$
import json
res = json.loads(p_args)
res[0] += 23
return json.dumps(res)
$$;

SELECT test2(json_build_array(2,3)::jsonb)


DROP FUNCTION crossbar.call (TEXT, JSONB, JSONB, JSONB);

CREATE OR REPLACE FUNCTION crossbar.call (p_proc TEXT,
    p_args JSONB DEFAULT NULL, p_kwargs JSONB DEFAULT NULL,
    p_options JSONB DEFAULT NULL)
RETURNS JSONB
LANGUAGE plpythonu
AS
$$
    import requests, json
    payload = {"procedure": p_proc}
    if p_args:
        payload['args'] = json.loads(p_args)
    if p_kwargs:
        payload['kwargs'] = json.loads(p_kwargs)
    headers = {'Content-Type': 'application/json'}
#    r = requests.post("http://127.0.0.1:8080/call", json=payload, headers=headers)
    r = requests.post("http://127.0.0.1:8080/call", data=json.dumps(payload), headers=headers)
#    res = json.loads(r.text)
    res = r.json()
    if ('args' in res and len(res['args']) > 1) or ('kwargs' in res and res['kwargs']):
        pass
    else:
        res = res.get('args', [None])[0]
    return json.dumps(res)
$$;

select max(crossbar.call('com.example.add2', json_build_array(a, a * 2)::jsonb)::text::int)
from generate_series(0,1000) as a;



CREATE OR REPLACE FUNCTION http_head (url TEXT)
RETURNS TEXT
LANGUAGE plpythonu
AS
$$
import requests
r = requests.head(url)
return r.status_code
$$;

CREATE OR REPLACE FUNCTION http_get (url TEXT)
RETURNS TEXT
LANGUAGE plpythonu
AS
$$
import requests
r = requests.get(url)
return r.text
$$;

SELECT MAX(http_head('http://127.0.0.1/')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 10550 ms.

SELECT MAX(http_head('http://127.0.0.1:8080/dummy')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 18233 ms.

SELECT MAX(http_head('http://127.0.0.1:8080/ws')) FROM generate_series(0, 10000) AS x;
-- Gesamtlaufzeit der Abfrage: 29590 ms.


SELECT http_get('http://127.0.0.1');

SELECT length(http_get('http://127.0.0.1'));

SELECT MAX(length(http_get('http://127.0.0.1'))) FROM generate_series(0, 10000) AS x;
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





