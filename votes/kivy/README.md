This version of the Votes demo offers a frontend written using [kivy](http://kivy.org/#home) in addition to the browser frontend.

## Regular startup

In the demo folder do 

```
crossbar start
```

and then open 

```
http://localhost:8080
```

to see the browser frontend.

## Additional Requirements

For the kivy frontend you need to install kivy (big surprise) - follow the instructions at the [project website](http://kivy.org/docs/gettingstarted/installation.html).

You then need to install Autobahn|Python and its dependencies - for kivy (.

In the `kivy` folder, using the Python as setup by kivy, do

* on Mac OSX

```
kivy -m pip install -r requirements-tavendo.txt
```

* on other systems

```
python -m pip install -r requirements-tavendo.txt
```

> Note: To use Python with kivy's setup e.g. on Windows go to the kivy folder, execute `kivy-X.x.bat` ( where `X.x` = the Python version you downloaded kivy for), which opens a command shell with the environment set to use the correct Python. Then navigate to the votes demo folder and execute the above commands.

Then start the kivy votes frontend by doing

(Mac OSX)

``` 
kivy main.py
```

(others)

```
python main.py
```

This connects to the locally running Crossbar.io.

You can get the additional browser frontend by opening

```
http://localhost:8080
```

Use either to increase/reset the vote count, and see this updated immediately in the other.

> Thanks to [Roger Erens](https://github.com/rogererens) for providing this example!
