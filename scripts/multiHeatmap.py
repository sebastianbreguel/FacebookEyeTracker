import pandas as pd
import json
from datetime import datetime, timedelta
import os
import argparse

def load_gaze_data(file_path):
    df = pd.read_csv(file_path)
    df["current_time"] = pd.to_datetime(df["current_time"], format="%Y-%m-%dT%H:%M:%S.%fZ")
    return df

def load_json_data(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)
    return json_data

def process_gaze_data(df, json_data):
    #Step 1: initial date and first time
    initial_date = datetime.strptime(json_data[0]["initialDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    last_time_seconds = df[df["current_time"] - initial_date < timedelta(seconds=0)]["time_seconds"].iloc[-1]

    # Step 2: Remove all rows where `time_seconds` is less than 0
    df["time_seconds"] = df["time_seconds"] - last_time_seconds
    df = df[df["time_seconds"] >= 0].reset_index(drop=True)
    df["postID"] = None

    #Step 3: Assign postID based on PostStartTime and PostEndTime
    for obj in json_data:
        post_start_time = obj["PostStartTime"]
        post_end_time = obj["PostEndTime"]
        post_id = obj["postID"]

        df.loc[
            (df["time_seconds"] >= post_start_time) & (df["time_seconds"] <= post_end_time),
            "postID",
        ] = post_id

    #Step 4: Remove all rows where `postID` is None
    df = df[df["postID"].notna()].reset_index(drop=True)
    return df

def process_screenshots(screenshots_folder, json_data):

    #Step 1: Get the list of screenshot files
    screenshot_files = os.listdir(screenshots_folder)
    screenshot_files = [file for file in screenshot_files if file.endswith('.png')]
    screenshot_assignments = []

    #Step 2: Assign postID based on screenshot timestamp
    for file in screenshot_files:
        timestamp_str = file.replace('screenshot_', '').replace('.png', '').replace('_', ':')
        screenshot_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        assigned_post_id = None
        for obj in json_data:
            initial_date = datetime.strptime(obj["initialDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            post_start_time = initial_date + timedelta(seconds=obj["PostStartTime"])
            post_end_time = initial_date + timedelta(seconds=obj["PostEndTime"])

            if post_start_time <= screenshot_time <= post_end_time:
                assigned_post_id = obj["postID"]
                break

        screenshot_assignments.append({
            "filename": file,
            "screenshot_time": screenshot_time,
            "postID": assigned_post_id
        })
    
    #Step 3: Create a DataFrame with the assignments
    screenshot_df = pd.DataFrame(screenshot_assignments)
    screenshot_df = screenshot_df[screenshot_df["postID"].notna()].reset_index(drop=True)
    screenshot_df = screenshot_df.drop_duplicates(subset='postID', keep='first')
    screenshot_df.sort_values(by="screenshot_time", inplace=True)
    return screenshot_df

def assign_screenshot_filenames(df, screenshot_df):
    screenshot_df['postID'] = screenshot_df['postID'].astype(int)
    postID_to_filename = screenshot_df.set_index('postID')['filename'].to_dict()
    df['screenshot_filename'] = df['postID'].map(postID_to_filename)
    return df

def save_split_files(df, output_folder, name):
    os.makedirs(output_folder, exist_ok=True)
    unique_post_ids = df['postID'].unique()

    for post_id in unique_post_ids:
        df_filtered = df[df['postID'] == post_id]
        filename = f'{name}_gaze_{post_id}.csv'
        df_filtered.to_csv(os.path.join(output_folder, filename), index=False)
    
    print(f'Archivos CSV creados en la carpeta {output_folder}')

def create_heatmaps(unique_post_ids, width, height, name, root):

    for post_id in unique_post_ids:
        df_file = pd.read_csv(f"gaze_posts/{name}_gaze_{post_id}.csv")
        input_csv = root + f"gaze_posts/{name}_gaze_{post_id}.csv"
        image_screenshot = root + f"screenshots/{df_file['screenshot_filename'].iloc[0]}"
        heatmap_file = root + f"heatmaps/{name}_heatmap_{post_id}.png"

        os.system(
            f"python scripts/gazeheatplot.py {input_csv} {width} {height} -b {image_screenshot} -o {heatmap_file}")
        

def main():
    argpase = argparse.ArgumentParser()

    argpase.add_argument("name", type=str, help="total seconds to collect data")
    args = vars(argpase.parse_args())
    name = args["name"]

    root = f"data/{name}/"
    input_file = root + 'gaze_clean.csv'
    json_file  = root + f'times/{name}_posts_times.json'
    screenshot_folder = root + 'screenshots/'

    df = load_gaze_data(input_file)
    json_data = load_json_data(json_file)
    df = process_gaze_data(df, json_data)
    screenshot_df = process_screenshots(screenshot_folder, json_data)
    df = assign_screenshot_filenames(df, screenshot_df)
    save_split_files(df, 'gaze_posts/', name)
    unique_post_ids = df['postID'].unique()

    create_heatmaps(unique_post_ids, width=1920, height=1080, name=name, root=root)

if __name__ == "__main__":
    main()
