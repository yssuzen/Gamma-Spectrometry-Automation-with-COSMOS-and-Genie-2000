# Gamma Spectrometry Automation Program
This project automates the measurement process of a gamma spectrometer by integrating Velmex COSMOS software (for source positioning) and Genie 2000 (for data acquisition). It provides a graphical interface for users to define measurement parameters, execute a sequence of acquisitions, and save results automatically. The program supports flexible configuration, including uncertainty-based or time-based acquisition, and includes logging for both systems.


## Features

- User-friendly GUI built with Tkinter
- Automated movement control via Velmex COSMOS using the `serial` library
- Automated GUI interactions with Genie 2000 using `PyAutoGUI`
- Multi-threaded architecture to keep the interface responsive
- Screenshot logging at each stage for traceability
- Intelligent file naming to prevent overwriting
- Support for both time-based and uncertainty-based acquisitions
- Abort and skip handling with intermediate data saving

## File Structure

- `gui.py`: Contains the main application interface and automation sequence logic
- `cosmos.py`: Handles serial communication with the Velmex COSMOS system
- `icon.ico`: Custom icon for the GUI application

## Installation

1. Make sure you have Python 3 installed
2. Install required libraries:

```bash
pip install pyserial pyautogui
