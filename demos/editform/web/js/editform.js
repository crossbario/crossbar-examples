// KnockoutJS viewmodel
// Instantiate and bind the viewmodel
var vm = new ViewModel();
ko.applyBindings(vm);


function ViewModel () {

   var self = this;

   /***************************************
   *  Establish connection to WAMP Router *
   ***************************************/

   // the URL of the WAMP Router (Crossbar.io)
   //
   var wsuri;
   if (document.location.origin == "file://") {
      wsuri = "ws://127.0.0.1:8080";

   } else {
      wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
                  document.location.host + "/ws";
   }

   var httpUri;

   if (document.location.origin == "file://") {
      httpUri = "http://127.0.0.1:8080/lp";

   } else {
      httpUri = (document.location.protocol === "http:" ? "http:" : "https:") + "//" +
                  document.location.host + "/lp";
   }

   // WAMP session object
   self.session = null;

   // the WAMP connection to the Router
   //
   self.connection = new autobahn.Connection({
      // url: wsuri,
      transports: [
         {
            'type': 'websocket',
            'url': wsuri
         },
         {
            'type': 'longpoll',
            'url': httpUri
         }
      ],
      realm: "crossbardemo"
   });

   // fired when connection is established and session attached
   //
   self.connection.onopen = function (sess, details) {

      console.log("Connected");

      self.session = sess;

      // $('#new-window').attr('href', window.location.pathname);
      document.getElementById('secondInstance').setAttribute('href', window.location.pathname);

      self.connectionStatus("Connected to " + self.wsuri + " in session " + self.session.id);

      // set an URI prefix
      self.session.prefix("form", "io.crossbar.demo.product");

      // request full data set initially and fill grid
      self.session.call("form:read", [], {start: 0, limit: 25}).then(self.fillList, self.session.log);

      // subscribe to data change events
      self.session.subscribe("form:oncreate", self.onItemCreated);
      self.session.subscribe("form:onupdate", self.onItemUpdated);
      self.session.subscribe("form:ondelete", self.onItemDeleted);
      self.session.subscribe("form:onreset", self.onDataReset);

   };


   // fired when connection was lost (or could not be established)
   //
   self.connection.onclose = function (reason, details) {
      console.log("Connection lost: " + reason, details);
      self.connectionStatus("Connection lost!");
   }


   // now actually open the connection
   //
   self.connection.open();




   /**********************************************
   *  Define our observables and other variables *
   **********************************************/

   // extend knockout observable array to
   // track an index on items in an observableArray
   ko.observableArray.fn.indexed = function(prop) {
      prop = prop || 'index';
      //whenever the array changes, make one loop to update the index on each
      this.subscribe(function(newValue) {
         if (newValue) {

            var item;
            for (var i = 0, j = newValue.length; i < j; i++) {
               item = newValue[i];
               if (!ko.isObservable(item[prop])) {
                  item[prop] = ko.observable();
               }
               item[prop](i);
            }
         }
      });

      //initialize the index
      this.valueHasMutated();
      return this;
   };

   self.listData = ko.observableArray([]).indexed('index');

   self.detailsIds = ["orderNumber", "name", "price", "weight", "size", "inStock"];

   self.detailsEditable = {
      orderNumber: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      name: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      weight: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      size: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      inStock: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      price: {
         displayedValue: ko.observable(),
         storedValue: ko.observable(),
         hasBeenUpdated: ko.observable(false)
      },
      itemState: ko.observable()
   };


   // add computeds for handling 'isDirty' flag on detailsEditable
   self.detailsIds.forEach(function (id) {
      // console.log("adding 'isDirty' for " + id);
      self.detailsEditable[id].isDirty = ko.computed(function() {
         if (self.detailsEditable[id].displayedValue() != self.detailsEditable[id].storedValue()) {
            console.log(id + " is dirty");
            return true;
         } else {
            console.log(id + " is clean");
            return false;
         }
      })
   });

   self.detailsDirty = ko.computed(function() {
      
      // the console.log shows similar behavior to the traditional loop below, 
      // but the computed returns as 'undefined'
      // self.detailsIds.some(function (id) { 
      //    console.log("x", id, self.detailsEditable[id].isDirty());
      //    if (self.detailsEditable[id].isDirty()) {
      //       return true;
      //    }
      // });

      for (var i = 0; i < self.detailsIds.length; ++i) {
         var id = self.detailsIds[i];
         console.log("x", id, self.detailsEditable[id].isDirty());
         if (self.detailsEditable[id].isDirty()) {
            return true;
         }
      }

      // works equivalent to the above loop
      // easier to read in this context, but less adaptable
      // return this.orderNumber.isDirty() || this.name.isDirty() || this.weight.isDirty() || this.size.isDirty() || this.inStock.isDirty() || this.price.isDirty();

   })

   self.orderNumberMissing = ko.computed(function() {
      return self.detailsEditable.orderNumber.displayedValue() === "";
   });
   self.nameMissing = ko.computed(function() {
      return self.detailsEditable.name.displayedValue() === "";
   });

   self.switchWarning = ko.observable(false);
   self.cancelSwitchWarning = ko.computed(function() {
      if (!self.detailsDirty()) {
         self.switchWarning(false);
      }
   })
   
   self.saveButtonVisible = ko.computed(function () {
      return self.orderNumberMissing() === false && self.nameMissing() === false && self.detailsDirty();
   });

   self.cancelButtonVisible = ko.computed(function () {
      return self.detailsDirty() || ( self.detailsCurrent && self.detailsCurrent.itemState() === 'isNew');
   });
   
   self.detailsCurrent = null;
   self.detailsPrevious = null;

   self.focusOnOrderNumber = ko.observable(true);

   self.displayResetNotice = ko.observable(false);

   self.inputs = { "orderNumber": "string", "name": "string", "price": "num", "weight": "num", "size": "num", "inStock": "num" };

   self.ListItem = function (data) {
      return {
         orderNumber: ko.observable(data.orderNumber),
         name: ko.observable(data.name),
         price: ko.observable(data.price),
         weight: ko.observable(data.weight),
         size: ko.observable(data.size),
         inStock: ko.observable(data.inStock),
         id: ko.observable(data.id),
         itemState: ko.observable(data.itemState || undefined)
      };
   }

   self.connectionStatus = ko.observable("Not connected!");

   self.addButtonVisible = ko.observable(true);



   /**************************************
   *  Fill the model                     *
   ***************************************/

   // +
   // fill items list after initial connect or reconnect
   self.fillList = function (res) {
      // clear list since this is also called after reconnect
      self.listData([]);

      // result list may be empty
      if(res === null || res.length === 0) {
         // needs some proper error handling
         return;
      }

      // fill grid with records
      res.forEach(function (itemData) {
         self.listData.push(new self.ListItem(itemData));
      })

      // set focus & display details for first list element
      self.displayDetails(vm.listData()[0]);
   }




   /**************************************
   *  Display & Switch details           *
   ***************************************/

   self.displayDetails = function(listItem, event) {

      self.switchWarning(false);

      // fill detailsEditable
      self.detailsIds.forEach(function(key) {

         var property = self.detailsEditable[key];

         property.displayedValue(listItem[key]());

         property.storedValue(listItem[key]());

         // reset updated state
         property.hasBeenUpdated(false);
      })

      // store for other checks
      self.detailsCurrent = listItem;
      
      // switch highlighting to displayed
      if (listItem.itemState() !== 'isNew') {
         listItem.itemState('isBeingDisplayed');
      }

      // if previously highlighted item !== current item, and not shown as being deleted, remove highlighting
      if (self.detailsPrevious && self.detailsPrevious.index() !== listItem.index() && self.detailsPrevious.itemState() !== "isBeingDeleted") {
         self.detailsPrevious.itemState('');
      }
      self.detailsPrevious = self.detailsCurrent;

      self.focusOnOrderNumber(true); // browser scrolls if focussed element not in view!

   };

   self.switchDetailsDisplayed = function(listItem, event) {

      // exclude clicks on an already displayed item
      if (self.detailsCurrent === listItem) {
         console.log("clicked on already selected item");
         return;
      }

      // special case: new item and no data entered yet
      // --> simply delete item
      if (self.detailsCurrent.itemState() === "isNew" && !self.detailsDirty() && listItem.itemState() !== "isNew") {

         // delete the new item, no notification sent
         self.listData.splice(-1, 1);
         self.displayDetails(listItem, event);

         self.addButtonVisible(true);
      }
      // no data changed: switch to new item
      else if (!self.detailsDirty()) {
         self.displayDetails(listItem, event);
      }
      // data changed, would we be lost on switch
      // --> display switch warning
      else {
         self.switchWarning(true);
      }
   };



   /*********************************************
   *  Edit details, cancel edit & store edited  *
   *********************************************/

   // format input on fields in item details box
   self.mangleInputs = function(viewmodel, event) {
      
      // block non-numeric input on numeric input fields
      if (self.inputs[event.target.id] === "num") {
         // self.session.log("evt", event.keyCode);
         if (event.keyCode > 57 && event.keyCode !== 190) {
            return false;
         }
      }
      
      return true; // knockout.js otherwise prevents the default action
   };

   self.normalizeSet = function(set) {
      
      for (var i in set) {
         
         // backend expects numerical values for certain fields
         // either parse to numerical, or remove field from save set
         if (self.inputs[i] === "num" && set[i] !== "") {
            set[i] = parseFloat(set[i], 10);
         }
         else if (self.inputs[i] === "num" && set[i] === "") {
            delete set[i];
         }

      }
      return set;
   };

   // +
   // store new item or update stored item
   self.saveDetailsEdits = function() {

      var saveSet = {};
      for (var i in self.inputs) {
         saveSet[i] = self.detailsEditable[i].displayedValue();
      }
      // if we're updating an existing item, we need to add its id
      if (self.detailsCurrent.itemState() != 'isNew') {
         saveSet.id = self.detailsCurrent.id();
      }

      self.normalizeSet(saveSet);

      // set call URI depending on creating new item or updating existing one
      var callURI = self.detailsCurrent.itemState() === 'isNew' ? 'form:create' : 'form:update';

      self.session.call(callURI, [], saveSet, { disclose_me: true }).then(
         function(res) {
            console.log("res", res);

            //// use return from DB for this
            for (var i in res) {
               if (res.hasOwnProperty(i)) {
                  self.detailsCurrent[i](res[i]);   
               }                  
            }

            // display details to clear field states + set button states
            self.displayDetails(self.listData()[self.detailsCurrent.index()]);

            // additional actions when we've created a new item
            if (self.detailsCurrent.itemState() === 'isNew') {
               // re-enable the 'add item' button
               self.addButtonVisible(true);
               // set item state
               self.detailsCurrent.itemState('isBeingDisplayed');
            }

         },
         self.session.log
      );
      
   };

   // +
   // cancel editing of the item in details view
   self.cancelDetailsEdits = function() {
      // check whether this is a new item
      if (self.detailsCurrent.itemState() === 'isNew') {
         // delete item from list
         self.listData.splice(self.detailsCurrent.index(), 1);
         // set focus to top of the list and display the details for this
         self.displayDetails(self.listData()[0]);
         // re-enable the 'add item' button
         self.addButtonVisible(true);
      }
      else {
         self.displayDetails(self.listData()[self.detailsCurrent.index()]);
      }
   };

   /**************************************
   *  Update an Item                        *
   ***************************************/

   // handle PubSub event for item update
   self.onItemUpdated = function (args, kwargs, details) {

      var update = kwargs;
      // 
      // below could be replaced with a getItemFromId
      // 
      var index = self.getIndexFromId(update.id);
      var item = self.listData()[index];

      // update locally stored values that habe been updated remotely
      for (var i in update) {
         if(update.hasOwnProperty(i)) {
            item[i](update[i]);
         }
      }

      // update the details view if this shows the updated item
      if (self.detailsCurrent.id() === update.id) {

         self.displayDetails(item);

         // temporary highlighting of the changed details
         for (var i in update) {
            if (update.hasOwnProperty(i) && i != "id" ){
               self.detailsEditable[i].hasBeenUpdated(true);
               (function(i) {
                     window.setTimeout(function() {
                        console.log(i + " hasBeenUpdated = false");
                           self.detailsEditable[i].hasBeenUpdated(false);
                     }, 1400);
               })(i);
            }
         }
      }

      // temporary highlighting of the list item
      var previousItemState = item.itemState();
      item.itemState("hasBeenEdited");
      window.setTimeout(function() { item.itemState(previousItemState); }, 1400);
   }



   /**************************************
   *  Add an Item                        *
   ***************************************/

   // +
   // add a new, blank item
   self.addListItem = function() {
      // block the 'add item' button
      self.addButtonVisible(false);

      // create the item
      var itemData = {
         "orderNumber": "",
         "name": "",
         "weight": "",
         "size": "",
         "inStock": "",
         "itemState": "isNew",
         "price": ""
      };
      var item = new self.ListItem(itemData);

      // add to our model
      self.listData.push(item);
     
      // display in details view
      self.displayDetails(item);
   };

   // +
   // handle PubSub event for item creation
   self.onItemCreated = function (args, kwargs, details) {
      
      var itemData = kwargs;
      var item = new self.ListItem(itemData)
      self.listData.push(item);

      // highlight the newly created item
      item.itemState("hasBeenCreated");
      window.setTimeout(function() { item.itemState(''); }, 1000);
   }




   /**************************************
   *  Delete an item                     *
   ***************************************/

   // +
   // delete triggered locally via delete button on list item
   self.triggerDelete = function( listItem, event ) {
      self.session.call("form:delete", [listItem.id()], {}, { disclose_me: true }).then(
         function(res) {
            // console.log("item " + listItem.id() + " deleted on backend", res);
            var locallyTriggered = true;
            self.deleteListItem(listItem, locallyTriggered);
         },
         self.session.log // we should really have some error handling here - FIXME!
         );
   };

   self.deleteListItem = function (item, locallyTriggered) {

      item.itemState("isBeingDeleted");

      var timeout = locallyTriggered === true ? 500 : 1500;

      window.setTimeout(function() {
         // fade out item - CHECKME!
         item.itemState("nonDisplay");
         // set timeout to delete item after end of fade
         window.setTimeout(function() {
            var index = self.getIndexFromId(item.id());
            var id = item.id();
            self.listData.remove(item);
            self.changeFocusAfterDelete(id, index);
         }, 200);
      }, timeout);

   };

   self.changeFocusAfterDelete = function (id, index) {
      // we only need to change focus if the deleted item was currently in focus
      if (id != self.detailsCurrent.id()) {
         return;
      }
      
      // set focus to 
      var newFocus = false;
      if (self.listData().length > 0) {
         newFocus = index < self.listData().length - 1 ? index : self.listData().length - 1;
      }

      // switch to list element or to blank view
      if (newFocus !== false) {
         self.displayDetails(self.listData()[newFocus]);
      }
      else {
         // clear the details view
         // detailsCurrent already gone --> referenced object deleted
         self.detailsIds.forEach(function(id) {
            self.detailsEditable[id].displayedValue("");
            self.detailsEditable[id].storedValue("");
         })
         // self.addListItem();
      }
   };

   // +
   // handle PubSub event for item deletiong
   self.onItemDeleted = function (args) {
   
      var id = args[0];
      console.log("onItemDeleted", id);   

      // get the item we need to delete
      var item = self.listData()[self.getIndexFromId(id)];
      var locallyTriggered = false;

      self.deleteListItem(item, locallyTriggered);
   }




   /**************************************
   *  Reset the ViewModel                *
   ***************************************/

   // +   
   // local user requests data reset
   self.requestDataReset = function() {
      self.session.call("form:reset", [], {}, { disclose_me: true }).then(
         function(res) {
            self.resetData(res);
         }, self.session.log
      );
   };

   self.resetData = function (data) {
      console.log("resetData", data);

      self.displayResetNotice(true);
      setTimeout(function() {
         self.displayResetNotice(false);
      }, 1200);

      self.fillList(data);
   }; 

   // +
   // handle PubSub event for data reset
   self.onDataReset = function (args, kwargs, details) {
      self.resetData(args);
   };  




   /*********************************
   *  Helper methods & miscellany   *
   *********************************/
  

   self.getIndexFromId = function (id) {
      var index;
      for (var i = 0; i < vm.listData().length; i++) {
         if (vm.listData()[i].id() === id) {
            index = vm.listData()[i].index();
         }
      }
      return index;
   }

   self.helpShown = ko.observable(false);
   self.toggleHelp = function (viewmodel, event) {
      console.log("toggleHelp", event);
      self.helpShown(!self.helpShown());
   }

}