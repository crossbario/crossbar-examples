/******************************************************************************
 *
 *  Copyright 2012-2013 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

var examineMe,
    channelBaseUri = "http://crossbar.io/crossbar/demo/autocomplete#",
    session = null;

// works
$(document).ready(function() {
   updateStatusline("Not connected.");

   setupDemo();

   connect();
});

// works
function connect() {
   // turn on WAMP debug output
   //ab.debug(true, false, false);

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
                         sessionIdent: "MyFormSession"}
      },
      // session open handler
      function (newSession) {
         session = newSession;
         updateStatusline("Connected to " + session.wsuri() + " in session " + session.sessionid());

         session.prefix("api", channelBaseUri);

         // make call to establish whether necessary oracle connection is available
         session.call("api:search", "a", { "after": 0, "limit": 10 }).then(ab.log, onOraCallError);

         session.call("api:count", "").then(function(count) {
            var formatedCount = parseInt(count/1000) + "." + parseInt((count/1000 - parseInt(count/1000))*1000);
            vm.totalRecords(formatedCount);
         }, ab.log);
      },
      // session close handler
      function (code, reason, detail) {
         session = null;
         updateStatusline(reason);
      }
   );


}

function setupDemo() {

   // apply the view model bindings
   ko.applyBindings(vm);

   // set focus to the input box
   document.getElementById("enteredName").focus();

   // hide the box initially
   updateSuggestions({ "display": false });

   $("#helpButton").click(function() {
      $(".info_bar").toggle();
   });

}

var vm = new ViewModel(); // instantiates the view model and makes its methods accessible

function ViewModel() {

   var self = this;


   self.enteredName = ko.observable("");
   self.sendChange = function() {
      selectField = "name";
      selectValue = self.enteredName();
      onSelectorChanged();
   };
   self.enteredName.subscribe(self.sendChange);

   self.totalRecords = ko.observable();

   self.handleCursor = function(viewmodel, event) {
      switch (event.which) {
         case 13:
            if (self.enteredName !== "" && currentItemId !== null) {
               // ignores the case when something has been entered,
               // but the processing of the entry hasn't yet extended to setting
               // the correct currentItemID:
               //    - no initial currentItemID --> enter doesn't do anything
               //    - incorrect currentItemID --> selects wrong(previous) item
               // FIXME ?
               selectItem();
            }
            break;
         case 38:
            // keydown events are processed to move the selection in the suggestions box
            // keyup events are used to determine when the user has stopped moving the
            // cursor, and the request for the item details is only sent then, based on the
            // global 'currentItemId' variable that was set by the keydown handler
            if (event.type === "keydown") {
               cursorMove("up");
               return false; // prevent default, which sets the cursor to the beginning of the text box in chrome
            }
            else if (event.type === "keyup") {
               // needs to catch up at the beginning of the results list - FIXME
               // = item details displayed === item details to request
               if (currentDetailsId !== currentItemId) {
                  requestItemDetails(currentItemId);
               }
            }
            break;
         case 40:
            if (event.type === "keydown") {
               cursorMove("down");
               return false;
            }
            else if (event.type === "keyup") {
               // needs to catch down at the end of the results list - FIXME
               if (currentDetailsId !== currentItemId) {
                  requestItemDetails(currentItemId);
               }
            }
            break;
         default:
            break;
      }

      return true; // retain default behaviour
   };

   self.suggestionClicked = function(item) {
      // get the item id from the html list element id
      var itemId = item.id;
      selectItem(itemId);
   };

   self.autocompleteSuggestions = ko.observableArray([]);

   self.name = ko.observable("");
   self.birthdate = ko.observable("");
   self.birthplace = ko.observable("");
   self.deathdate = ko.observable("");
   self.deathplace = ko.observable("");
   self.descr = ko.observable("");

   self.detailsGreyedOut = ko.observable(true);
   self.selectorEmpty = ko.observable(true);

   self.requestsForAutocompleteSuggestions = ko.observable(0);
   self.receivedAutocompleteSuggestions = ko.observable(0);
   self.currentCacheSize = ko.observable(0);
   self.requestedDetailsStatic = ko.observable(0);
   self.currentMatches = ko.observable(0);

}




function onOraCallError(error) {
   ab.log("oce", error);
   $("#error_overlay").show();
}

// global state variables
var suggestionsArrays = []; // contains the one or more arrays with autocomplete suggestions
var maxSuggestionsArraysLength = 3; // maximum length of arrays to keep stored locally. should be at least 3.

var arrayPosition = [0, 0]; // current position within the suggestions cache starting from which the currently displayed suggestions in the box are extracted
// should better be:
   // var currentArray = 0;
   // var positionInArray = 0;
   // please REFACTOR
var arrayCounter = null; // the position of the currently used array within the total result set, e.g. 5 = the fifth array received
var endInLastArray = false; // flag for end of the full results set contained in the last array in the arrays

var limit = 30; // max number of suggestions in the results set from the DB
var comfortZone = 10; // distance from the beginning/end of an array at which check for next/previous array is initiated

var listPosition = 0; // current position within the items displayed in the box

var currentItemId = null; // the id of the currently highlighted item in the box
var maxDisplay = 10; // max number of suggestions to display in the box

var currentDetailsId = null; // the id of the item shown in the details view
var currentSubscriptions = []; // stores any current subscriptions as strings that can be used directly as the argument for unsubscribe

var selectField = null; // the name of the key for the values which autocomplete filters
var selectValue = null; // the current value which to prefix match

var nextSetRequested = false; // next item set requested, but not yet received
var previousSetRequested = false; // previous item set requested, but not yet received

function logState() {
   ab.log(
      "arrays", suggestionsArrays.length,
      "arrayposition 0", arrayPosition[0],
      "arrayposition 1", arrayPosition[1],
      "arrayCounter", arrayCounter,
      "endinlast", endInLastArray
      );
}



function selectItem(itemId) {
   ab.log("sel", itemId);
   // reached via 'enter' or click on an item
   // via enter does not pass an itemId, since the details
   // were already requested on the highlighting of the item

   // clear the selection input + suggestions box
   vm.enteredName("");

   var cs = {};
   cs.items = [];
   cs.above = false;
   cs.below = false;
   cs.display = false;
   updateSuggestions(cs);

   // reset global state
   suggestionsArrays = [];
   listPosition = 0;
   arrayPosition = [0, 0];
   // currentItem = {}; - not, because response for details RPC might still be outstanding

   // request details to display
      //// first request if clicked
   if (itemId) {
      ab.log("request");
      currentItemId = itemId;
      requestItemDetails(itemId);
   }
      //// additional request on enter, since the details are cleared
      //// when the selection input is cleared
   else {
      requestItemDetails(currentItemId);
   }
}

// works
function requestItemDetails(itemId) {
   var self = this;

   // sends request for item details
   currentItemId = itemId; // set to enable check whether return still needed (???? should be set by the calling function, this here should not change values outside of its functional scope)

   // for static details
   session.call("api:get", itemId).then(function(details) {
      // check if item still current
      if (details.id === currentItemId) {
         updateDetails(details);
         // set global currentDetail value
         currentDetailsId = details["id"];
      }
   }, ab.log);

   // increase requests counter
   vm.requestedDetailsStatic(vm.requestedDetailsStatic() + 1);

}

/************************************************
*     handling of input on the box              *
*************************************************/

function cursorMove(direction) {
   // blank the details
   blankOutDetails();

   //change selection within the currently displayed items
   var positionChange = direction === "down" ? 1 : -1;
   var newPosition = listPosition + positionChange;

   // limit the maxMoveWithinBox to suggestions list length
   // if list completely displayed in suggestions box
   var listItems = $("#suggestionsList").children("li");
   var listItemCount = listItems.length;
   var maxMoveWithinBox = listItemCount < maxDisplay ? listItemCount : maxDisplay;

   // movement within currently displayed items possible?
   if (moveWithinList(newPosition, maxMoveWithinBox, listItems)) {
      return;
   }

   // prevent movement at beginning and end of the list
   if (checkBeginningOrEnd(newPosition, maxMoveWithinBox)) {
      return;
   }

   // check whether comfort zone for the present array has been reached,
   // for position in first array & not the beginning of the results set
   // or last array and end of the results set not in this array
   if ((arrayPosition[0] === 0 && arrayCounter !== 0) || (arrayPosition[0] === suggestionsArrays.length - 1 && !endInLastArray)) {
      checkComfortZone(newPosition);
   }

   // update the array positions
   updateArrayPositions(newPosition);

   // update list position
   if (newPosition < 0) {
      listPosition = 0;
   }
   else if (newPosition > vm.autocompleteSuggestions.length - 1) {
      listPosition = vm.autocompleteSuggestions().length - 1;
   }

   // display the updated set of items in the box
   var cs = getCurrentSuggestionsSet();
   updateSuggestions(cs);

   // set the currentItemId
   currentItemId = cs.items[listPosition].id;
}

/*
   returns the current set of suggestions to display in the
   suggestions box
*/
function getCurrentSuggestionsSet() {
   var cs = {};

   var toggles = toggleAboveBelow();
   cs.above = toggles["above"];
   cs.below = toggles["below"];

   cs.items = getSuggestionsItemSet();
   cs.position = listPosition;

   return cs;
}

/*
   Checks whether the curso movement can be executed by changing the
   position with in the currently displayed suggestions list in the box,
   without any scrolling
*/
function moveWithinList(newPosition, maxMoveWithinBox, listItems) {
   // catch special case: no items in list (nothing entered yet, no results back yet)
   if (maxMoveWithinBox === 0) {
      return true;
   }

   if (newPosition >= 0 && newPosition < maxMoveWithinBox) {

      // update list position
      listPosition = newPosition;

      // change highlighting to item at position
      updateSuggestions({ "position": listPosition });

      // change currentId
      var newId = listItems[listPosition].id;
      currentItemId = parseInt(newId, 10);
      return true;
   }
   return false;
}

/*
   Checks whether any more scrolling is possible in principle
*/
function checkBeginningOrEnd(newPosition, maxMoveWithinBox) {
   // beginning of the suggestions reached
   max = maxMoveWithinBox;

   if (newPosition === -1 && arrayCounter === 0 && arrayPosition[1] === 0) {
      ab.log("at the top");
      return true;
   }

   // end of the suggestions reached
   if (endInLastArray /* no new arrays to get */ && listPosition === maxMoveWithinBox - 1 /* list position is at the end of the list */ && suggestionsArrays[suggestionsArrays.length - 1][suggestionsArrays[suggestionsArrays.length - 1].length - 1].id === vm.autocompleteSuggestions()[vm.autocompleteSuggestions().length - 1].id
         /* id of last element in this last array matches id of the last item in the suggestions box */
      ) {
      ab.log("the end");
      return true;
   }
}

/*

*/
function updateArrayPositions(newPosition) {
   // we are scrolling, so adjust the positions for getting the new cut

   if ((arrayPosition[1] + newPosition) < 0) {
      // new position in previous array;

      arrayPosition[0] = arrayPosition[0] - 1;
      arrayCounter = arrayCounter - 1; // decrease array counter
      arrayPosition[1] = (suggestionsArrays[arrayPosition[0]].length - 1); // with position change = 1 position, this should work - CHECKME
   }
   else if (arrayPosition[1] + newPosition - listPosition > suggestionsArrays[arrayPosition[0]].length) {
      // new position within next array
      arrayPosition[0] = arrayPosition[0] + 1;
      arrayCounter = arrayCounter + 1;
      ab.log("scroll into next array", arrayPosition[0], arrayCounter);
      arrayPosition[1] = 0; // with position change = 1 position, this should work - CHECKME
   }
   else {
      arrayPosition[1] = arrayPosition[1] + newPosition - listPosition;
   }
}

// buggy -try "Gauss" and see the behaviour of the below indicator
function toggleAboveBelow() {
   var toggles = {};
   // not in first array, or offset not at beginning of an array
   if (arrayPosition[0] > 0 || arrayPosition[1] > 0) {
      toggles.above = true;
   }
   else {
      toggles.above = false;
   }
   // not in last array, or
   // in last array & current set does not include the end of the array
   if (endInLastArray /* no new arrays to get */ && suggestionsArrays[suggestionsArrays.length - 1][suggestionsArrays[suggestionsArrays.length - 1].length - 1].id === vm.autocompleteSuggestions()[vm.autocompleteSuggestions().length - 1].id /* id of last element in this last array matches id of the last item in the suggestions box */
      ) {
      toggles.below = false;
   }
   else {
      toggles.below = true;
   }
   return toggles;
}

// works except for the branching that handles next array not there yet
/*
   Returns the set of items to currently display in the suggestions box
*/
function getSuggestionsItemSet() {
   var self = this;

   this.getAdditional = function() {
      var additionalNeeded = maxDisplay - slice.length;
      for (var i = 0; i < additionalNeeded; i++) {
         slice.push(suggestionsArrays[arrayPosition[0] + 1][i]);
      }
      return slice;
   };

   // gets a set of size maxDisplay (or smaller if at end of last array)
   // needs to handle the case that this extends across two arrays
   // assumes that the individual arrays are larger than the maximum number of items to display
   // i.e. that a request can in principle be fulfilled from a single array
   var extractedItemSet = [];
   // slice from the present position within the present array
   var slice = suggestionsArrays[arrayPosition[0]].slice(arrayPosition[1], arrayPosition[1] + maxDisplay);

   // check if this is smaller than maxDisplay, and exclude cases where this is
   // because the end of the full results set has been reached
   if (slice.length < maxDisplay && // results set not big enough
      ((arrayPosition[0] < suggestionsArrays.length - 1) || // not last array
      (arrayPosition[0] === suggestionsArrays.length - 1 && !endInLastArray))) { // last array, but more should come

      // get missing elements from the next array

      var additionalNeeded = maxDisplay - slice.length;
      // check that the next array already exists
      // if not, block, recheck periodically, then progress once its there
      if (suggestionsArrays[arrayPosition[0] + 1]) {
         return self.getAdditional();
      }
      else {
         // this branching doesn't work properly yet - FIXME
         ab.log("not present yet - FIXME");

         // function checkForNextArrayExists(timeout) {
         //    window.setTimeout(
         //       function() {
         //          if (suggestionsArrays[arrayPosition[0] + 1]) {
         //             ab.log("array delivered");
         //             return self.getAdditional();
         //          }
         //          else {
         //             checkForNextArrayExists(20);
         //          }
         //       }, timeout
         //    );
         // }
      }
   }
   else {
      // slice extends to the end, so just return it
      return slice;
   }

   // Alternative implementation of the above, works as far as it's there
   // written during bug hunting - PICK THE ONE THAT SEEMS NICER
   // // check how to handle slices that are shorter than maxDisplay
   // if (slice.length < maxDisplay) {
   //    // ab.log("shorter slice");
   //    // slice shorter because there are no more items in the full results set
   //    if (arrayPosition[0] === suggestionsArrays.length - 1 && // is last array
   //    endInLastArray) // end in last array
   //    {
   //       // shorter slice is fine
   //       // ab.log("fine, because end of results set");
   //       // should never occur - this would be scrolling that leads to a shorter set
   //       // should be caught before in cursorMove
   //       return slice;
   //    }
   //    else {
   //       // we need more results from another array
   //       if (arrayPosition[0] === suggestionsArrays.length - 1) {
   //          // the array we need isn't there yet
   //          // just log this for now
   //          ab.log("next array should be there, but isn't yet");
   //       }
   //       else {
   //          // ab.log("calling add from next array");
   //          return self.getAdditional();
   //       }
   //    }
   // } else {
   //    // console.log("slice big enough")
   //    return slice;
   // }
}



// incomplete
/*
   Checks whether the new position within the locally cached results
   necessitates the request of a previous/next slice of
   the results set
*/
function checkComfortZone(newPosition) {
   var newArrayOffset = arrayPosition[1] + newPosition;

   // within the beginning comfort zone of an array, and no preceding array present
   if (newArrayOffset < comfortZone) {
      console.log("upper comofort zone, prevArrayexists: " + suggestionsArrays[arrayPosition[0] - 1] + " request already sent: " + previousSetRequested);
      if (!suggestionsArrays[arrayPosition[0] - 1] && !previousSetRequested) {
         // get preceding cut in results set

         // if the present array is the first one in the full set, do nothing
         if( arrayCounter === 0 ) {
            console.log("first array in results set, returning");
            return;
         }

         // get the previous cut in the results set
         var set = {};
         // find the lowest id in the current array
         // var lowestId = getLowestId(suggestionsArrays[arrayPosition[0]]);
         // arrays now appear to be ordered, so just get the first id
         var lowestId = suggestionsArrays[arrayPosition[0]][0].id;

         set.before = lowestId;
         set.limit = limit;
         previousSetRequested = true;
         session.call("api:search", selectValue, set).then(
            function(res) {
               previousSetRequested = false;
               // handle empty sets (needs to be fixed on the back end) - FIXME / REMOVE ME
               if (res.length === 0) {
                  ab.log("received empty set - backend problem");
                  return;
               }

               suggestionsArrays.unshift(res);
               // cull the array at its end if necessary
               if (suggestionsArrays.length > maxSuggestionsArraysLength) {
                  suggestionsArrays.splice(maxSuggestionsArraysLength - 1, 1);
               }

               // increase the received counter
               vm.receivedAutocompleteSuggestions(vm.receivedAutocompleteSuggestions() + res.length);
               // update the cache indicator
               var cacheSize = 0;
               for (var i = 0; i < suggestionsArrays.length; i++) {
                  cacheSize += suggestionsArrays[i].length;
               }
               vm.currentCacheSize(cacheSize);

            }, ab.log);

      }
   }
   // within the end comfort zone of an array, and no subsequent array present
   else if (newArrayOffset > ((suggestionsArrays[arrayPosition[0]].length - 1) - comfortZone)) {
      if (!suggestionsArrays[arrayPosition[0] + 1] && !nextSetRequested) {
         console.log("no next array, and not requested yet");

         // if end in last received array do nothing
         if (endInLastArray) {
            return;
         }

         // get next cut in results set
         var set = {}; // FIXME: already defined!!
         // find the highest id in the current array
         // var highestId = getHighestId(suggestionsArrays[arrayPosition[0]]);
         // arrays now appear to be ordered, so just get the first id
         var currentArray = suggestionsArrays[arrayPosition[0]];
         var highestId = currentArray[currentArray.length - 1].id;


         set.after = highestId;
         set.limit = limit + 1;

         nextSetRequested = true;
         session.call("api:search", selectValue, set).then(
            function(res) {
               nextSetRequested = false;
               // handle empty sets (needs to be fixed on the back end) - FIXME / REMOVE ME
               if (res.length === 0) {
                  endInLastArray = true;
                  return;
               }

               // check if end of results in current cut of results set
               if (res.length === limit + 1) {
                  res.splice(res.length - 1, 1); // cut results to limit size
                  endInLastArray = false;
               }
               else {
                  endInLastArray = true;
               }
               suggestionsArrays.push(res);
               // cull the array at its beginning if necessary
               if (suggestionsArrays.length > maxSuggestionsArraysLength) {
                  suggestionsArrays.splice(0, 1);
                  arrayPosition[0] -= 1;
               }

               // increase the received counter
               vm.receivedAutocompleteSuggestions(vm.receivedAutocompleteSuggestions() + res.length);
               // update the cache indicator
               var cacheSize = 0;
               for (var i = 0; i < suggestionsArrays.length; i++) {
                  cacheSize += suggestionsArrays[i].length;
               }
               vm.currentCacheSize(cacheSize);
            }, ab.log);
      }
   }
}

// works
/*
   Evaluates the current content of the selection box
   Modifies it as needed for processing by the backend
   Sends requests for new autocomplete suggestions +
   the size of the current results set
*/
function onSelectorChanged() {
   // blank out the currently displayed details
   blankOutDetails(true);

   // reset the current matches
   vm.currentMatches(0);

   //cancelSubscriptions();

   // branching if empty string
   if (selectValue === "") {
      ab.log("select empty");
      updateSuggestions({ "display": false, "items": [] });
      vm.selectorEmpty(true);
      return;
   }
   else {
      vm.selectorEmpty(false);
   }

   // empty the suggestions list
   updateSuggestions({ "items": [] });

   // send request for suggestions to DB
   var offset = 0; // fresh set, so get from the start

   var set = {};
   //set.after = offset;
   set.after = 0; // hard-coded for now, FIXME
   set.limit = limit + 1;

   // filter any occurences of ',' from the selectValue
   // so that e.g. "einstein, albert" is equivalent to "einstein albert",
   // which the back-end uses as the searchable string
   if (selectValue.indexOf(',') !== -1) {
      var split = selectValue.split(',');
      var united = "";
      for (var i = 0; i < split.length; i++) {
         united += split[i];
      }
      selectValue = united;
      ab.log("United", selectValue);
   }

   //ab.log("ssent", selectValue, set);
   session.call("api:search", selectValue, set).then(onNewSuggestions, ab.log);

   // in parallel: persons count for current string
   session.call("api:count", selectValue).then(function(count) {
      vm.currentMatches(count);
   }, ab.log);

   //session.call("api:get-autocomplete-suggestions", selectField, selectValue, offset, limit + 1).then(onNewSuggestions, ab.log);

   // increase requests counter
   vm.requestsForAutocompleteSuggestions(vm.requestsForAutocompleteSuggestions() + 1);
}


// works
/*
   Handles new autocomplete suggestions results set
   Checks whether the current set contains the entire results set
   Sends the relevant part of the set on to be displayed in the
   suggestions box
*/
function onNewSuggestions(data) {
   // extract the id of the first item + send the RPC to get the details for this

   // catch special case: selector box empty, receive delayed suggestions from previously
   // sent search
   if (vm.selectorEmpty()) {
      return;
   }

   // catch special case: no selections since search string does not match on anything
   if (data.length === 0) {
      //ab.log("data", data);
      return;
   }

   var suggestions = data;
   var firstItemId = suggestions[0].id;
   requestItemDetails(firstItemId);
   currentItemId = firstItemId;

   // check if end of results in current cut of results set
   if (suggestions.length === limit + 1) {
      suggestions.splice(data.length - 1, 1); // cut results to limit size
      endInLastArray = false;
   }
   else {
      endInLastArray = true;
   }

   // store the items and set variables
   suggestionsArrays = []; // delete old cache
   suggestionsArrays[0] = suggestions;
   listPosition = 0;
   arrayPosition = [0, 0]; // no offset yet
   arrayCounter = 0; // first array in the entire set

   // increase the items counter
   vm.receivedAutocompleteSuggestions(vm.receivedAutocompleteSuggestions() + suggestionsArrays[0].length);
   // update the cache indicator
   vm.currentCacheSize(suggestionsArrays[0].length);

   // initialize the suggestions box
   var itemsToDisplay = suggestionsArrays[0].slice(0, maxDisplay);
   var cs = {};
   cs.items = itemsToDisplay;
   cs.position = 0;
   cs.display = true;
   cs.above = false;
   if (suggestionsArrays[0].length > maxDisplay) {
      cs.below = true;
   }
   else {
      cs.below = false;
   }
   updateSuggestions(cs);

}

// works
function autoCompleteSuggestion(data) {
   return {
      name: data.name,
      id : data.id
   };
}


/************************************
 *        UI update functions       *
 ************************************/
// works
/*
   Handles display & updates contents of the suggestions box
*/
function updateSuggestions(data) {
   // receives a dictionary containing:
   //    - suggestion list items ("items", optional)
   //    - current navigation position within the list ("position", optional)
   //    - toggle for display of "more above" and "more below" indicators ("above"/"below", optional)
   //    - toggle for display of the box ("display", optional)
   // fully empty dict

   // fill box with suggestion items
   if ("items" in data) {
      // clear old data
      vm.autocompleteSuggestions([]);
      // add new data
      var items = data.items;

      if (items.length > 0) {

         for (var i = 0; i < items.length; i++) {
            vm.autocompleteSuggestions.push(new autoCompleteSuggestion(items[i]));
         }
      }
   }

   // toggle display of moreAbove & moreBelow indicators
   if ("above" in data && data.above === true) {
      $("#moreAbove").show(20);
   }
   if ("above" in data && data.above === false) {
      $("#moreAbove").hide(20);
   }
   if ("below" in data && data.below === true) {
      $("#moreBelow").show(20);
   }
   if ("below" in data && data.below === false) {
      $("#moreBelow").hide(20);
   }

   // toggle display of box
   if ("display" in data && data.display === true) {
      $("#autocompleteBox").show(300);
   }
   if ("display" in data && data.display === false) {
      $("#autocompleteBox").hide(300);
   }

   // move the highlighting
   if ("position" in data) {
      var listItems = $("#suggestionsList").children("li");
      var position = data.position;


      for (var i = 0; i < listItems.length; i++) {

         if (i === position) {
            $(listItems[i]).addClass("highlighted");
         }
         else {
            if ($(listItems[i]).has(".highlighted")) {
               $(listItems[i]).removeClass("highlighted");
            }
         }
      }
   }
}

// works
function updateDetails(data) {
   examineMe = data;
   // receives a single dictionary with the keys listed below in dataMap

   // change back from greyed out state
   vm.detailsGreyedOut(false);

   // mapping of the dictionary keys to observables in the details view
   var dataMap = {
      "name": vm.name,
      "birthdate": vm.birthdate,
      "birthplace": vm.birthplace,
      "deathdate": vm.deathdate,
      "deathplace": vm.deathplace,
      "descr": vm.descr
   };

   // format the dates
   if (data.birthdate !== "") {
      var birthDate = new Date(data.birthdate.replace(/-/g, '/').replace(/T/, ' ').replace(/\+/, ' +'));
      var birthDateFormatted = birthDate.getFullYear() + "-" + (birthDate.getMonth() + 1) + "-" + birthDate.getDate();
      data.birthdate = birthDateFormatted;
   }
   if (data.deathdate !== "") {
      var deathDate = new Date(data.deathdate.replace(/-/g, '/').replace(/T/, ' ').replace(/\+/, ' +'));
      var deathDateFormatted = deathDate.getFullYear() + "-" + (deathDate.getMonth() + 1) + "-" + deathDate.getDate();
      data.deathdate = deathDateFormatted;
   }


   // update the observables bound to the data display fields
   for (var key in dataMap) {
      if (dataMap.hasOwnProperty(key)) {
         (dataMap[key])(data[key]);
      }
   }

}

// works
function blankOutDetails(greyOut) {
   // no args since there is currently only one details view to operate on
   // send empty details set to clear fields
   var emptyDetails = {
      "name": "",
      "birthdate": "",
      "birthplace": "",
      "deathdate": "",
      "deathplace": "",
      "descr": ""
   };
   updateDetails(emptyDetails);

   // grey out the details display areas
   if (greyOut) {
       vm.detailsGreyedOut(true);
   }
}

function updateStatusline(status) {
   if (session && session._websocket && session._websocket.extensions && session._websocket.extensions !== "") {
      $(".statusline").text(status + " [" + session._websocket.extensions + "]");
   } else {
      $(".statusline").text(status);
   }
}
