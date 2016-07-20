var leaderBoard = {
  maxEntries: 10,
  entries: [
    {
      id: "djsakjzvbnvjsake34",
      length: 6500,
      route: [],
      nick: "tester1", // nick is optional!
      computeNodesCurrent: 5,
      computeNodesMax: 8,
      iterationsSecond: 50
    },
    {
      id: "7584758vjsake34",
      length: 6800,
      route: [],
      nick: "gzost", // nick is optional!
      computeNodesCurrent: 3,
      computeNodesMax: 12,
      iterationsSecond: 100
    },
    {
      id: "fzueuiwhjdskaeghr4",
      length: 7800,
      route: [],
      nick: "latster", // nick is optional!
      computeNodesCurrent: 1,
      computeNodesMax: 3,
      iterationsSecond: 20
    }
  ],
  bestLength: 6500,
  lowestLength: 7800
};

// everything after nick relies on the presence of that
// otherwise: computeNodes, computeNodesMax = 1
// iterationsSecond = iterations on the single Node
// ! if we have computeNodesCurrent, iterationsSecond then we need
// monitoring for these

//
// for the main routine which handles resuts:
//
// if (length < leaderBoard.lowestLength) {
//   addToLeaderBoard(id, route, length);
// }

var addToLeaderBoard = function(id, route, length) {
  var addAtPosition = function(id, position) {
    var newEntry = {
      length: length,
      id: id,
      route: route,
    };

    // get the other information we require to fully fill this in - FIXME
    
    leaderBoard.entries.splice(position, newEntry);

    // if new first entry, update the best length
    if(position === 0) {
      leaderBoard.bestLength = length;
    }
  };

  // check where this fits in
  var isPosition = function(el, i) {
    if(el.length < length) {
      addAtPosition(id, i);
      return true;
    }
  };
  leaderBoard.every(isPosition);


  // kick out the last entry if necessary
  // and update the lowest length
  if(leaderBoard.entries.length > leaderBoard.maxEntries) {
    leaderBoard.entries.shift();
    leaderBoard.lowestLength = leaderBoard.entries[leaderBoard.entries.length - 1];
  }
};

var testAddToLeaderBoard = function() {


};
