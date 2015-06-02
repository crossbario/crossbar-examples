###############################################################################
##
##  Copyright 2012 Tavendo GmbH
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

import sys, shelve, json, random, uuid

from flask import Flask, url_for, Response, request, session, render_template

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# http://flask.pocoo.org/docs/config/
app.config['SESSION_COOKIE_NAME'] = 'FLASKSESSID'
app.config['SESSION_COOKIE_HTTPONLY'] = False

db = shelve.open("articles.dat")


def newid():
   return ''.join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in xrange(6)])

def returnJson(obj, code = 200):
   resp = Response(json.dumps(obj), status = code, mimetype = 'application/json')
   return resp


@app.route('/')
def root():
   session['foo'] = 'bar'
   return render_template('home.html')


@app.route('/articles', methods = ['PUT'])
def article_create():
   if request.headers['Content-Type'] == 'application/json':
      try:
         data = json.loads(request.data)
      except Exception, e:
         return returnJson("payload must be valid JSON", 400)
      key = newid()
      db[key] = data
      return returnJson(key)
   else:
      return returnJson("payload type must be JSON", 400)


@app.route('/articles')
def article_readall():
   articles = []
   for a in db.items():
      article = a[1]
      article['id'] = a[0]
      articles.append(article)
   return returnJson(articles)


@app.route('/articles/<articleid>')
def article_read(articleid):
   articleid = str(articleid)
   if db.has_key(articleid):
      return returnJson(db.get(articleid))
   else:
      return returnJson("no article with id %s" % articleid, 400)


@app.route('/articles/<articleid>', methods = ['POST'])
def article_update(articleid):
   if request.headers['Content-Type'] == 'application/json':
      try:
         data = json.loads(request.data)
      except Exception, e:
         returnJson("payload must be valid JSON", 400)
      articleid = str(articleid)
      if db.has_key(articleid):
         db[articleid] = data
         return ""
      else:
         return returnJson("no article with id %s" % articleid, 400)
   else:
      return returnJson("payload type must be JSON", 400)


@app.route('/articles/<articleid>', methods = ['DELETE'])
def article_delete(articleid):
   articleid = str(articleid)
   if db.has_key(articleid):
      del db[articleid]
      return ""
   else:
      return returnJson("no article with id %s" % articleid, 400)


if __name__ == "__main__":

   app.run(host = "0.0.0.0", port = 8005, debug = True)
