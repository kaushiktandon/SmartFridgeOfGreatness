#include <iostream>
#include "firebase/app.h"

using namespace std;

app = App::Create(AppOptions(), jni_env, activity);

Storage* storage = Storage::GetInstance(app);

// Get a reference to the storage service, using the default Firebase App
Storage* storage = Storage::GetInstance(app);

// Create a storage reference from our storage service
StorageReference storage_ref = storage->GetReferenceFromUrl("gs://demotesterito.appspot.com/");

StorageReference images_ref = storage_ref.Child("Photos");

// Create a reference to the file you want to download
StorageReference islandRef = storage_ref.Child("Photos/19894.jpg"];

// Create local filesystem URL
const char* local_url = "testFridge.jpg";

// Download to the local filesystem
Future future = islandRef.GetFile(local_url);

// Wait for Future to complete...

if (future.Error() != firebase::storage::kErrorNone) {
  // Uh-oh, an error occurred!
} else {
  // The file has been downloaded to local file URL "images/island.jpg"
}