# Tests for real time processing
This file describes the manual tests for real time processing.
## Pre-requisites
Run the app using manual provided in README.md file in root directory.
## Test scenarios
### Test scenario 1
    - Given: The app is running and camera is connected
    - When: There is a face in front of the camera
    - Then: The app should show one camera feed from original stream and one from processed stream containing 
            bounding box and age label. The delay between original and processed stream should not be noticeable.
### Test scenario 2
    - Given: The app is running and camera is connected
    - When: There are many faces in front of the camera
    - Then: The app should show one camera feed from original stream and one from processed stream with
            bounding box and age label for each face. Additionally, processed stream might show slight delay because
            of processing time.
### Test scenario 3
    - Given: The app is running and camera is connected
    - When: There is a face in front of the camera with head tilted to the side by more than 45 degrees
    - Then: The app should show one camera feed from original stream and one from processed stream without
            bounding box and age label. 