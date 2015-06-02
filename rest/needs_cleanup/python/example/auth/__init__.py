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

## Tavendo WebMQ Application Key and Secret for our Web app
APPKEY = 'foobar'
APPSECRET = 'secret'

## The "user database" of our Web app
USERDB = {'joe': 'secret', 'admin': 'hoho'}


import json, uuid, sys

from flask import Flask, url_for, Response, request, session, \
                  render_template, redirect, escape, flash

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())




import hmac, hashlib, binascii

def authSignature(authChallenge, authSecret = None):
   if authSecret is None:
      authSecret = ""
   h = hmac.new(authSecret, authChallenge, hashlib.sha256)
   sig = binascii.b2a_base64(h.digest()).strip()
   return sig


@app.route('/')
def index():
   if 'username' in session:
      return render_template('index.html',
                             server = sys.argv[1],
                             topic = "http://example.com/simple")
   else:
      return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      username = request.form['username']
      if not USERDB.has_key(username) or \
         USERDB[username] != request.form['password'] != 'secret':
         error = 'Invalid credentials'
      else:
         flash("You were successfully logged in as '%s'" % username)
         session['username'] = username
         return redirect(url_for('index'))
   return render_template('login.html', error = error)


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


@app.route('/authsign', methods = ['POST'])
def authsign():
   if 'username' in session:
      try:
         data = json.loads(request.data)
         print "Challenge:", data
         if data['authkey'] == APPKEY:
            sig = authSignature(request.data, APPSECRET)
            print "Signature:", sig
            return sig
      except Expection, e:
         print e
   return ""


if __name__ == "__main__":
   app.run(host = "0.0.0.0", port = 8000, debug = True)
