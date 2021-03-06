  // Set the configuration for your app
  // TODO: Replace with your project's config object
  var config = {
    apiKey: 'AIzaSyA1dwI3Xq8S0SeMKbyNgTh-537ba3rqhMg ',
    authDomain: 'demotesterito.firebaseapp.com',
    databaseURL: 'https://demotesterito.firebaseio.com',
    storageBucket: 'gs://demotesterito.appspot.com/'
  };
  firebase.initializeApp(config);

  // Get a reference to the storage service, which is used to create references in your storage bucket
  //var storage = firebase.storage();

// Points to the root reference
var storageRef = firebase.storage().ref();

// Points to 'images'
var imagesRef = storageRef.child('Photos/').child('19894');

// File path is 'images/space.jpg'
var path = imagesRef.fullPath

// Get the download URL
imagesRef.getDownloadURL().then(function(url) {
  // `url` is the download URL for 'images/stars.jpg'

  // This can be downloaded directly:
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'blob';
  xhr.onload = function(event) {
    var blob = xhr.response;
  };
  xhr.open('GET', url);
  xhr.send();

  // Or inserted into an <img> element:
  var img = document.getElementById('myimg');
  img.src = url;

}).catch(function(error) {

  // A full list of error codes is available at
  // https://firebase.google.com/docs/storage/web/handle-errors
  switch (error.code) {
    case 'storage/object_not_found':
      // File doesn't exist
      break;

    case 'storage/unauthorized':
      // User doesn't have permission to access the object
      break;

    case 'storage/canceled':
      // User canceled the upload
      break;
      
    case 'storage/unknown':
      // Unknown error occurred, inspect the server response
      break;
  }
});