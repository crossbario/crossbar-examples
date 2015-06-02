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

import sys
import webmqconnect

if __name__ == '__main__':

   if len(sys.argv) < 6:
      print """
Usage:   python signedpush.py <WebMQ Push Endpoint> <Auth Key> <Auth Secret> <Topic URI> <Message>
Example: python signedpush.py http://autobahn-euwest.tavendo.de:8080 "foobar" "secret" http://autobahn.tavendo.de/public/demo/pubsub/577274 "Hello from Python"
"""
      sys.exit(1)

   client = webmqconnect.Client(sys.argv[1], authKey = sys.argv[2], authSecret = sys.argv[3])
   client.push(topic = sys.argv[4], event = sys.argv[5])
