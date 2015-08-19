var mraa = require('mraa');
var led = new mraa.Gpio(13);
led.dir(mraa.DIR_OUT);
var led_state = true;

function toggle_led () {
  led.write(led_state ? 1 : 0);
  led_state = !led_state;
  setTimeout(toggle_led, 200);
}

toggle_led();

