import launchpad
import time, random

if __name__=="__main__":
   launchPads = launchpad.findLaunchpads()
   print launchPads
   l = launchpad.launchpad(*launchPads[-1])

   l.reset()
   l.ledTest(1)
   l.setDrumRackMode()

   for i in range(5):
      for y in range(9):
         for x in range(9):
            c = random.randint(0,3)
            l.light(x,y,c,0)
      for y in range(9):
         for x in range(9):
            c = random.randint(0,3)
            l.light(x,y,0,c)
      for y in range(9):
         for x in range(9):
            c = random.randint(0,3)
            l.light(x,y,c,c)

   for y in range(9):
      for x in range(9):
         l.light(x,y,0,0)
