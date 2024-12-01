import argparse
import csv
import subprocess
import sys

import tobii_research as tr
from utils import get_current_time_iso8601, make_beep

"""
Parameters of your own EYE TRACKER
"""
user = "Nelson Breguel"
TETM_PATH = f"C:/Users/{user}/AppData/Local/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe"
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
        sys.exit("No connected eye trackers found. Please check the connection " "and/or install any missing drivers with Tobii Pro Eye Tracker Manager.")
    return all_eyetrackers[0]


def calibrate():
    command = [
        TETM_PATH,
        f"--device-sn={SERIAL_NUMBER}",
        "--mode=usercalibration",
        "--screen=1",
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Calibration completed successfully.")
        make_beep()
        return True
    else:
        print(f"Calibration failed with exit code {result.returncode}")
        return False


def gaze_data_callback(gaze_data):
    global gaze_data_samples
    gaze_data["current_time"] = get_current_time_iso8601()
    gaze_data_samples.append(gaze_data)


def save_gaze_data(gaze_samples_list, name):
    if not gaze_samples_list:
        print("No gaze samples were collected. Skipping saving")
        return

    # print("Sample dictionary keys:", gaze_samples_list[0].keys())

    file_handle = open(f"data/{name}/gaze.csv", "w")
    gaze_writer = csv.writer(file_handle)
    gaze_writer.writerow(["time_seconds", "current_time", "left_x", "left_y", "right_x", "right_y"])
    start_time = gaze_samples_list[0]["system_time_stamp"]
    for recording_dict in gaze_samples_list:
        sample_time_from_start = recording_dict["system_time_stamp"] - start_time

        sample_time_from_start = sample_time_from_start / (10 ** (6))  # convert from microseconds to seconds

        current_time = recording_dict["current_time"]

        left_x, left_y = recording_dict["left_gaze_point_on_display_area"]
        right_x, right_y = recording_dict["right_gaze_point_on_display_area"]
        gaze_writer.writerow([sample_time_from_start, current_time, left_x, left_y, right_x, right_y])
    file_handle.close()

    make_beep()


def main():
    parser = argparse.ArgumentParser(description="Parameters required for processing.")
    parser.add_argument("duration", type=int, help="total seconds to collect data")
    parser.add_argument("name", type=str, help="name of the output file")

    args = vars(parser.parse_args())
    collection_duration = args["duration"]
    name = args["name"]

    if not calibrate():
        return

    eyetracker = get_eyetracker()
    print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))

    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

    print("Collecting gaze data for {} seconds...".format(collection_duration))

    subprocess.run(["python", "scripts/screenshot.py", name, str(collection_duration)])

    # time.sleep(collection_duration)
    print("Unsubscribing from gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))

    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    save_gaze_data(gaze_data_samples, name)


if __name__ == "__main__":
    main()
