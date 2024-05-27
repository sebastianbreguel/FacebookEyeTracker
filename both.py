import time
import tobii_research as tr
import cv2
import numpy as np

# Initialize the eye tracker (assuming you have a connected eye tracker)
eyetrackers = tr.find_all_eyetrackers()
if len(eyetrackers) == 0:
    print("No eye trackers found.")
    exit()
eyetracker = eyetrackers[0]

# Calibration function
def calibrate_eye_tracker(eyetracker):
    calibration = tr.ScreenBasedCalibration(eyetracker)

    # Enter calibration mode.
    calibration.enter_calibration_mode()
    print("Entered calibration mode for eye tracker with serial number {}.".format(eyetracker.serial_number))

    # Define the points on screen we should calibrate at.
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

    # The calibration is done. Leave calibration mode.
    calibration.leave_calibration_mode()
    print("Left calibration mode.")

    return calibration_result

# Perform calibration
calibration_result = calibrate_eye_tracker(eyetracker)

if calibration_result.status != tr.CALIBRATION_STATUS_SUCCESS:
    print("Calibration was not successful.")
    exit()

# Callback function to handle gaze data
def gaze_data_callback(gaze_data):
    print("Gaze data: {}".format(gaze_data))

# Create a black image for gaze data collection
screen_width = 800
screen_height = 600
image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Subscribe to gaze data
eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

# Display the image during data collection
cv2.imshow('Data Collection', image)

# Collect data for a specific duration
collection_duration = 10  # seconds
print("Collecting gaze data for {} seconds...".format(collection_duration))
start_time = time.time()

while time.time() - start_time < collection_duration:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Unsubscribe from gaze data
eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

print("Gaze data collection completed.")

# Close the OpenCV window
cv2.destroyAllWindows()
