import time
import tobii_research as tr
import cv2
import numpy as np

# Assuming `eyetracker` is already defined and connected
calibration = tr.ScreenBasedCalibration(eyetracker)

# Enter calibration mode.
calibration.enter_calibration_mode()
print("Entered calibration mode for eye tracker with serial number {}.".format(eyetracker.serial_number))

# Define the points on screen we should calibrate at.
# The coordinates are normalized, i.e. (0.0, 0.0) is the upper left corner and (1.0, 1.0) is the lower right corner.
points_to_calibrate = [(0.5, 0.5), (0.1, 0.1), (0.1, 0.9), (0.9, 0.1), (0.9, 0.9)]

# Create a black image
screen_width = 800
screen_height = 600
image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Function to draw a point on the screen
def draw_point(x, y):
    img = image.copy()
    cv2.circle(img, (x, y), 10, (0, 0, 255), -1)  # Draw a red circle
    cv2.imshow('Calibration', img)
    cv2.waitKey(1)  # Display the image for a brief moment

for point in points_to_calibrate:
    screen_x = int(point[0] * screen_width)
    screen_y = int(point[1] * screen_height)
    
    print("Show a point on screen at {}.".format(point))
    draw_point(screen_x, screen_y)

    # Wait a little for user to focus.
    time.sleep(0.7)

    print("Collecting data at {}.".format(point))
    if calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
        # Try again if it didn't go well the first time.
        calibration.collect_data(point[0], point[1])

print("Computing and applying calibration.")
calibration_result = calibration.compute_and_apply()
print("Compute and apply returned {} and collected at {} points.".format(calibration_result.status, len(calibration_result.calibration_points)))

# Analyze the data and maybe remove points that weren't good.
recalibrate_point = (0.1, 0.1)
print("Removing calibration point at {}.".format(recalibrate_point))
calibration.discard_data(recalibrate_point[0], recalibrate_point[1])

# Redo collection at the discarded point
print("Show a point on screen at {}.".format(recalibrate_point))
screen_x = int(recalibrate_point[0] * screen_width)
screen_y = int(recalibrate_point[1] * screen_height)
draw_point(screen_x, screen_y)
calibration.collect_data(recalibrate_point[0], recalibrate_point[1])

# Compute and apply again.
print("Computing and applying calibration.")
calibration_result = calibration.compute_and_apply()
print("Compute and apply returned {} and collected at {} points.".format(calibration_result.status, len(calibration_result.calibration_points)))

# The calibration is done. Leave calibration mode.
calibration.leave_calibration_mode()

print("Left calibration mode.")

# Close the OpenCV window
cv2.destroyAllWindows()
