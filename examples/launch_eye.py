import subprocess

# Define the path to the Tobii Pro Eye Tracker Manager executable
# Adjust the path according to your installation location and OS
TETM_PATH = "C:/Users/Nelson Breguel/AppData/Local/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe"

# Define the serial number of your eye tracker
SERIAL_NUMBER = "TPNA1-030108540815"

# Command to launch the calibration
command = [
    TETM_PATH,
    f"--device-sn={SERIAL_NUMBER}",
    "--mode=usercalibration"
]

# Run the command
result = subprocess.run(command, capture_output=True, text=True)
print(result)

# Check the result
if result.returncode == 0:
    print("Calibration completed successfully.")
else:
    print(f"Calibration failed with exit code {result.returncode}")
