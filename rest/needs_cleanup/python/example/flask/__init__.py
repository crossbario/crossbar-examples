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

import sys
import crossbarconnect
from flask import Flask, request, render_template

## some configuration
##
PUSH_URL = "http://127.0.0.1:8080/push"
TOPIC_URI = "com.myapp.topic1"
WAMP_URL = "ws://127.0.0.1:8080/ws"
WAMP_REALM = "realm1"

app = Flask(__name__)


@app.route("/")
def index():
   """
   Render demo main page.
   """
   return render_template('index.html',
      ## prefill the form with these values
      name = "Heinzelmann", age = 23,
      ## config for subscribing to events
      router = WAMP_URL, realm = WAMP_REALM, topic = TOPIC_URI)


@app.route('/form1', methods = ['POST'])
def form1_submit():
   """
   Extract data from a submitted HTML form, publish event via
   Crossbar.io HTTP Pusher service and render success page.
   """
   try:
      ## here we publish the form data via Crossbar.io HTTP Pusher service
      ## as a WAMP event to all subscribers on TOPIC_URI
      ##
      publication_id = app.pusher.publish(TOPIC_URI,
         name = request.form['name'], age = request.form['age'])
      return render_template('onsubmit.html', publication_id = publication_id)
   except Exception as e:
      return "Publication failed: {}".format(e)



if __name__ == "__main__":

   ## we create a client for pushing event via Crossbar.io
   app.pusher = crossbarconnect.Client(PUSH_URL)

   ## now run our Flask app
   app.run(debug = True)
