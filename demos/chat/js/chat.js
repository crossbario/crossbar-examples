/******************************************************************************
 *
 *  Copyright 2012-2014 Tavendo GmbH.
 *
 *  Licensed under the Apache 2.0 license
 *  http://www.apache.org/licenses/LICENSE-2.0.html
 *
 ******************************************************************************/

"use strict";

var demoRealm = "crossbardemo";
var demoPrefix = "io.crossbar.demo";


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




var initialChannel = null,
    currentSubscription = null,
    presetNicks = ["Nick", "Knatterton", "Micky", "Maus", "Donald", "Bruce", "Wayne", "Clark", "Kent", "Sarah", "Connor", "Mary", "Shelley", "Rosemary", "Wilma", "Louis", "Selina", "Barbara", "Gordon", "Herbert", "The Count"],
    nick,
    oldNick,
    assignedNicks = {},
    nickColors = ["black", "orange", "green", "blue", "red"],
    sess = null,
    retryCount = 0,
    retryDelay = 2,
    oldHash = window.location.href,
    isReconnect = false;

var chatWindow = null;


updateStatusline("Not connected.");

// check for controller channel id in the URL
var windowUrl = document.URL; // string
if (windowUrl.indexOf('#') !== -1) {
   initialChannel = windowUrl.split('#')[1];
} else {
   console.log("no fragment yet");
}

setupDemo();

connect();


function switchChannel(oldChannelID, newChannelID) {
   console.log("switchChannel called");
   // either oldChannelID or newChannelID could be null = start page with no demo selected
   if (oldChannelID && currentSubscription !== null && currentSubscription.session.isOpen === true) {
      currentSubscription.unsubscribe().then(
         function() {
            console.log("successful unsubscribe");
         },
         function(error) {
            console.log("unsubscribe error ", error);
         }
      );
   }

   sess.subscribe("api:" + newChannelID, onMessage).then(
      function(subscription) {
         console.log("subscriped", subscription);
         currentSubscription = subscription;
      },
      function(error) {
         console.log("subscription failed ", error);
      }
   );

   // clear messages box
   $("#messages_box").html('');

   // set the second instance link
   $('#secondInstance').attr('href', window.location.pathname + '#' + newChannelID);

   // clear the unread chat message indicator if set
   $("#show_chat_window").removeClass("message_received");
}


function updateStatusline(status) {
   $(".statusline").text(status);
};


function connect() {

   // the WAMP connection to the Router
   //
   var connection = new autobahn.Connection({
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

   connection.onopen = function (session) {
      sess = session;

      sess.prefix("api", demoPrefix + ".chat");

      updateStatusline("Connected to " + wsuri);

      console.log("initialChannel", initialChannel, isReconnect);

      // if window url contained channel id, trigger the necessary actions
      if (initialChannel && !isReconnect) {
         switchChannel(null, initialChannel);
         changeChannelIndicators(initialChannel);
         isReconnect = true;
      }

   };

   connection.onclose = function() {
      console.log("connection closed ", arguments);
   }

   connection.open();

}


function onHashChanged(evt) {
   console.log("onHashChanged", oldHash);

   var newUrl = window.location.href;
   var oldUrl = oldHash;
   oldHash = newUrl;

   var newChannelID;
   var oldChannelID;

   if (newUrl.indexOf('#') !== -1) {
      newChannelID = newUrl.split('#')[1];
   }
   else {
      newChannelID = null;
   }
   if (oldUrl.indexOf('#') !== -1) {
      oldChannelID = oldUrl.split('#')[1];
   }
   else {
      oldChannelID = null;
   }

   switchChannel ( oldChannelID, newChannelID );

   changeChannelIndicators ( newChannelID );
}

function changeChannelIndicators ( newChannelID ) {

   // indicate presently picked channel via highlighting
   var channelSelectors = $(".chat_channel_selector"),
       currentChannel;

   for (var i = 0; i < channelSelectors.length; i++) {

      if ("ch" + (i + 1) == newChannelID) {

         $(channelSelectors[i]).addClass("channel_selected");
         currentChannel = i + 1;
      }

      else if ($(channelSelectors[i]).hasClass("channel_selected")) {

         $(channelSelectors[i]).removeClass("channel_selected");
      }
   }

   // set the channel title on the chat window
   $("#channel_title").text("Channel " + currentChannel);
}


function setupDemo() {
   chatWindow = $("#chat_window");

   // add 'onhashchange' event to trigger the channel change + chat window display
   window.onhashchange = onHashChanged;

   // initial timed display of the chat window
   window.setTimeout(function() { $("#chat_window").toggle(300) }, 2300);

   // set up show + hide chat window handlers
   document.getElementById("show_chat_window").onclick = function () {

      $("#chat_window").toggle(300);

      var messagesBox = $("#messages_box")[0];

      // scroll messages box
      messagesBox.scrollTop = messagesBox.scrollHeight;

   };

   document.getElementById("hide_chat_window").onclick = function () {

      $("#chat_window").toggle(300);
      $("#show_chat_window").removeClass("message_received");

   };


   // set random preset nick
   nick = $("#nick");
   var randomNick = presetNicks[Math.floor(Math.random() * presetNicks.length)];
   nick.val(randomNick);
   oldNick = nick.val();
   getNickColor(nick.val()); // assigns a color to the nick

   // set 'enter' on chat message textarea sends message
   var messageInput = $("#message_input")[0];
   messageInput.onkeypress = function(e) {

      var e = e || event; // IE8 fix, since here the window.event, not the event itself contains the keyCode

      if (e.keyCode === 13) {

         console.log("enter");
         sendMessage(messageInput);

         return false;

      };

   };


   $("#helpButton").click(function() {

      $(".info_bar").toggle();

      if ($("#chat_window:visible").length) {
         $("#chat_window").toggle(300);
      }

   });

}

function sendMessage(messageInput) {
   console.log("send message");

   var message = messageInput.value;
   var currentNick = nick.val();

   // check if own nick has changed since last send
   if (currentNick !== oldNick) {
      changeOwnNick(currentNick);
   }
   var channel;
   var windowUrl = document.URL;
   if (windowUrl.indexOf('#') !== -1) {
      channel = windowUrl.split('#')[1];
   }

   var payload = {};
   payload.message = message;
   payload.nick = currentNick;

   sess.publish("api:" + channel, [payload], {}, {exclude_me: false});

   // clear the message input
   messageInput.value = '';
   messageInput.placeholder = '';

};

function changeOwnNick(currentNick) {

   // get the color value for the old nick
   var nickColor = assignedNicks[oldNick];

   // delete the old nick
   delete assignedNicks[oldNick];

   // add new nick with the old color
   assignedNicks[currentNick] = nickColor;

};


function getNickColor(nickString) {

   // check if nickstring has color assigned, and return this
   if (!(nickString in assignedNicks)) {

      // count the nicks
      var nickCounter = 0;
      for (var i in assignedNicks) {
         if (assignedNicks.hasOwnProperty(i)) {
            nickCounter += 1;
         }
      }

      // pick a color
      var nickColor;
      if (nickCounter <= nickColors.length) {
         nickColor = nickColors[nickCounter];
      }
      else {
         nickColor = nickColors[(nickCounter % nickColors.length)];
      }

      // add the nick and color
      assignedNicks[nickString] = nickColor;

   }

   return assignedNicks[nickString];

};


// function onMessage(topicUri, event) {
function onMessage(args, kwargs, details) {

   console.log("on message");

   addMessage(args[0]);
   // set new message highlighting on "chat" button
   $("#show_chat_window").addClass("message_received");

}

function addMessage(payload) {

   // get the parts of the message event
   var message = payload.message;
   var messageNick = payload.nick;
   var nickColor = getNickColor(messageNick);

   var messageTime = formattedMessageTime();

   var messagesBox = $("#messages_box")[0];

   // add html to messages box
   $(messagesBox).append("<p class='nick_line' style='color: " + nickColor + ";'>" + messageNick + " - <span class='message_time'>" + messageTime + "</span></p>");
   $(messagesBox).append("<p class='message_line'>" + message + "</p>");
   $(messagesBox).append("</br>");

   // scroll messages box
   messagesBox.scrollTop = messagesBox.scrollHeight;

}

function formattedMessageTime() {

   var messageTimeRaw = new Date();

   var day = messageTimeRaw.getDate();
   var month = messageTimeRaw.getMonth() + 1;
   var hours = messageTimeRaw.getHours();
   var minutes = messageTimeRaw.getMinutes();
   // add initial '0' where necessary
   minutes = minutes < 10 ? "0" + minutes : minutes;
   hours = hours < 10 ? "0" + hours : hours;

   var formattedMessageTime = hours + ":" + minutes;
   return formattedMessageTime;
};
