console.log("loaded");

// below may not be correct yet - test more!!
var computeSlice = function(points, calcTime) {
   var currentPoints = points;
   var swappedPoints = null;

   // initial temperature
   var temp = 1;
   var endTemp = 0.01;
   var tempDecrease = 0.99;
   // calculate temp decrease based on calcTime
   // for the time being: decrease linearly across the time
   // var tempDropRate =

   // P: We want a fixed time for the execution of the calculation. The usual method is to reduce the temperate after each iteration, and to stop when the temperatur has reached the lowest intended value.

   // // below is used to stop the recursive loop
   // var isExpired = false;
   // setTimeout(function() {
   //    isExpired = true;
   // }, calcTime * 1000)

   var initialLength = computeLength(points);
   var currentBestLength = initialLength;

   // initial random sort of points
   swappedPoints = randomSwapTwo(points, points.length);// should this be by a constant factor or power?

   var i = 0;
   while(temp > endTemp) {
      // get current length
      var currentLength = computeLength(swappedPoints);

      // decide whether to keep the current permutation
      if(
         currentLength < currentBestLength ||
         Math.random() < Math.exp((currentLength - currentBestLength)/temp)
      ) {
         // keep and work from this
         currentPoints = swappedPoints;
      }

      if(currentLength < currentBestLength) {
         currentBestLength = currentLength;
      }

      // swap currentPoints
      swappedPoints = randomSwapTwo(currentPoints, 1);

      temp *= tempDecrease;

      console.log(i, currentLength, currentBestLength);
      i++;
   }

   return [currentPoints, currentBestLength];

}

// // length for this is 3
// var points = [
//    [1,1],
//    [1,2],
//    [2,2],
//    [2,1]
// ];

var points = [
   [1,1],
   [1,2],
   [2,2],
   [2,1],
   [5,1]
];

// var points = [
//    [3,3],
//    [5,3],
//    [3,5]
// ]

var computeLength = function(points) {
   var length = null;

   points.forEach(function(point, i) {
      if(points[i + 1]) {
         // console.log(points[i + 1], points[i]);
         var distance = computeDistance(points[i + 1], points[i]);
         length += distance;
      }
   })

   return length;
}

var computeDistance = function(firstPoint, secondPoint) {
   var distance = Math.sqrt(
      Math.pow(firstPoint[0] - secondPoint[0], 2) +
      Math.pow(firstPoint[1] - secondPoint[1], 2)
   );

   return distance;
}

var deepCopyArray = function(array) {
   var copiedArray = [];
   array.forEach(function(el) {
      copiedArray.push(el);
   })
   return copiedArray;
}

// random swap of two points
var randomSwapTwo = function(points, iterations) {
   var i = 0;
   // points is array, and since we don't want to overwrite this, wee need to deep-copy it
   var pointsCopy = deepCopyArray(points);

   while(i < iterations) {
      // pick the two elements to swap
      var first = Math.floor(Math.random() * pointsCopy.length);
      var second = first;
      while(second === first) {
         // console.log("calculating second", first, second);
         second = Math.floor(Math.random() * pointsCopy.length);
      }

      var store = pointsCopy[first];
      pointsCopy[first] = pointsCopy[second];
      pointsCopy[second] = store;

      i++;
   }
   return pointsCopy;
}


var createPoints = function(amount, maxCoordinates, minDistance) {
   var amount = amount || 30;
   var maxCoordinates = maxCoordinates || [500, 500];
   var minDistance = minDistance || 10;
   var points = [];

   console.log(amount, maxCoordinates, minDistance);

   while(amount) {
      console.log("creating a point");

      // create point
      var point = [
         Math.floor(Math.random() * maxCoordinates[0]),
         Math.floor(Math.random() * maxCoordinates[1]),
      ];

      var minDistanceKept = points.every(function(el) {
         if(parseInt(computeDistance(el, point)) < minDistance) {
            return false;
         }
         return true;
      });

      // check that point is not below minimum distance to existing points
      if(minDistanceKept) {
         // if point is OK decrement counter
         points.push(point);
         amount--;
      }

   }

   return points;

}
