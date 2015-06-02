###############################################################################
##
##  Copyright 2013 Tavendo GmbH. Licensed under the Apache 2.0 license.
##
###############################################################################


import argparse, time, random
import cx_Oracle


if __name__ == '__main__':
   ## parse command line args
   ##
   parser = argparse.ArgumentParser(description = 'Sales event generator for WebMQ dashboard demo.')
   parser.add_argument('--host', type = str, required = True, help = "Oracle database hostname or IP address")
   parser.add_argument('--port', type = int, default = 1521, help = "Oracle database listening port [default: 1521]")
   parser.add_argument('--sid', type = str, default = "ORCL", help = "Oracle database SID [default: ORCL]")
   parser.add_argument('--user', type = str, default = "webmqdemo", help = "WebMQ demo schema user name [default: webmqdemo]")
   parser.add_argument('--password', type = str, default = "webmqdemo", help = "WebMQ demo schema user password [default: webmqdemo]")

   args = parser.parse_args()

   ## connect to Oracle
   ##
   dsn = cx_Oracle.makedsn(args.host, args.port, args.sid)
   conn = cx_Oracle.connect(args.user, args.password, dsn)
   conn.autocommit = True

   cur = conn.cursor()
   cur.execute("SELECT SYSTIMESTAMP AT TIME ZONE 'utc' FROM dual")
   res = cur.fetchone()
   print "Connected to Oracle - current time on database", res[0]

   ## generate fake sales events
   ##
   regions = [('North', 10.), ('South', 12.), ('East', 5.), ('West', 2.)]
   products = [('Product A', 169.25, 4), ('Product B', 99.5, 10), ('Product C', 599.99, 3)]

   cur = conn.cursor()
   cur.prepare("""
      INSERT INTO sales
         (id, trans_dt, product, region, units, price)
            VALUES (sales_id.nextval, SYSTIMESTAMP AT TIME ZONE 'utc', :product, :region, :units, :price)
   """)

   while True:
      product = random.choice(products)
      region = random.choice(regions)
      units = random.randint(1, product[2])
      uvp = product[1]
      discount = uvp * (region[1] / 100.)
      price = uvp - discount
      cur.execute(None, product = product[0], region = region[0], units = units, price = price)
      print "Generated Sales Event:", product[0], region[0], units, price
      time.sleep(2 * random.expovariate(2))
