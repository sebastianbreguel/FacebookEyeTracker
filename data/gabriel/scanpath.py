import matplotlib.pyplot as plt
import pandas as pd
import math
import argparse
import os

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main(args):
    # Load data
    data = pd.read_csv(args.gaze_csv)
    image = plt.imread(args.image_path)

    x = data['x']
    y = data['y']

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(image)
    # Initialize plot
    ax.set_xlim([0, 1920])
    ax.set_ylim([1080, 0])


    # Setup variables for plotting
    radius = 450
    last_x = data['x'].iloc[0]
    last_y = data['y'].iloc[0]
    accumulated_time = 0
    start_time = data['time_seconds'].iloc[0]
    plot_x = []
    plot_y = []
    times = []
    last_time = max(data['time_seconds'])

    # Loop through data
    last_take = False
    for i in range(1, len(data)):
        if 0 < data['x'].iloc[i] < 1920 and 0 < data['y'].iloc[i] <  1020:
            pass
        else:
            continue
        dist = euclidean_distance(last_x, last_y, data['x'].iloc[i], data['y'].iloc[i])
        if last_time - data['time_seconds'].iloc[i] < 0.5 and not last_take:
            plot_x.append(last_x)
            plot_y.append(last_y)
            times.append(accumulated_time if accumulated_time > 0 else 1)
            last_x = data['x'].iloc[i]
            last_y = data['y'].iloc[i]
            start_time = data['time_seconds'].iloc[i]
            accumulated_time = 0
            last_take = True
            continue

        if dist <= radius:
            accumulated_time += (data['time_seconds'].iloc[i] - start_time)
        else:
            plot_x.append(last_x)
            plot_y.append(last_y)
            times.append(accumulated_time if accumulated_time > 0 else 1)
            last_x = data['x'].iloc[i]
            last_y = data['y'].iloc[i]
            start_time = data['time_seconds'].iloc[i]
            accumulated_time = 0

    plot_x.append(last_x)
    plot_y.append(last_y)
    times.append(accumulated_time if accumulated_time > 0 else 1)

    # Normalize times for circle sizes
    max_time = max(times) if max(times) > 0 else 1
    sizes = [math.log(time) / math.log(max_time) * 500 for time in times]

    # Plot points and lines
    ax.plot(plot_x, plot_y, marker='', linestyle='-', color='red')
    scatter = ax.scatter(plot_x, plot_y, s=sizes, c='red', alpha=0.5, edgecolors='black')

    # Annotate points
    for i, (px, py, time) in enumerate(zip(plot_x, plot_y, times)):
        ax.annotate(i, (px, py), textcoords="offset points", xytext=(0,0), ha='center', va='center', color='black')

    ax.set_title('Gaze Duration and Path Visualization')

    # Remove numbers (tick labels) from the axes
    ax.set_xticks([])
    ax.set_yticks([])
    output_dir = "scanpath"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(args.output_scanpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate gaze duration and path visualization.")
    parser.add_argument("-i", "--image_path", type=str, required=True, help="Path to the background image.")
    parser.add_argument("-g", "--gaze_csv", type=str, required=True, help="Path to the gaze data CSV file.")
    parser.add_argument("-o", "--output_scanpath", type=str, required=True, help="Output path for the generated scanpath image.")

    args = parser.parse_args()
    main(args)
