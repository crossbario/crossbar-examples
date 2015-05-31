// see if IE < 9

$(document).ready(function() {
   
   // see if any elements inserted by conditional comments
   // are in the DOM
   var ieSmallerNine = $(".link_disable");
   
   // attach click handler that prevents default behaviour
   // for links
   if (ieSmallerNine[0]) {
      for (var i = 0; i < ieSmallerNine.length; i++) {
         $('.link_disable>a').click(function() {
            //alert("clicked");
            return false;
         });
      }
   }
   
})