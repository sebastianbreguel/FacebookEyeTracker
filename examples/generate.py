import subprocess
import csv
import sys
import time
import tobii_research as tr

# Define the path to the Tobii Pro Eye Tracker Manager executable
# Adjust the path according to your installation location and OS
TETM_PATH = "C:/Users/Nelson Breguel/AppData/Local/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe"

# Define the serial number of your eye tracker
SERIAL_NUMBER = "TPNA1-030108540815"
EYETRACKER_ADDRESS = "tobii-prp://TPNA1-030108540815"

# This list will be filled with dictionaries, with one dictionary per recording sample.
gaze_data_samples = []

def get_eyetracker():
    # Check if a specific eye tracker address has been provided, and if so, try to locate it and return the corresponding eye tracker object.
    if SERIAL_NUMBER:
        eyetracker = tr.EyeTracker(EYETRACKER_ADDRESS)
        if not eyetracker:
            sys.exit("Specified eye tracker not found, please check the address.")
        return eyetracker
    # If we reach this point, no specific address was provided, so return the first found eye tracker.
    all_eyetrackers = tr.find_all_eyetrackers()
    if not all_eyetrackers:
        sys.exit(
            "No connected eye trackers found. Please check the connection "
            "and/or install any missing drivers with Tobii Pro Eye Tracker Manager."
        )
    return all_eyetrackers[0]

def gaze_data_callback(gaze_data):
    global gaze_data_samples 
    gaze_data_samples.append(gaze_data)

def calibrate():
    # Command to launch the calxibration
    command = [
        TETM_PATH,
        f"--device-sn={SERIAL_NUMBER}",
        "--mode=usercalibration",
        "--screen=2"
    ]

    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result
    if result.returncode == 0:
        print("Calibration completed successfully.")
        return True
    else:
        print(f"Calibration failed with exit code {result.returncode}")
        return False

def save_gaze_data(gaze_samples_list):
    if not gaze_samples_list:
        print("No gaze samples were collected. Skipping saving")
        return
    print("Sample dictionary keys:", gaze_samples_list[0].keys())
    file_handle = open("my_gaze_data3.csv", "w")
    gaze_writer = csv.writer(file_handle)
    gaze_writer.writerow(["time_seconds", "left_x", "left_y", "right_x", "right_y"])
    start_time = gaze_samples_list[0]["system_time_stamp"]
    for recording_dict in gaze_samples_list:
        sample_time_from_start = recording_dict["system_time_stamp"] - start_time
        sample_time_from_start = sample_time_from_start / (10**(6))  # convert from microseconds to seconds
        left_x, left_y  = recording_dict["left_gaze_point_on_display_area"]
        right_x, right_y = recording_dict["right_gaze_point_on_display_area"]
        gaze_writer.writerow(
            [sample_time_from_start, left_x, left_y, right_x, right_y]
        )
    file_handle.close()

def main():
    if not calibrate():
        print("Calibration failed. Exiting.")
        return

    eyetracker = get_eyetracker()
    print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    collection_duration = 20  # seconds
    print("Collecting gaze data for {} seconds...".format(collection_duration))
    time.sleep(collection_duration)
    print("Unsubscribing from gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    save_gaze_data(gaze_data_samples)

if __name__ == "__main__":
    main()
