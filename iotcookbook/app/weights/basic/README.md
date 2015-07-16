# Arduino Yun Weighing Pad - Basic Version

This connects weighing pads connected to an Arduino Yun to an in-browser spreadsheet, from which the converted values are sent to be displayed in gauges.

A constant stream of values (at a configurable sampling frequency) is sent.

## To do

* Common configuration: Presently the pins/number of pads needs to be configured separately in the code for the Yun and the spreadsheet, and the gauges output is not configurable. 

   * have a configuration file in the spreadsheet part
   * this can be requested via RPC
   * the yun uses this to set up the pads
   * the gauges output creates a gauge for each of the pads


