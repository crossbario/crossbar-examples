[Enable audio](https://www.raspberrypi.org/documentation/configuration/audio-config.md) output on the 3.5mm plug:

```console
sudo amixer cset numid=3 1
```

Install the [flite](http://www.festvox.org/flite/) text-to-speech processor:

```console
sudo apt-get install -y flite
```

Test the text-to-speech engine:

```console
flite -voice slt -t "Hi, my name is Susan. How can I help you?"
```

