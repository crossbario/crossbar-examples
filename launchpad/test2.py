import launchpad
import time, random


class Test:

   FENCE = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]

   def __init__(self, lp, mode = 0):
      self.lp = lp
      self.mode = mode

   def run(self):
      while True:
         e = self.lp.poll()
         if e:
            if e[2]:
               if self.mode == 0:
                  self.lp.light(e[0], e[1], 3, 3)
               elif self.mode == 1:
                  self.lp.light(e[0], e[1], 3, 0)
                  for c in Test.FENCE:
                     self.lp.light(e[0] + c[0], e[1] + c[1], 3, 3)
               elif self.mode == 2:
                  self.lp.ledTest(3)
                  self.lp.light(e[0], e[1], 0, 0)
            else:
               if self.mode == 0:
                  self.lp.light(e[0], e[1], 0, 0)
               elif self.mode == 1:
                  self.lp.light(e[0], e[1], 0, 0)
                  for c in Test.FENCE:
                     self.lp.light(e[0] + c[0], e[1] + c[1], 0, 0)
               elif self.mode == 2:
                  self.lp.reset()
         time.sleep(0.01)

if __name__=="__main__":

   launchPads = launchpad.findLaunchpads()
   l = launchpad.launchpad(*launchPads[-1])
   l.reset()

   t = Test(l, 1)
   t.run()
