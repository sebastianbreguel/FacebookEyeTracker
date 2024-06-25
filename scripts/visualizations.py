import argparse
import json
import os
from datetime import datetime, timedelta

import pandas as pd


def load_gaze_data(file_path):
    df = pd.read_csv(file_path)
    df["current_time"] = pd.to_datetime(
        df["current_time"], format="%Y-%m-%dT%H:%M:%S.%fZ"
    )
    return df


def load_json_data(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
    return json_data


def extract_number_simple(filename):
    # Split by underscore and take the second last element (index -2)
    parts = filename.split("_")
    # Remove the '.csv' and convert to integer
    number = int(parts[-1].replace(".csv", ""))
    return number


def create_visualizations(unique_post_ids, name, root, width=1920, height=1080):
    for post_id in unique_post_ids:
        input_csv = root + f"gaze_posts/{name}_gaze_{post_id}.csv"
        screenshot_path = root + f"screenshots/{name}_screenshot_{post_id}.png"

        heatmap_file = root + f"heatmaps/{name}_heatmap_{post_id}.png"
        scanpath_file = root + f"scanpath/{name}_scanpath_{post_id}.png"

        os.system(
            f"python scripts/visualizations/gazeHeatplot.py {input_csv} {width} {height} -b {screenshot_path} -o {heatmap_file}"
        )

        os.system(
            f"python scripts/visualizations/scanpathPlot.py -g {input_csv} -i {screenshot_path} -o {scanpath_file}"
        )


def main():
    argpase = argparse.ArgumentParser()

    argpase.add_argument("name", type=str, help="total seconds to collect data")
    args = vars(argpase.parse_args())
    name = args["name"]

    root = f"data/{name}/"

    post_files = os.listdir(root + f"gaze_posts")
    unique_post_ids = []
    for post_file in post_files:
        number = extract_number_simple(post_file)
        unique_post_ids.append(number)

    create_visualizations(unique_post_ids, name, root)


if __name__ == "__main__":
    main()
