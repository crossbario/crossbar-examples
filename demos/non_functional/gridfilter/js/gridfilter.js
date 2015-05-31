/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

var channelBaseUri = "http://crossbar.io/crossbar/demo/chat/";
var session = null;

var rows = 20; // number of rows in the result set requested from the database
var filterFields = {}; // mapping of field names to filter input fields

var addedItemId;


$(document).ready(function() {
   updateStatusline("Not connected.");

   ko.applyBindings(vm);

   $("#helpButton").click(function() {
      $(".info_bar").toggle();
   });

   connect();
});

function connect() {

   // use jQuery deferreds
   ab.Deferred = $.Deferred;

   // Connect to Crossbar.io ..
   //
   ab.launch(
      // WAMP app configuration
      {
         // Crossbar.io server URL
         wsuri: ab.getServerUrl("ws", "ws://127.0.0.1:8080/ws"),
         // authentication info
         appkey: null, // authenticate as anonymous
         appsecret: null,
         appextra: null,
         // additional session configuration
         sessionConfig: {maxRetries: 10,
                         sessionIdent: "Vote"}
      },
      // session open handler
      function (newSession) {
         session = newSession;

         updateStatusline("Connected to " + session.wsuri() + " in session " + session.sessionid());

         session.prefix("api", "http://crossbar.io/crossbar/demo/product#");

         // send request for initial data cut from DB
         session.call("api:filter", {}, rows).then(
            gridfilter.refreshGridData,
            onOraCallError);

         // subscribe to data change events
         session.subscribe("api:oncreate", onItemCreated);
         session.subscribe("api:onupdate", onItemUpdated);
         session.subscribe("api:ondelete", onItemDeleted);
      },
      // session close handler
      function (code, reason, detail) {
         session = null;
         updateStatusline(reason);
      }
   );
}

gridfilter = {};

gridfilter.displayEmptyRow = function() {
   var emptyRow = { "name": " ", "orderNumber": " ", "weight": " ", "size": " ", "inStock": " ", "price": " " };
   vm.tableData.push(new product(emptyRow));
   vm.noEntries(true);
};

gridfilter.currentlyHighlighted = [];

gridfilter.isEmptyObject = function(obj) {
   // from http://stackoverflow.com/questions/4994201/is-object-empty

   // null and undefined are empty
   if (obj === null) return true;
   // Assume if it has a length property with a non-zero value
   // that that property is correct.
   if (obj.length && obj.length > 0)    return false;
   if (obj.length === 0)  return true;

   for (var key in obj) {
      if (hasOwnProperty.call(obj, key))    return false;
   }

   return true;
};

gridfilter.refreshGridData = function(data) {
   // clear previous data
   vm.tableData([]);
   vm.noEntries(false);

   // add new data
   if (data.length !== 0) {
      for (var i = 0; i < data.length; i++) {
         vm.tableData.push(new product(data[i]));
      }
   }
   else {
      // display a 'no results for the current filter criteria' indicator
      var emptyRow = { "name": " ", "orderNumber": " ", "weight": " ", "size": " ", "inStock": " ", "price": " " };
      vm.tableData.push(new product(emptyRow));
      vm.noEntries(true);
   }
};

/*
   Highlights any of the 'currentyHighlighted' items that are found in the current grid
*/
// gridfilter.setCurrentHighlights = function() {
//    console.log("setting highlights for ", gridfilter.currentlyHighlighted.toString());
//    for(var i = 0; i < gridfilter.currentlyHighlighted.length; i++ ){
//       var index = getIndexFromId(gridfilter.currentlyHighlighted[i]);
//       if (index != "notFound") {
//          vm.tableData()[index].itemState("hasBeenCreated");
//       }
//    }
// };

gridfilter.setCurrentHighlights = function() {
   for( var i = 0; i < vm.tableData().length; i++ ) {
      var id = vm.tableData()[i].id();
      for( var c = 0; c < gridfilter.currentlyHighlighted.length; c++ ){
         if(id === gridfilter.currentlyHighlighted[c]) {
            vm.tableData()[i].itemState("hasBeenCreated");
         }
      }
   }
};

/*
   Removes the highlighting from a specific item, if found in the grid
   + removes this from 'currentlyHighlighted'
*/
gridfilter.removeHighlight = function(id) {

   var index = getIndexFromId(id);

   if(index != "notFound") {
      vm.tableData()[index].itemState("");
   }

   for(var i = 0; i < gridfilter.currentlyHighlighted.length; i++) {
      if(gridfilter.currentlyHighlighted[i] === id) {
         gridfilter.currentlyHighlighted.splice(i, 1);
      }
   }

};


function onDataReceived(data) {
   gridfilter.refreshGridData(data);
}

function onItemCreated(uri, obj){

   var addedItemId = obj.id;

   // re-request the set to display for the current filter settings
   session.call("api:filter", vm.filter(), rows).then(function(obj) {

      // check whether the added item is contained in the revised set
      // that should be the current display
      // resuls set does not always contain the item when it should
      var found = false;
      for(var i = 0; i < obj.length; i++) {

         if(obj[i].id === addedItemId) {
            found = true;

            // add the item id to 'currently highlighted' array
            gridfilter.currentlyHighlighted.push(obj[i].id);

            // refresh grid with new data
            gridfilter.refreshGridData(obj);

            // set the current highlights
            gridfilter.setCurrentHighlights();

            // start timeout for this particular highlight
            var id = obj[i].id;
            window.setTimeout(function() {
               gridfilter.removeHighlight(id);
            }, 1400);

         }
      }
      if (found === false) {
         // console.log("item not in results set");
      }
   }, session.log);

}

function onItemUpdated(uri, obj){

   var index = getIndexFromId(obj.id);

   // do nothing if the updated item is not part of the currently
   // displayed grid
   if (index === "notFound") {
      // console.log("modified item not in current grid");
      return;
   }
   // temporary highlighting of the grid item
   var previousItemState = vm.tableData()[index].itemState();
   vm.tableData()[index].itemState("hasBeenEdited");
   window.setTimeout(function() { vm.tableData()[index].itemState(previousItemState); }, 1400);

   // update the changes
   for(var i in obj) {
      if(obj.hasOwnProperty(i)){
         vm.tableData()[index][i](obj[i]);
      }
   }
}


/* bug: sometimes, with multiple quick deletions,
    one item remains undeleted - FIXME
*/
function onItemDeleted(uri, obj){
   var index = getIndexFromId(id);

   // do nothing if the updated item is not part of the currently
   // displayed grid
   if (index === "notFound") {
      // console.log("deleted item not in current grid");
      return;
   }

   vm.tableData()[index].itemState("isBeingDeleted");

   window.setTimeout(function() {
      var fadeTime = 200;
      // fade out item
      var index = getIndexFromId(id); // get index again, since with mass deletions, this might have changed in the meantime
      vm.tableData()[index].itemState("nonDisplay");
      // set timeout to delete item after end of fade
      window.setTimeout(function() {
         var index = getIndexFromId(id); // get index again - see above;
         vm.tableData.splice(index, 1); // delete the item

         // check whether there is an entry beyond what was previously displayed and add this
         session.call("api:filter", vm.filter(), rows).then(function(obj){
            if(obj.length > vm.tableData().length){
               // we need to add an object
               // in the DB, at this point multiple items may have been deleted already
               // we need to find the first item in the results set that is not
               // part of the displayed set
               for( var i = 0;  i < obj.length; i++ ) {
                  var displayed = false;
                  var curObj = obj[i];
                  // is current item displayed?
                  // can't go by position, since several items may have been deleted before timeout finishes
                  for (var t = 0; t < vm.tableData().length; t++ ) {
                     if (curObj.id === vm.tableData()[t].id()) {
                        var displayed = true;
                     }
                  }
                  if(displayed === false) {
                     // not displayed. since we only deleted one item, this is the only item
                     // we need to add at this point
                     var newRow = new product(curObj);
                     vm.tableData.push(newRow); // can just push, since this is always added at the end;
                     return;
                  }
               }
            }
            // check whether current list is empty
            if (vm.tableData().length === 0) {
               gridfilter.displayEmptyRow();
            }
         });
      }, fadeTime);
   }, 1400);
}

// gives the current index of the item to be updated or deleted
// within the grid
// return 'undefined' is valid, since the item may not be part of
// the present grid content
function getIndexFromId(id) {
   var index = "notFound",
       gridLength = vm.tableData().length;
   for (var i = 0; i < gridLength; i++ ) {
      if (vm.tableData()[i].id() === id) {
         index = i;
      }
   }
   return index;
}

function onOraCallError(error) {
   $("#error_overlay").show();
}

var vm = new ViewModel(); // instantiates the view model and makes its methods accessible

function ViewModel() {

   var self = this;

   this.tableData = ko.observableArray([]);
   this.noEntries = ko.observable(false);

   // request counter
   this.requestsSent = ko.observable(0);

   // filter currently contains values changed from default empty
   this.currentFilterValues = ko.observable(false);

   // textual inputs
   this.name = ko.observable("");
   this.orderNumber = ko.observable("");
   this.weight = ko.observable("");
   this.size = ko.observable("");
   this.inStock = ko.observable("");
   this.price = ko.observable("");

   // radio inputs
   this.nameType = ko.observable("prefix");
   this.orderNumberType = ko.observable("prefix");
   this.weightType = ko.observable("lte");
   this.sizeType = ko.observable("lte");
   this.inStockType = ko.observable("lte");
   this.priceType = ko.observable("lte");

   this.inputs = { "filterByOrderNumber": "string", "filterByName": "string", "filterByPrice": "num", "filterByWeight": "num", "filterBySize": "num", "filterByInStock": "num" };
   this.mangleInputs = function(viewmodel, event) {
      // filter out non-numeric inputs on numeric input fields
      if (self.inputs[event.target.id] === "num") {
         if (event.keyCode > 57 && event.keyCode !== 190) {
            return false;
         }
      }
      return true; // knockout.js otherwise prevents the default action
   };

   this.filter = ko.computed(function() {

      var filterSet = {};
      // triggers based on single change
      // calculates entire filter set based on present input states
      if (self.name() !== "") {
         filterSet.name = { value: self.name(), type: self.nameType() };
      }
      if (self.orderNumber() !== "") {
         filterSet.orderNumber = { value: self.orderNumber(), type: self.orderNumberType() };
      }
      if (self.weight() !== "") {
         filterSet.weight = { value: parseFloat(self.weight(), 10), type: self.weightType() };
      }
      if (self.size() !== "") {
         filterSet.size = { value: parseFloat(self.size(), 10), type: self.sizeType() };
      }
      if (self.inStock() !== "") {
         filterSet.instock = { value: parseFloat(self.inStock(), 10), type: self.inStockType() };
      }
      if (self.price() !== "") {
         filterSet.price = { value: parseFloat(self.price(), 10), type: self.priceType() };
      }
      if (!gridfilter.isEmptyObject(filterSet)) {
         self.currentFilterValues(true);
      }
      if (session !== null) {
         self.requestsSent(self.requestsSent() + 1);
         session.call("api:filter", filterSet, rows).then(onDataReceived, session.log);
      }
      return filterSet;
   }, this);

   this.resetFilter = function() {
      // textual inputs
      this.name("");
      this.orderNumber("");
      this.weight("");
      this.size("");
      this.inStock("");
      this.price("");

      // radio inputs
      this.nameType("prefix");
      this.orderNumberType("prefix");
      this.weightType("lte");
      this.sizeType("lte");
      this.inStockType("lte");
      this.priceType("lte");

      // hide the reset button
      this.currentFilterValues(false);
   };
}

function product(data) {
   return {
      id: ko.observable(data["id"]),
      name: ko.observable(data["name"]),
      orderNumber: ko.observable(data["orderNumber"]),
      weight: ko.observable(data["weight"]),
      size: ko.observable(data["size"]),
      inStock: ko.observable(data["inStock"]),
      price: ko.observable(data["price"]),
      itemState: ko.observable()
   };
}





function updateStatusline(status) {
   $(".statusline").text(status);
}
