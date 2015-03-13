#!/usr/bin/env python2.7
# vim: set fileencoding=UTF-8 :
"""Python interface for Novation Launchpads

Requires pyPortMidi from http://alumni.media.mit.edu/~harrison/code.html
But that version doesn't compile on a modern python without patching. You
can instead use pyGame's MIDI support which is more up to date.

TODO:
	LED double-buffering and flashing
"""

try:
	import pypm
except ImportError:
	from pygame import pypm

import time, random


class LaunchPadError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def findLaunchpads():
   ins = []
   outs = []
   i = 0
   for loop in range(pypm.CountDevices()):
      interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
      print i, interf,name,inp,outp,opened
      if name.find("Launchpad") >= 0:
         if inp:
            ins.append(loop)
         else:
            outs.append(loop)
      i += 1
   return zip(ins,outs)


class launchpad:
   _midiIn = None
   _midiOut = None
   _drumrackMode = False

   def __init__(self, idIn, idOut):
      self._midiIn = pypm.Input(idIn)
      self._midiOut = pypm.Output(idOut, 0)

   def reset(self):
      self._midiOut.WriteShort(0xb0, 0, 0)
      self._drumrackMode = False

   def autoTest1(self, n = 4):
      i = 0
      v = [1, 2, 3, 2]
      while i < n * 4:
         self.ledTest(v[i % 4])
         i += 1
         time.sleep(0.2)
      self.reset()

   def autoTest2(self, n = 6):
      for i in range(n):
         for y in range(9):
            for x in range(9):
               c = random.randint(0,3)
               self.light(x,y,c,0)
         for y in range(9):
            for x in range(9):
               c = random.randint(0,3)
               self.light(x,y,0,c)
         for y in range(9):
            for x in range(9):
               c = random.randint(0,3)
               self.light(x,y,c,c)
      self.reset()


   def autoTest3(self, n = 100):
      for i in xrange(n):
         a = []
         for y in xrange(9):
            a.append([])
            for x in xrange(9):
               a[y].append([random.randint(0,3), random.randint(0,3)])
         self.lightAll(a)
      self.reset()


   def ledTest(self, brightness = 3):
      if not 1 <= brightness <= 3:
         raise LaunchPadError("Bad brightness value %s" % brightness)
      self._midiOut.WriteShort(0xb0, 0, 124 + brightness)
      self._drumrackMode = False

   def setDutyCycle(self, numerator, denominator):
      if numerator < 9:
         data = (16 * (numerator - 1)) + (denominator - 3)
         self._midiOut.WriteShort(0xb0, 0x1e, data)
      else:
         data = (16 * (numerator - 9)) + (denominator - 3)
         self._midiOut.WriteShort(0xb0, 0x1f, data)

   def setDrumRackMode(self, drumrack=True):
      self._drumrackMode = drumrack
      self._midiOut.WriteShort(0xb0, 0, drumrack and 2 or 1)

   def light(self, x, y, red, green):
      if not 0 <= x <= 8: return
      if not 0 <= y <= 8: return
      if not 0 <= red <= 3: return
      if not 0 <= green <= 3: return

      #if not 0 <= x <= 8: raise LaunchPadError("Bad x value %s" % x)
      #if not 0 <= y <= 8: raise LaunchPadError("Bad y value %s" % y)
      #if not 0 <= red <= 3: raise LaunchPadError("Bad red value %s" % red)
      #if not 0 <= green <= 3: raise LaunchPadError("Bad green value %s" % green)

      velocity = 16*green + red + 8 + 4

      if y==8:
         if x != 8:
            note = 104 + x
            self._midiOut.WriteShort(0xb0,note,velocity)
         return

      if self._drumrackMode:
         if x==8:
            # Last column runs from 100 - 107
            note = 107-y;
         elif x<4:
            note = 36 + x + 4*y
         else:
            # Second half starts at 68, but x will start at 4
            note = 64 + x + 4*y
      else:
         note = x + 16*(7-y)

      self._midiOut.WriteShort(0x90,note,velocity)

   def lightAll(self, levels):
      velocity = 0
      for level in self._orderAll(levels):
         red = level[0]
         green = level[1]
         if velocity:
            velocity2 = 16*green + red + 8 + 4
            self._midiOut.WriteShort(0x92, velocity, velocity2)
            velocity = 0
         else:
            velocity = 16*green + red + 8 + 4
      self.light(0,0,levels[0][0][0],levels[0][0][1])

   def _orderAll(self,levels):
      for y in range(8):
         for x in range(8):
            yield levels[x][7-y]
      x = 8
      for y in range(8):
         yield levels[x][7-y]

      y = 8
      for x in range(8):
         yield levels[x][y]



   def lightSingleTest(self):
      for x in range(8):
         for y in range(8):
            self.light(x,y,x%4,y%4)

   def lightAllTest(self,r=None,g=None):
      grid = []
      for x in range(9):
         grid.append([])
         for y in range(9):
            if (r==None):
               grid[x].append( (x%4, y%4) )
            else:
               grid[x].append( (r%4, g%4) )

      self.lightAll(grid)

   def poll(self):
      if self._midiIn.Poll():
         data = self._midiIn.Read(1);
         #print data
         [status,note,velocity,extraData] = data[0][0]
         timestamp=data[0][1]
         if status == 176:
            y = 8
            x = note - 104
           # print x, y
         elif self._drumrackMode:
            if note>99:
               x=8
               y=107-note
            else:
               x = note % 4
               y = (note/4)-9
               if y>7:
                  x += 4
                  y -= 8
         else: # Normal mode
            x = note % 16
            y = 7 - (note / 16)
         #print x,y,velocity==127
         return x,y,velocity==127,timestamp
      return None

   def showImage(self, im, offsetx=0, offsety=0):
      grid = []
      xsize,ysize = im.size
      for x in range(9):
         grid.append([])
         for y in range(9):
            try:
               r,g,b = im.getpixel(((x + offsetx), (8-y + offsety)))[:3]
               grid[x].append((r/64, g/64))
            except IndexError:
               # We are off the side of the image
               grid[x].append((0,0))
      self.lightAll(grid)

# I don't know if the below is needed, or if it is safe to call automatically, but the comment in the example I'm copying said:
# always call this first, or OS may crash when you try to open a stream
pypm.Initialize()

if __name__=="__main__":
	import time

	launchPads = findLaunchpads()
	l = launchpad(*launchPads[0])

	l.reset()
	l.setDrumRackMode()
	l.lightAllTest()
	#l.lightSingleTest()

	# Wait half a second before exiting to make sure all data has got out.
	time.sleep(.5)
