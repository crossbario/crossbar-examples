import launchpad
import time, random

if __name__=="__main__":
   launchPads = launchpad.findLaunchpads()
   l = launchpad.launchpad(*launchPads[-1])
   l.reset()

   #l.autoTest1()
   #l.autoTest2()
   l.autoTest3()
