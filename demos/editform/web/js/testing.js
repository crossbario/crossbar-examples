// create test events for the editable form
// needs to be loaded after the main app JS
// since it uses the session and
// the normalizeSet function from there

function createTestEvents (evt, rep) {
   switch(evt) {
      case "create":
         rep = !rep ? 1 : rep;
         for( var i = 0; i < rep; i++) {
            console.log("constructing", i);
            var saveSet = { inStock: i, name: "Test Item " + i, orderNumber: "TT-" + i, price: i*3.5, size: i +4, weight: i*1.3+40 };
            vm.normalizeSet(saveSet);
            session.call("form:create", [], saveSet).then(
               function (res) {
                  session.log("created", res);
               },
               session.log
            );
         }
         break;
      case "delete":
         // console.log("no deleting yet");
         var items;
         session.call("form:filter", [rep], {name: {type: "prefix", value: "Test" }}).then(function(res) {
            for(var i = 0; i < rep; i++) {
               if(res[i]) {
                  // var index = getIndexFromId(res[i].id);
                  console.log("id ", res[i].id);
                  session.call("form:delete", [res[i].id]).then(
                     function(res) {
                        session.log("deleted", res);
                        // delete the item
                        onItemDeleted("localDelete", res[i].id);
                     },
                     session.log
                  );
               }
            }
         }, session.log);

         break;
      case "update":
         // console.log("no update yet");
         var items;
         session.call("form:filter", [rep], {name: {type: "prefix", value: "Test" }}).then(function(res) {
            for(var i = 0; i < rep; i++) {
               if(res[i]) {
                  // var index = getIndexFromId(res[i].id);
                  console.log("id ", res[i].id);
                  var updated = { id: res[i].id, orderNumber: "updated " + i*rep};
                  session.call("form:update", [], updated).then(session.log, session.log);
               }
            }
         }, session.log);
         break;
      default:
         break;
   }
};