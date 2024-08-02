
Key Insight - Keystroke Tracker
===============================

Description
-----------
Key Insight is a keystroke tracking tool developed in Python. It captures every keystroke, calculates typing speeds, 
and periodically saves this data as both images and JSON files. This tool can be utilized to analyze typing patterns for 
productivity assessments or simply for personal monitoring.

Features
--------
- Real-time keystroke recording.
- Calculates typing speed in words per minute.
- Saves data in two formats:
  1. PNG images showing keystrokes and typing speed.
  2. JSON files with detailed records of keystrokes and average typing speeds.

Requirements
------------
- Python 3.6 or higher
- pynput
- PIL (Pillow)
- Any additional libraries required by the project can be installed via the requirements.txt file that accompanies this project.

Installation
------------
1. Ensure Python 3.6+ is installed on your system.
2. Clone the repository or download the source code:
   [Insert your repository link or download link here]
3. Navigate to the project directory and install required Python packages:
   ```
   pip install -r requirements.txt
   ```

Usage
-----
To run the Keystroke Tracker:
1. Navigate to the project directory in your terminal.
2. Run the script using Python:
   ```
   python keystroke_tracker.py
   ```
3. The tracker will start immediately. Data is saved automatically at intervals specified in the script.

Configuration
-------------
- `save_interval`: Adjust the time interval (in seconds) between data recordings in the `keystroke_tracker.py` script.
- Data is saved in the directory specified by `keystroke_track_dir` within the script. Modify as necessary.

Output
------
- The program generates and saves data in the `app/tests/keystroke-tracking` directory by default.
- Outputs include:
  - `keystroke_track_{timestamp}.png`: Image file with visual data.
  - `keystroke_track_{timestamp}.json`: JSON file with detailed keystroke data.

Stopping the Tracker
--------------------
To stop the tracker, use `Ctrl+C` in your terminal. Ensure to stop gracefully to avoid any data loss.

Contributing
------------
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. If you find bugs or 
have suggestions, please open an issue in the repository.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.
