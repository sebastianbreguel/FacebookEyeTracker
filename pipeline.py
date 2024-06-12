import argparse
import os

argpase = argparse.ArgumentParser()

## args: duration, name, width, height, input_file, output_file
argpase.add_argument("duration", type=int, help="total seconds to collect data")
argpase.add_argument("name", type=str, help="name of the output file")
argpase.add_argument("width", type=int, help="Screen width", default=1920)
argpase.add_argument("height", type=int, help="Screen height", default=1080)

args = vars(argpase.parse_args())
duration = args["duration"]
name = args["name"]
width = args["width"]
height = args["height"]
base = "images/image.png"

# input for the processing
input_file = f"../data/{name}/gaze/{name}"


# creating folder for this user
os.system(f"mkdir ../data/{name}")
# make ra_gaze folder for that person, screenshots, heatmaps and gaze_cleanded
os.system(f"mkdir ../data/{name}/gaze")
os.system(f"mkdir ../data/{name}/screenshots")
os.system(f"mkdir ../data/{name}/heatmaps")


# print("Running eye tracker")
# os.system(f"python generate.py {duration} {name}")


# print("Processing gaze data")
# os.system(
#     f"python gazeProcess.py {input_file}.csv {input_file}_clean.csv {width} {height}"
# )


# print("Generating heatmap")
# os.system(
#    f"python gazeheatplot.py {input_file}_clean.csv {width} {height} -b {base} -o images/heatmap_{name}.png"
# )
