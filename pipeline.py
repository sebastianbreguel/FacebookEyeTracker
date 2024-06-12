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
input_file = f"data/{name}/gaze"


# make folder for the gaze of the user, screenshots and heatmap
os.makedirs(f"data/{name}/gaze_post", exist_ok=True)
os.makedirs(f"data/{name}/screenshots", exist_ok=True)
os.makedirs(f"data/{name}/heatmaps", exist_ok=True)
print(f"Directories for {name} created successfully.")


print("Running eye tracker")
os.system(f"python scripts/generate.py {duration} {name}")


print("Processing gaze data")
os.system(
    f"python scripts/gazeProcess.py {input_file}.csv {input_file}_clean.csv {width} {height}"
)


# print("Generating heatmap")
# os.system(
#    f"python gazeheatplot.py {input_file}_clean.csv {width} {height} -b {base} -o images/heatmap_{name}.png"
# )
