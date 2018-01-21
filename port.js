// Points to the root reference
var storageRef = firebase.storage().ref();

// Points to 'images'
var imagesRef = storageRef.child('Photos/').child(getLastPathSegment());

// File path is 'images/space.jpg'
var path = imagesRef.fullPath

// Get the download URL
imagesRef.getDownloadURL().then(function(url) {
  // Insert url into an <img> tag to "download"
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
