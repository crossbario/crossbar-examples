# Exclude Subscribers

This example shows several ways to exclude subscribers from getting a
subscription.

After starting the router ("crossbar start") in one terminal open
three other terminals and run the three scripts "alice.py", "bob.py"
and "carol.py" in each.

Each of these publishes a "heartbeat" message every 3 seconds that the
others listen for; see the PublishOptions in each of alice, bob and
carol for use of exclude_authid= and exclude_authrole= options.

Note: if you change the .priv key files you'll have to change
.crossbar/config.json to update the authorized public keys.

alice and bob are in the "alpha" role and carol is in the "beta"
role. dave is the Web page that you can visit at http://localhost:8080
and is also in role "alpha"
