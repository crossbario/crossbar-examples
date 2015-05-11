var exec = require('child_process').exec;

function get_photo () {
   exec("fswebcam -r 640x480 --no-banner", function(err, stdout, stderr) {
      console.log("stdout ", stdout);
      console.log("stderr ", stdout);
      if (error != null) {
         console.log("exec error: ", error);
      };
   })
}