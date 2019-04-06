# Getting user input asynchronously

The [Python Prompt Toolkit](https://github.com/jonathanslenders/python-prompt-toolkit) has a neat feature: it supports non-blocking [prompts in asyncio applications](http://python-prompt-toolkit.readthedocs.io/en/stable/pages/building_prompts.html#prompt-in-an-asyncio-application).

> Sadly, it doesn't seem to support Twisted.

To install:

    pip install "prompt_toolkit>=2"

Then, start Crossbar.io in terminal 1 (`crossbar start` from this folder).

Now run the client:

```console
(cpy360_4) oberstet@office-corei7:~/scm/crossbario/crossbar-examples/prompt$ python client.py
Connected!
x: 33
RPC succeded: 33 + 23 = 56
```

The input is validated .. so try entering a string which isn't a valid integer.
