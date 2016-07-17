Some clients nax not have 24 cores - hey, a E7 v3 only costs like 5k bucks!

Anyway. For these clients, it might make sense to limit the concurrency at which Crossbar.io will forward them calls - so they don't collapse under load.

With regular registrations, that is without using "shared registrations", this is already useful.

A client able to utilize 4 cores might register a procedure at a concurrency of 4.

Crossbar.io will then never forward more than 4 invocations to that client. When the maximum concurrency (of 4) is reached, and yet another call comes in, Crossbar.io can:

1. deny the call immediately (that is, the call returns with error)
2. queue up the call internally and only forward if outstanding invocations come back (and hence we can forward while staying under the max)
