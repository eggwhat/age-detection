# Test scenarios for image directory
This file describes the manual test scenarios for uploading images from a directory to the app.
## Pre-requisites
Run the app using manual provided in README.md file in root directory.
## Test scenarios
To perform tests 1-4, upload the directory `tests/image_processing/test_images/manual_test` to the app using
`Upload Image Directory` button.
The result should be a zip file `images.zip` containing processed images from given directory. These
images should be in the directory with the same name as the original directory. 
### Test scenario 1
    - Given: The app is running
    - When: The user uploads the directory with valid image `valid.jpg`
    - Then: The app should return a zip file with processed image `valid_image.jpg` 
             with bounding box and age label ...
### Test scenario 2
    - Given: The app is running
    - When: The user uploads the directory with invalid image `no_faces.jpg` 
            that does not contain any faces
    - Then: The app should return a zip file with processed image `no_faces.jpg` 
            without bounding box and age label ...
### Test scenario 3
    - Given: The app is running
    - When: The user uploads the directory with image `many_faces.jpg` that 
            contains more than one face
    - Then: The app should return a zip file with processed image `many_faces.jpg` 
            with bounding box for each face and with following age labels: `age_1`, `age_2`, `age_3`
### Test scenario 4
    - Given: The app is running
    - When: The user uploads the directory with upside down image `upside_down.jpg`
    - Then: The app should return a zip file with processed image `upside_down.jpg` 
            with bounding box and age label ...
### Test scenario 5
    - Given: The app is running
    - When: The user uploads the directory `tests/image_processing/test_images/manual_test_huge_image/` 
            with image `huge_image.jpg`
    - Then: The app should take some time to process the image and show a message that upload failed.