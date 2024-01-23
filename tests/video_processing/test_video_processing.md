# Test for video processing
This file describes the manual test for uploading videos to the app.
## Pre-requisites
Run the app using manual provided in README.md file in root directory.
## Testing video processing
To perform this test, upload the video from `tests/video_processing/test_videos/valid_videos/valid_video.mp4` 
directory to the app using `Upload Video` button. The result should be a video file `processed_video.mp4`.
### Test scenario
    - Given: The app is running
    - When: The user uploads the video with valid file extension `valid_video.mp4`
    - Then: The app should stop showing camera feed and show waiting screen until the video is processed. 
            After processing is finished, the app should download the processed video and return to the camera feed.
            For given video, the time of processing should take about 30 seconds.
