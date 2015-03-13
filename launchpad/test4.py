import launchpad
import time, random


class Test:

   FENCE = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]

   def __init__(self, lp, mode = 0):
      self.lp = lp
      self.mode = mode
      self.matrix = []
      for y in xrange(9):
         self.matrix.append([])
         for x in xrange(9):
            self.matrix[y].append([])

   def pushlight(self, x, y, r, g):
      if x >= 0 and x < 9 and y >= 0 and y < 9:
         self.matrix[y][x].append((r, g))
         self.lp.light(x, y, r, g)

   def poplight(self, x, y):
      if x >= 0 and x < 9 and y >= 0 and y < 9:
         if len(self.matrix[y][x]) > 0:
            self.matrix[y][x].pop()
            if len(self.matrix[y][x]) > 0:
               c = self.matrix[y][x][-1]
            else:
               c = (0,0)
            self.lp.light(x, y, c[0], c[1])

   def pushrect(self, x0, y0, w, h, r, g):
      for x in xrange(w):
         for y in xrange(h):
            self.pushlight(x0 + x, y0 + y, r, g)

   def poprect(self, x0, y0, w, h):
      for x in xrange(w):
         for y in xrange(h):
            self.poplight(x0 + x, y0 + y)

   def run(self):
      while True:
         e = self.lp.poll()
         if e:
            if e[2]:
               self.pushrect(e[0] - 1, e[1] - 1, 3, 3, 3, 3)
               self.pushlight(e[0], e[1], 3, 0)
            else:
               self.poprect(e[0] - 1, e[1] - 1, 3, 3)
               self.poplight(e[0], e[1])
         time.sleep(0.01)

if __name__=="__main__":

   launchPads = launchpad.findLaunchpads()
   l = launchpad.launchpad(*launchPads[-1])
   l.reset()

   t = Test(l, 1)
   t.run()
