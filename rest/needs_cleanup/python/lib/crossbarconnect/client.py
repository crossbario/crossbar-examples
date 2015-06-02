###############################################################################
##
##  Copyright (C) 2012-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

__all__ = ['Client']

try:
   import ssl
   _HAS_SSL = True
except ImportError:
   _HAS_SSL = False

import sys

_HAS_SSL_CLIENT_CONTEXT = sys.version_info >= (2,7,9)

import json
import hmac
import hashlib
import base64
import random
from datetime import datetime

import six
from six.moves.urllib import parse
from six.moves.http_client import HTTPConnection, HTTPSConnection



def _utcnow():
   """
   Get current time in UTC as ISO 8601 string.

   :returns str -- Current time as string in ISO 8601 format.
   """
   now = datetime.utcnow()
   return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"



def _parse_url(url):
   """
   Parses a Crossbar.io HTTP bridge URL.
   """
   parsed = parse.urlparse(url)
   if parsed.scheme not in ["http", "https"]:
      raise Exception("invalid Push URL scheme '%s'" % parsed.scheme)
   if parsed.port is None or parsed.port == "":
      if parsed.scheme == "http":
         port = 80
      elif parsed.scheme == "https":
         port = 443
      else:
         raise Exception("logic error")
   else:
      port = int(parsed.port)
   if parsed.fragment is not None and parsed.fragment != "":
      raise Exception("invalid Push URL: non-empty fragment '%s" % parsed.fragment)
   if parsed.query is not None and parsed.query != "":
      raise Exception("invalid Push URL: non-empty query string '%s" % parsed.query)
   if parsed.path is not None and parsed.path != "":
      ppath = parsed.path
      path = parse.unquote(ppath)
   else:
      ppath = "/"
      path = ppath
   return {'secure': parsed.scheme == "https",
           'host': parsed.hostname,
           'port': port,
           'path': path}



class Client:
   """
   Crossbar.io HTTP bridge client.
   """

   def __init__(self, url, key = None, secret = None, timeout = 5, context = None):
      """
      Create a new Crossbar.io push client.

      The only mandatory argument is the Push service endpoint of the Crossbar.io
      instance to push to.

      For signed pushes, provide authentication key and secret. If those are not
      given, unsigned pushes are performed.

      :param url: URL of the HTTP bridge of Crossbar.io (e.g. http://example.com:8080/push).
      :type url: str
      :param key: Optional key to use for signing requests.
      :type key: str
      :param secret: When using signed request, the secret corresponding to key.
      :type secret: str
      :param timeout: Timeout for requests.
      :type timeout: int
      :param context: If the HTTP bridge is running on HTTPS (that is securely over TLS),
         then the context provides the SSL settings the client should use (e.g. the
         certificate chain against which to verify the server certificate). This parameter
         is only available on Python 2.7.9+ and Python 3 (otherwise the parameter is silently
         ignored!). See: https://docs.python.org/2/library/ssl.html#ssl.SSLContext
      :type context: obj or None
      """
      if six.PY2:
         if type(url) == str:
            url = six.u(url)
         if type(key) == str:
            key = six.u(key)
         if type(secret) == str:
            secret = six.u(secret)

      assert(type(url) == six.text_type)
      assert((key and secret) or (not key and not secret))
      assert(key is None or type(key) == six.text_type)
      assert(secret is None or type(secret) == six.text_type)
      assert(type(timeout) == int)
      if _HAS_SSL and _HAS_SSL_CLIENT_CONTEXT:
         assert(context is None or isinstance(context, ssl.SSLContext))

      self._seq = 1
      self._key = key
      self._secret = secret

      self._endpoint = _parse_url(url)
      self._endpoint['headers'] = {
         "Content-type": "application/json",
         "User-agent": "crossbarconnect-python"
      }

      if self._endpoint['secure']:
         if not _HAS_SSL:
            raise Exception("Bridge URL is using HTTPS, but Python SSL module is missing")
         if _HAS_SSL_CLIENT_CONTEXT:
            self._connection = HTTPSConnection(self._endpoint['host'],
                  self._endpoint['port'], timeout = timeout, context = context)
         else:
            self._connection = HTTPSConnection(self._endpoint['host'],
                  self._endpoint['port'], timeout = timeout)
      else:
         self._connection = HTTPConnection(self._endpoint['host'],
               self._endpoint['port'], timeout = timeout)




   def publish(self, topic, *args, **kwargs):
      """
      Publish an event to subscribers on specified topic via Crossbar.io HTTP bridge.

      The event payload (positional and keyword) can be of any type that can be
      serialized to JSON.

      If `kwargs` contains an `options` attribute, this is expected to
      be a dictionary with the following possible parameters:

       * `exclude`: A list of WAMP session IDs to exclude from receivers.
       * `eligible`: A list of WAMP session IDs eligible as receivers.

      :param topic: Topic to push to.
      :type topic: str
      :param args: Arbitrary application payload for the event (positional arguments).
      :type args: list
      :param kwargs: Arbitrary application payload for the event (keyword arguments).
      :type kwargs: dict

      :returns int -- The event publication ID assigned by the broker.
      """
      if six.PY2 and type(topic) == str:
         topic = six.u(topic)
      assert(type(topic) == six.text_type)

      ## this will get filled and later serialized into HTTP/POST body
      ##
      event = {
         'topic': topic
      }

      if 'options' in kwargs:
         event['options'] = kwargs.pop('options')
         assert(type(event['options']) == dict)

      if args:
         event['args'] = args

      if kwargs:
         event['kwargs'] = kwargs

      try:
         body = json.dumps(event, separators = (',',':'))
         if six.PY3:
            body = body.encode('utf8')

      except Exception as e:
         raise Exception("invalid event payload - not JSON serializable: {0}".format(e))

      params = {
         'timestamp': _utcnow(),
         'seq': self._seq,
      }

      if self._key:
         ## if the request is to be signed, create extra fields and signature
         params['key'] = self._key
         params['nonce'] = random.randint(0, 9007199254740992)

         # HMAC[SHA256]_{secret} (key | timestamp | seq | nonce | body) => signature

         hm = hmac.new(self._secret.encode('utf8'), None, hashlib.sha256)
         hm.update(params['key'].encode('utf8'))
         hm.update(params['timestamp'].encode('utf8'))
         hm.update(u"{0}".format(params['seq']).encode('utf8'))
         hm.update(u"{0}".format(params['nonce']).encode('utf8'))
         hm.update(body)
         signature = base64.urlsafe_b64encode(hm.digest())

         params['signature'] = signature

      self._seq += 1

      path = "{0}?{1}".format(parse.quote(self._endpoint['path']), parse.urlencode(params))

      ## now issue the HTTP/POST
      ##
      self._connection.request('POST', path, body, self._endpoint['headers'])
      response = self._connection.getresponse()
      response_body = response.read()

      if response.status != 202:
         raise Exception("publication request failed {0} [{1}] - {2}".format(response.status, response.reason, response_body))

      try:
         res = json.loads(response_body)
      except Exception as e:
         raise Exception("publication request bogus result - {0}".format(e))

      return res['id']
