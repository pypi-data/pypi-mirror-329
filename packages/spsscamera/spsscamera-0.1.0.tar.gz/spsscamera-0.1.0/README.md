# spsscamera

The `spsscamera` library accesses the device’s camera, captures high-quality frames, and preprocesses them for efficient decoding by `spssdecode`. It supports cross-platform compatibility for web, iOS, and Android.

## Installation

```bash
pip install -r requirements.txt
```

USAGE:
from spsscamera.camera import Camera

# Initialize the Camera

camera = Camera()

# Capture a frame

frame = camera.capture_frame()

# Optimize for low-light conditions

optimized_frame = camera.optimize_low_light(frame)

# Preprocess the image

preprocessed_frame = camera.preprocess_image(optimized_frame)

print(preprocessed_frame)
