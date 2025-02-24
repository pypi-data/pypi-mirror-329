import unittest
from spsscamera.camera import Camera

class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera()

    def test_initialize_camera(self):
        self.camera.initialize_camera()
        # Add assertions if needed

    def test_capture_frame(self):
        frame = self.camera.capture_frame()
        self.assertIn("frame", frame)

    def test_optimize_low_light(self):
        frame = {"frame": "captured_image_data"}
        optimized_frame = self.camera.optimize_low_light(frame)
        self.assertIn("optimized_frame", optimized_frame)

    def test_preprocess_image(self):
        frame = {"frame": "captured_image_data"}
        preprocessed_frame = self.camera.preprocess_image(frame)
        self.assertIn("preprocessed_frame", preprocessed_frame)

    def test_provide_feedback(self):
        frame = {"frame": "captured_image_data"}
        feedback_frame = self.camera.provide_feedback(frame)
        self.assertIn("feedback_frame", feedback_frame)

if __name__ == "__main__":
    unittest.main()