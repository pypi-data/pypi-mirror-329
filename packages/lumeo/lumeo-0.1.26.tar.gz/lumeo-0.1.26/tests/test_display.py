import unittest
import numpy as np
import cv2
from lumeo.pipeline.display import write_label_on_frame

class TestDisplay(unittest.TestCase):
    def test_write_label_on_frame(self):
        # Create a black image
        mat = np.zeros((500, 500, 3), dtype=np.uint8)

        # Define label and position
        xidx, yidx = 50, 50
        label = "This is a test label. It should wrap correctly."

        # Call the method
        label_width, total_label_height = write_label_on_frame(mat, xidx, yidx, label)

        # Check that label is written on the frame by verifying pixel values
        self.assertNotEqual(np.sum(mat), 0, "The label was not written on the frame.")

        # Optionally, you can check specific pixels to verify that the label is correctly placed
        self.assertTrue(np.any(mat[50:50+total_label_height, 50:50+label_width] != 0), "Label not correctly written.")

if __name__ == '__main__':
    unittest.main()
