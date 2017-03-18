# Exclude Subscribers

This example shows several ways to exclude subscribers from getting a
subscription.

After starting the router ("crossbar start") in one terminal open four
other terminals and run the four scripts "alice.py", "bob.py",
"carol.py" and "erin.py" in each. "dave" is javascript code running on
Web page that you can visit at http://localhost:8080

Each of these publishes a "heartbeat" message every 3 seconds that the
others listen for; see the PublishOptions in each of alice, bob and
carol for use of exclude_authid= and exclude_authrole= options. Every
6 seconds, alice publish to just the "alpha" role.

Note: if you change the .priv key files you'll have to change
.crossbar/config.json to update the authorized public keys.

Roles:

  alpha: alice, bob, dave
   beta: erin, carol

Blacklisting:

  alice: excludes "bob" via exclude_authid
    bob: excludes "beta" via exclude_authrole
   dave: excludes "alice", "bob" via exclude_authid
  carol: publishes normally

Whitelisting:

   erin: to "alice", "bob" and "dave" via eligible_authid
         also to "beta" via eligible_authrole

Note that by default a publish does *not* get echoed back to the
session that sent it. "alice" and "erin" use "exclude_me=False" to get
(some of) their publishes echoed back.
