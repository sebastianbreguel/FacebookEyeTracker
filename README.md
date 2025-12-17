# FacebookEyeTracker

A Python-based research tool for collecting, processing, and visualizing eye-tracking data while users view Facebook-like social media content. This tool captures gaze patterns using Tobii Pro Eye Trackers and generates heatmaps and scanpath visualizations to analyze user attention and engagement.

### Visualization Results

The pipeline generates two types of visualizations for each post:

<table>
<tr>
<td align="center" width="50%">

**Heatmap Visualization - gaze intensity**

![Heatmap Example](https://github.com/sebastianbreguel/FacebookEyeTracker/blob/main/data_example/nn/heatmaps/nn_heatmap_0.png)

</td>
<td align="center" width="50%">

**Scanpath Visualization - eye movement trajectory**

![Scanpath Example](https://github.com/sebastianbreguel/FacebookEyeTracker/blob/main/data_example/nn/scanpath/nn_scanpath_0.png)

</td>
</tr>
</table>

## Features

- **Eye-tracking data collection** using Tobii Pro Eye Tracker hardware
- **Automatic eye tracker calibration** via Tobii Pro Eye Tracker Manager
- **Screenshot capture** during experimental sessions
- **Gaze data processing** with automatic cleaning and interpolation
- **Post-level data matching** correlating gaze data with specific content
- **Heatmap generation** showing gaze intensity overlaid on content
- **Scanpath visualization** displaying eye movement trajectories
- **Batch processing** support for multiple participants

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Flow](#data-flow)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Known Issues](#known-issues)

## Requirements

### Hardware

- **Tobii Pro Eye Tracker** (tested with model TPNA1-030108540815)
- **Windows PC** (required for Tobii Pro Eye Tracker Manager)
- Monitor with standard resolution (default: 1920x1080)

### Software

- **Python 3.7+**
- **Tobii Pro Eye Tracker Manager** (Windows application)
- **Backend server** running on `localhost:3001` (for post metadata)

### Python Dependencies

```
matplotlib==3.7.1
numpy==1.24.3
pandas>=1.5.0
pyautogui==0.9.54
requests>=2.28.0
tobii_research==1.11.0
```

**Note**: The `requirements.txt` file is currently incomplete. You must manually install pandas and requests:

```bash
pip install pandas requests
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sebastianbreguel/FacebookEyeTracker.git
cd FacebookEyeTracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux (Note: This project requires Windows for eye tracker support)
source venv/bin/activate
```

### 3. Install dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# IMPORTANT: Manually install missing dependencies
pip install pandas requests
```

### 4. Install Tobii Pro Eye Tracker Manager

Download and install from [Tobii Pro](https://www.tobii.com/products/software/behavior-research-software/tobii-pro-eye-tracker-manager)

## Hardware Setup

1. **Connect the Tobii Pro Eye Tracker** to your computer via USB
2. **Launch Tobii Pro Eye Tracker Manager** to verify the device is detected
3. **Position the eye tracker** below your monitor at the recommended distance (typically 50-65 cm from user)
4. **Ensure proper lighting** - avoid direct sunlight or strong backlighting

## Usage

### Quick Start: Full Pipeline

Run the complete data collection and visualization pipeline:

```bash
python pipeline.py --duration 60 --name participant_01 --width 1920 --height 1080
```

**Parameters:**

- `--duration`: Recording duration in seconds (e.g., 60)
- `--name`: Participant identifier (e.g., "participant_01")
- `--width`: Screen width in pixels (default: 1920)
- `--height`: Screen height in pixels (default: 1080)

**Note**: The main pipeline code in `pipeline.py` is currently commented out. Uncomment lines 33-40 to enable full functionality.

### Step-by-Step: Individual Scripts

#### 1. Collect Eye-Tracking Data

```bash
python scripts/generate.py <duration_seconds> <participant_name>
```

Example:

```bash
python scripts/generate.py 60 participant_01
```

**Output**: `data/participant_01/gaze.csv`

**Important**: You must update `generate.py` line 12 to match your Windows username before running:

```python
user = "YourWindowsUsername"  # Change from "Nelson Breguel"
```

#### 2. Process Gaze Data

```bash
python scripts/gazeProcess.py <input_csv> <output_csv> <screen_width> <screen_height>
```

Example:

```bash
python scripts/gazeProcess.py data/participant_01/gaze.csv data/participant_01/gaze_clean.csv 1920 1080
```

**Output**: `data/participant_01/gaze_clean.csv`

#### 3. Match Gaze Data with Posts

Ensure your backend server is running on `localhost:3001`, then:

```bash
python scripts/match.py <participant_name>
```

Example:

```bash
python scripts/match.py participant_01
```

**Output**:

- `data/participant_01/times/participant_01_posts_times.json`
- `data/participant_01/gaze_posts/participant_01_gaze_<post_id>.csv` (per post)

#### 4. Generate Visualizations

```bash
python scripts/visualizations.py <participant_name>
```

Example:

```bash
python scripts/visualizations.py participant_01
```

**Output**:

- `data/participant_01/heatmaps/participant_01_heatmap_<post_id>.png`
- `data/participant_01/scanpath/participant_01_scanpath_<post_id>.png`

#### 5. Capture Screenshots (Run During Experiment)

```bash
python scripts/screenshot.py <participant_name> <duration_seconds>
```

Example:

```bash
python scripts/screenshot.py participant_01 60
```

**Output**: Screenshots saved to `data/participant_01/screenshots/`

### Batch Processing

To process multiple participants:

```bash
python tools/batch_process.py --participants participant_01 participant_02 --steps process match visualize
```

For more options, see `python tools/batch_process.py --help`.

## Project Structure

```
FacebookEyeTracker/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Project configuration & linting rules
├── .pre-commit-config.yaml            # Pre-commit hooks configuration
├── pipeline.py                        # Main pipeline orchestrator
│
├── scripts/                           # Core processing scripts
│   ├── generate.py                    # Eye tracker calibration & data collection
│   ├── gazeProcess.py                 # Clean and process raw gaze data
│   ├── match.py                       # Match gaze data with posts
│   ├── screenshot.py                  # Capture screenshots during session
│   ├── visualizations.py              # Orchestrate visualization generation
│   ├── utils.py                       # Utility functions (timestamps, interpolation)
│   ├── readme.md                      # Scripts documentation
│   └── visualizations/                # Visualization modules
│       ├── gazeHeatplot.py            # Generate heatmap visualizations
│       └── scanpathPlot.py            # Generate scanpath visualizations
│
├── tools/                             # Utility tools
│   ├── batch_process.py               # Batch processing for multiple participants
│   └── cleanup.py                     # Data cleanup utility
│
├── single_post_test/                  # Single image testing module
│   ├── generate.py                    # Simplified generation for testing
│   ├── gazeProcess.py                 # Test data processing
│   ├── gazeheatplot.py                # Test heatmap generation
│   ├── pipeline.py                    # Test pipeline
│   ├── screenshot.py                  # Test screenshot capture
│   ├── utils.py                       # Test utilities
│   └── readme.md                      # Test module documentation
│
└── data/                              # Experimental data (created at runtime)
    └── <participant_name>/
        ├── gaze.csv                   # Raw eye-tracking data
        ├── gaze_clean.csv             # Processed gaze data
        ├── times/
        │   └── <name>_posts_times.json
        ├── screenshots/
        │   └── screenshot_*.png
        ├── gaze_posts/
        │   └── <name>_gaze_<post_id>.csv
        ├── heatmaps/
        │   └── <name>_heatmap_<post_id>.png
        └── scanpath/
            └── <name>_scanpath_<post_id>.png
```

## Data Flow

```
┌─────────────────────┐
│  Eye Tracker HW     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  generate.py        │ → data/<name>/gaze.csv
│  (Raw data)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  gazeProcess.py     │ → data/<name>/gaze_clean.csv
│  (Clean & process)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  screenshot.py      │ +   │  Backend Server  │
│  (Capture screen)   │     │  (Post metadata) │
└──────────┬──────────┘     └────────┬─────────┘
           │                         │
           └────────┬────────────────┘
                    ▼
           ┌─────────────────────┐
           │  match.py           │ → data/<name>/gaze_posts/
           │  (Match posts)      │   data/<name>/times/
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  visualizations.py  │ → data/<name>/heatmaps/
           │  (Generate visuals) │   data/<name>/scanpath/
           └─────────────────────┘
```

## Configuration

### Screen Resolution

Default resolution is 1920x1080. To use a different resolution:

1. **Pass as command-line arguments**:

   ```bash
   python pipeline.py --duration 60 --name test --width 2560 --height 1440
   ```

2. **Or edit** `scripts/scanpathPlot.py` lines 26-27:
   ```python
   ax.set_xlim([0, 2560])  # Your screen width
   ax.set_ylim([1440, 0])   # Your screen height
   ```

### Eye Tracker Settings

Edit `scripts/generate.py` lines 12-15:

```python
user = "YourWindowsUsername"  # REQUIRED: Change this
TETM_PATH = f"C:/Users/{user}/AppData/Local/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe"
SERIAL_NUMBER = "TPNA1-030108540815"  # Your device serial number
EYETRACKER_ADDRESS = "tobii-prp://TPNA1-030108540815"  # Your device address
```

### Backend Server URL

Edit `scripts/match.py` line 12:

```python
url = "http://localhost:3001/download/answersPostsAndSurvey"
```

### Example Data Structure

After running the full pipeline for participant "alice", your data directory will look like:

```
data/alice/
├── gaze.csv                           # Raw eye-tracking data (x, y coordinates + timestamps)
├── gaze_clean.csv                     # Processed data (cleaned, interpolated, averaged)
├── times/
│   └── alice_posts_times.json         # Post timing metadata from backend
├── screenshots/
│   ├── screenshot_2024-06-23T21_44_00.png
│   ├── screenshot_2024-06-23T21_44_05.png
│   └── ...                            # One screenshot every ~5 seconds
├── gaze_posts/
│   ├── alice_gaze_20.csv              # Gaze data for post ID 20
│   ├── alice_gaze_21.csv              # Gaze data for post ID 21
│   └── ...                            # One CSV per post viewed
├── heatmaps/
│   ├── alice_heatmap_20.png           # Heatmap for post ID 20
│   ├── alice_heatmap_21.png
│   └── ...
└── scanpath/
    ├── alice_scanpath_20.png          # Scanpath for post ID 20
    ├── alice_scanpath_21.png
    └── ...
```

### Sample CSV Data

**Raw Gaze Data** (`gaze.csv`):

```csv
time_seconds,current_time,left_x,left_y,right_x,right_y
0.000,2024-06-23T21:44:46.395Z,0.512,0.487,0.515,0.489
0.033,2024-06-23T21:44:46.428Z,0.518,0.492,0.520,0.494
0.067,2024-06-23T21:44:46.462Z,0.525,0.498,0.527,0.500
```

**Processed Gaze Data** (`gaze_clean.csv`):

```csv
time_seconds,current_time,x,y
0.000,2024-06-23T21:44:46.395Z,985,487
0.033,2024-06-23T21:44:46.428Z,1001,492
0.067,2024-06-23T21:44:46.462Z,1010,498
```

**Post Timing Data** (`times/alice_posts_times.json`):

```json
[
  {
    "userName": "alice",
    "postID": 20,
    "truth": -2,
    "confidence": 1,
    "initialDate": "2024-06-23T21:44:46.395Z",
    "PostStartTime": 0.061,
    "PostEndTime": 26.511,
    "PostTimeSpent": 26.45,
    "SurveyStartTime": 26.519,
    "SurveyEndTime": 45.908,
    "SurveyTimeSpent": 19.389
  }
]
```

### Batch Processing Output Example

Running the batch processing tool:

```bash
$ python tools/batch_process.py --participants alice bob charlie --steps visualize

============================================================
BATCH PROCESSING
============================================================
Participants: alice, bob, charlie
Steps: visualize
Resolution: 1920x1080
============================================================

============================================================
Processing participant: alice
Steps: visualize
============================================================

--- Step: visualize ---
Generating heatmaps and scanpaths...
Created: data/alice/heatmaps/alice_heatmap_20.png
Created: data/alice/scanpath/alice_scanpath_20.png
Created: data/alice/heatmaps/alice_heatmap_21.png
Created: data/alice/scanpath/alice_scanpath_21.png
✅ Step 'visualize' completed successfully

============================================================
Processing participant: bob
Steps: visualize
============================================================

--- Step: visualize ---
✅ Step 'visualize' completed successfully

============================================================
Processing participant: charlie
Steps: visualize
============================================================

--- Step: visualize ---
✅ Step 'visualize' completed successfully

============================================================
BATCH PROCESSING COMPLETE
============================================================
✅ alice: 1/1 steps succeeded
✅ bob: 1/1 steps succeeded
✅ charlie: 1/1 steps succeeded

------------------------------------------------------------
Total steps succeeded: 3
Total steps failed: 0
============================================================
```

### Cleanup Utility Output Example

Running the cleanup tool:

```bash
$ python tools/cleanup.py --participants alice --visualizations

============================================================
Processing participant: alice
============================================================
Deleted: data/alice/heatmaps/alice_heatmap_20.png
Deleted: data/alice/heatmaps/alice_heatmap_21.png
Deleted: data/alice/heatmaps/alice_heatmap_22.png
Deleted: data/alice/scanpath/alice_scanpath_20.png
Deleted: data/alice/scanpath/alice_scanpath_21.png
Deleted: data/alice/scanpath/alice_scanpath_22.png

Deleted 6 file(s) for alice

============================================================
CLEANUP COMPLETE - Total files deleted: 6
============================================================
```

## Troubleshooting

### "Module not found" errors

**Problem**: `ModuleNotFoundError: No module named 'pandas'` or `'requests'`

**Solution**:

```bash
pip install pandas requests
```

The `requirements.txt` is incomplete. These packages must be installed manually.

### "Eye tracker not found"

**Problem**: `Could not find Tobii eye tracker`

**Solutions**:

1. Ensure the eye tracker is connected via USB
2. Open Tobii Pro Eye Tracker Manager to verify device detection
3. Check that the serial number in `generate.py` matches your device
4. Try unplugging and reconnecting the device

### "FileNotFoundError" when running pipeline

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/...'`

**Solution**: The pipeline creates directories automatically, but ensure you have write permissions in the project directory.

### Heatmaps appear blank or incorrect

**Problem**: Heatmaps show no data or incorrect positions

**Possible causes**:

1. **Screen resolution mismatch**: Verify width/height parameters match your display
2. **Calibration issue**: Recalibrate the eye tracker using Tobii Pro Eye Tracker Manager
3. **Processing bug**: There's a known bug in `gazeProcess.py` line 37-38 (see Known Issues)

### Backend connection fails

**Problem**: `Error during request: Connection refused`

**Solution**: Ensure the backend server is running on `localhost:3001` before running `match.py`

### Windows-specific errors on macOS/Linux

**Problem**: `ModuleNotFoundError: No module named 'winsound'`

**Solution**: This project requires Windows due to Tobii hardware dependencies. The code is not currently cross-platform compatible.

## Known Issues

### Critical Bugs

1. **Coordinate averaging bug** (`scripts/gazeProcess.py:37-38`)

   - When left eye data is NaN, assigns `right_y` to `avg_x` (should be `right_x`)
   - **Impact**: Corrupts gaze coordinates
   - **Fix needed**: Change `right_y` to `right_x` on line 37

2. **Scanpath images not saved** (`scripts/scanpathPlot.py:109`)

   - `plt.savefig()` is commented out
   - **Impact**: Scanpath visualizations aren't actually saved
   - **Fix needed**: Uncomment the line

3. **Pipeline code disabled** (`pipeline.py:33-40`)
   - Core data collection steps are commented out
   - **Impact**: Pipeline doesn't run generate.py or gazeProcess.py
   - **Fix needed**: Uncomment lines 33-40

### Platform Limitations

- **Windows-only**: Requires Windows for Tobii SDK and `winsound` module
- **Hardcoded paths**: User-specific paths need manual configuration
- **No cross-platform support**: Cannot run on macOS or Linux

### Documentation Issues

- Incomplete `requirements.txt` (missing pandas, requests)
- Inconsistent typo "argpase" instead of "argparse" in multiple files
- No type hints or comprehensive docstrings

## Contributing

This is a research project developed for XR course studies. For questions or contributions, please contact the project maintainer.

### Development Setup

1. Fix critical bugs before making changes
2. Add tests for any new functionality
3. Follow PEP 8 style guidelines
4. Update documentation for new features

## License

[Add license information]

## Citation

If you use this tool in your research, please cite:

```
[Add citation information]
```

## Contact

[Add contact information]

## Acknowledgments

- Tobii Pro for eye-tracking hardware and SDK
- [Add other acknowledgments]
