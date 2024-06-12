import argparse
import os
import winsound
# run generate.py


argpase = argparse.ArgumentParser()
## args: duration, name, width, height, input_file, output_file
argpase.add_argument("duration", type=int, help="total seconds to collect data")
argpase.add_argument("name", type=str, help="name of the output file")
argpase.add_argument("width", type=int, help="Screen width", default=1920)
argpase.add_argument("height", type=int, help="Screen height", default=1080)

args = vars(argpase.parse_args())
duration = args['duration']
name = args["name"]
width = args["width"]
height = args["height"]
base = "images/image.png"

# input for the processing
input_file = f"my_gaze_data_{name}"

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)
print("Runnign eye tracker")
print("asdasd")
# os.system(f'python generate.py {duration} {name}')

print("asdasd")
# print("Processing gaze data")
os.system(
   f"python gazeProcess.py {input_file}.csv {input_file}_clean.csv {width} {height}"
)

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

# print("Generating heatmap")
#os.system(
#    f"python gazeheatplot.py {input_file}_clean.csv {width} {height} -b {base} -o images/heatmap_{name}.png"
#)
