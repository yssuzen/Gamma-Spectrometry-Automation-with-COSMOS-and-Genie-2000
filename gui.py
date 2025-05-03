# This file is part of the Gamma Spectrometry Automation Program project.
#
# Copyright (C) 2025 Yavuz Selim Suzen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import time
import json
import os
import subprocess  
import pyautogui
from datetime import datetime
import shutil
import pywinauto
import traceback
import win32gui
import re
from pywinauto import Application
from pywinauto import Desktop
from pathlib import Path

from cosmos import move_to_position, kill_motion, return_to_reference, get_position, setReference

Screenshot_base_folder = r"/put/your/own/path/here"
Destination_base_folder= r"put/your/own/path/here"
A_folder= os.path.join('put/your/folder/directory/like/A:\\', 'GENIE2K')
G2K_base_folder= os.path.join(A_folder, 'CAMFILES')
EXPECTED_ERROR = "Error: 278e2a. File is open and not sharable."

def open_datasource():
    pyautogui.hotkey('ctrl', 'o')   #Open Datasource - postion (x,y) on genie
    time.sleep(1)
    pyautogui.click(1146,729)   #Clicks 'Detector' - postion (x,y) on genie
    time.sleep(1)
    pyautogui.click(1111,640)   #Clicks 'Detector' - postion (x,y) on genie
    time.sleep(1)
    pyautogui.click(1461,699)   #Clicks 'Open' after clicking 'Detector' - position (x,y) on genie

def click_ok_on_warning():
    time.sleep(1)               #waits 1 secs because there will be alert on the screen
    pyautogui.click(1330,747)   #Clicks 'Ok' to open the Detector
    time.sleep(2) 
    pyautogui.click(41,314)   #Clicks 'Next' to see Marker Info
    time.sleep(0.5)
    pyautogui.click(41,314)   #Clicks 'Next' to see Livetime and Dead time

def warning_datasource():
    pyautogui.click(1380, 747) #clicks ok on datasource warning

def gui_hover_open():
    time.sleep(1)
    pyautogui.hotkey('win', '9')
    pyautogui.press('enter')

def acquisition_setup_time(minutes):
    time.sleep(1) 
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(2) 
    pyautogui.click(1039,600)   #Clicks 'Acquisition'
    time.sleep(1) 
    pyautogui.click(1264,616)   #Clicks 'Insert'
    time.sleep(1) 
    pyautogui.click(1052,743)   #Clicks 'Save Datasource'
    time.sleep(1) 
    pyautogui.click(1264,616)   #Clicks 'Insert'
    time.sleep(1)
    pyautogui.doubleClick(1412,623) #Double Click on Acquisition to setup
    time.sleep(1)
    pyautogui.click(1048,675)  #Real Time Preset
    time.sleep(1)
    pyautogui.click(1154,697)   #Clicks 'Min' - Acquisition Setup
    time.sleep(1)
    pyautogui.doubleClick(1217,653)   #Clicks Text Area for Time - Acquisition Setup
    time.sleep(1)
    pyautogui.typewrite(str(float(minutes)))
    time.sleep(1)
    pyautogui.click(1267,645)  #Click None for Computational Preset - Acquisition Setup
    time.sleep(1)
    pyautogui.click(1260,781)   #Clicks 'Clear Data/Time at Start of Acquisition' - Acquisition Setup
    time.sleep(1)
    pyautogui.click(1056,810)   #Clicks 'Ok' - Acquisition Setup

def acquisition_setup_area(value, start_ch, stop_ch):
    time.sleep(1) 
    pyautogui.hotkey('ctrl', 'e')
    time.sleep(2) 
    pyautogui.click(1039,600)   #Clicks 'Acquisition'
    time.sleep(1) 
    pyautogui.click(1264,616)   #Clicks 'Insert'
    time.sleep(1) 
    pyautogui.click(1052,743)   #Clicks 'Save Datasource'
    time.sleep(1) 
    pyautogui.click(1264,616)   #Clicks 'Insert'
    time.sleep(1)
    pyautogui.doubleClick(1412,623) #Double Click on Acquisition to setup
    time.sleep(1)
    pyautogui.doubleClick(1217,653)   #Clicks Text Area for Time - Acquisition Setup
    time.sleep(1)
    pyautogui.typewrite('0')
    time.sleep(1)
    pyautogui.click(1267,678) # Clicks 'Area' on computational preset - Acquisition Setup
    time.sleep(1)
    pyautogui.doubleClick(1483,649)   #Clicks Text Area for Area - Acquisition Setup
    time.sleep(1)
    pyautogui.typewrite(str(int(value)))
    time.sleep(1)
    pyautogui.doubleClick(1483,672)   #Clicks Text Area for Start Channel - Acquisition Setup
    time.sleep(1)
    pyautogui.typewrite(str(int(start_ch)))
    time.sleep(1)
    pyautogui.doubleClick(1483,697)   #Clicks Text Area for Stop Channel - Acquisition Setup
    time.sleep(1)
    pyautogui.typewrite(str(int(stop_ch)))
    time.sleep(1)
    pyautogui.click(1260,781)   #Clicks 'Clear Data/Time at Start of Acquisition' - Acquisition Setup
    time.sleep(1)
    pyautogui.click(1056,810)   #Clicks 'Ok' - Acquisition Setup

def start_genie_measurement():
    time.sleep(1)
    pyautogui.click(1480,860)   #Clicks 'Execute' - Analysis Sequence

# works only when 'Next Position' is pressed on gui. Stops measurement and saves the file
def stop_genie_measurement():
    time.sleep(1)
    pyautogui.click(112,128)   #Clicks 'Stop'

def close_datasource():
    pyautogui.hotkey('ctrl', 'alt', 'c')    #closes datasource
    pyautogui.click(1341, 750)  #clicks 'no' on alert to close the cnf file

def close():
    time.sleep(0.75)
    pyautogui.hotkey('alt','space') #using for closing genie cnf file
    time.sleep(0.75)
    pyautogui.hotkey('alt', 'F4')   #closes genie cnf file
    time.sleep(1)
    pyautogui.click(1341, 750)  #clicks 'no' on alert to close the cnf file

def close_genie():
    time.sleep(0.5)
    close_datasource()
    time.sleep(0.5)
    close()

def count_number_of_files():
    camfiles_folder = r"put/your/own/path/here"
    return len([f for f in os.listdir(camfiles_folder) if f.lower()])

def save_genie_files(filename_base):
    time.sleep(2)
    pyautogui.hotkey('ctrl', 's')   #opens 'Save as' window on genie
    time.sleep(0.75)
    pyautogui.click(1292,844)    #clicks on filename area - just in case
    time.sleep(0.75)
    pyautogui.typewrite(str(filename_base)) 
    time.sleep(0.75)
    pyautogui.click(1169, 845)  #avoid dropdown on filename area
    time.sleep(0.75)
    pyautogui.click(1435, 858)  #save as type dropdown
    time.sleep(0.75)
    pyautogui.click(1304, 903)  #clicks on IEC format
    time.sleep(0.75)
    pyautogui.click(1515, 830)  #save button
    time.sleep(2)
    pyautogui.hotkey('ctrl', 's')   #opens 'Save as' window on genie
    time.sleep(0.75)
    pyautogui.click(1292,844)    #clicks on filename area - just in case
    time.sleep(0.75)
    pyautogui.typewrite(str(filename_base)) 
    time.sleep(0.75)
    pyautogui.click(1169, 845)  #avoid dropdown on filename area
    time.sleep(0.75)
    pyautogui.click(1435, 858)  #save as type dropdown
    time.sleep(0.75)
    pyautogui.click(1291, 879)  #clicks on CNF format
    time.sleep(0.75)
    pyautogui.click(1515, 830)  #save button

#Edits sample info
def edit_sample_info(iso, id, pos):
    description = f"Ottawa - Position{pos}"
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'alt', 'i')    #opens edit sample info
    time.sleep(1)
    pyautogui.doubleClick(1258, 597)     #Sample Title on Edit Sample Info
    pyautogui.typewrite(str(iso))
    time.sleep(1)
    pyautogui.doubleClick(1494, 593)     #Sample ID on Edit Sample Info
    pyautogui.typewrite(str(int(id)))
    time.sleep(1)
    pyautogui.click(1212, 648)     #Sample Description on Edit Sample Info
    pyautogui.rightClick(1212, 648)     #Sample Description on Edit Sample Info
    time.sleep(0.1)
    pyautogui.click(1300,780)   #clicks on 'Selects All'
    pyautogui.typewrite(str(description))
    time.sleep(1)
    pyautogui.click(1052, 830)     #OK button

ROUTINES_FILE = "routines.json"

#loading routine
def load_routines():
    if not os.path.exists(ROUTINES_FILE):
        return []

    with open(ROUTINES_FILE,"r") as f:
        data=json.load(f)
        return data.get("routines",[])

#Saving routine
def save_routines(rlist):
    data={"routines":rlist}

    with open(ROUTINES_FILE,"w") as f:
        json.dump(data,f,indent=2)
 
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("COSMOS & Genie 2000 Control Panel")
        self.geometry("1200x800")

        self.columnconfigure(0, weight=1) # Genie grid setup
        self.columnconfigure(1, weight=0) # Separator grid setup
        self.columnconfigure(2, weight=1) # COSMOS grid setup
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        #Frames
        self.genie_frame = ttk.Frame(self, padding=10)
        self.genie_frame.grid(row=0, column=0, sticky="nsew")

        self.separator = ttk.Separator(self, orient='vertical')
        self.separator.grid(row=0, column=1, sticky="ns")

        self.cosmos_frame = ttk.Frame(self, padding=10)
        self.cosmos_frame.grid(row=0, column=2, sticky="nsew")

        self.log_frame_genie = ScrolledText(self, wrap='word', height=10, state='disabled')
        self.log_frame_genie.grid(row=1, column = 0, sticky='nsew')

        self.separator_log = ttk.Separator(self, orient='vertical')
        self.separator_log.grid(row=1, column=1, sticky="ns")

        self.log_frame_cosmos = ScrolledText(self, wrap='word', height=10, state='disabled')
        self.log_frame_cosmos.grid(row=1, column = 2, sticky='nsew')

        self.routines_list = load_routines()
        self.create_menus()

        # A boolean to handle "skip" request
        self.skip_flag = False
        # A boolean to handle "abort" request
        self.movement_flag = False
        self.abort_flag = False

        #Building panels for Genie and COSMOS
        self.create_genie_frame()
        self.create_cosmos_frame()
        self.pos_folder_cache = {}
    
    def get_or_create_screenshot_folder(self, date_val, iso_val, pos_str):

        key = (date_val, iso_val, pos_str)
        if key in self.pos_folder_cache:
            return self.pos_folder_cache[key]

        iso_folder = os.path.join(Screenshot_base_folder, iso_val)
        if not os.path.exists(iso_folder):
            os.makedirs(iso_folder)

        date_folder = os.path.join(iso_folder, date_val)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)

        pos_base = os.path.join(date_folder, pos_str)
        if not os.path.exists(pos_base):
            os.makedirs(pos_base)
            final_folder = pos_base
        else:
            index = 1
            while True:
                ss = os.path.join(date_folder, f"{pos_str}_{index}")
                if not os.path.exists(ss):
                    os.makedirs(ss)
                    final_folder = ss
                    break
                index+=1
        self.pos_folder_cache[key] = final_folder
        return final_folder
    
    def take_screenshot(self, phase_name, date_val, iso_val, pos_str):
        pos_folder = self.get_or_create_screenshot_folder(date_val, iso_val, pos_str)
        filename = f"{phase_name}.png"
        fullpath = os.path.join(pos_folder, filename)
        image = pyautogui.screenshot()
        image.save(fullpath)
        
    #Menu on top bar
    def create_menus(self):
        menubar=tk.Menu(self)
        routine_menu=tk.Menu(menubar, tearoff=0)
        routine_menu.add_command(label="Save", command=self.on_new_routine) #For saving new routine
        routine_menu.add_command(label="Load", command=self.on_load_routine) #For loading from saved routines
        routine_menu.add_command(label="Rename", command=self.on_rename_routine) #For renaming routine
        routine_menu.add_command(label="Delete", command=self.on_delete_routine) #For deleting from saved routines

        menubar.add_cascade(label="Routine", menu=routine_menu)
        self.config(menu=menubar)
    
    def create_genie_frame(self):
        lbl_genie_title = ttk.Label(self.genie_frame, text="Genie 2000 Control", font=("Arial", 14, "bold"))
        lbl_genie_title.pack(anchor="center", pady=(0,10))

        self.lbl_genie_warning = tk.Label(self.genie_frame, 
                                          text="\n  MEASUREMENT IN PROGRESS \n", 
                                          font=("Arial", 15, "bold"), 
                                          fg='black', 
                                          bg='red')
        
        self._update_status_genie("No acquisition in progress")
        #self.lbl_genie_status.pack(anchor="center", pady=(10, 0))
    
    def measurement_warning_disappear(self):
        self.lbl_genie_warning.pack_forget()

    def create_cosmos_frame(self):
        lbl_cosmos_title = ttk.Label(self.cosmos_frame, text="COSMOS Control", font = ("Arial", 14, "bold"))
        lbl_cosmos_title.pack(anchor="center", pady=(0, 10))

        #row for id, date, target peak energy and isotope
        frm_idi = ttk.Frame(self.cosmos_frame)
        frm_idi.pack(anchor="center", pady=5)

        #Date input
        lbl_date = ttk.Label(frm_idi, text="Date", font=("Arial", 10, "bold"))
        lbl_date.grid(row=0, column=0, padx=5)
        self.entry_date = ttk.Entry(frm_idi, width=15)
        self.entry_date.grid(row=1, column=0, padx=5)

        #Isotope input
        lbl_iso = ttk.Label(frm_idi, text="Isotope", font=("Arial", 10, "bold"))
        lbl_iso.grid(row=0, column=2, padx=5)
        self.entry_iso = ttk.Entry(frm_idi, width=15)
        self.entry_iso.grid(row=1, column=2, padx=5)

        #ID input
        lbl_id = ttk.Label(frm_idi, text="ID", font=("Arial", 10, "bold"))
        lbl_id.grid(row=0, column=4, padx=5)
        self.entry_id = ttk.Entry(frm_idi, width=15)
        self.entry_id.grid(row=1, column=4, padx=5)

        #Target Peak Energy (keV) input
        lbl_id = ttk.Label(frm_idi, text="Target Peak Energy (keV)", font=("Arial", 10, "bold"))
        lbl_id.grid(row=0, column=6, padx=5)
        self.entry_target_peak = ttk.Entry(frm_idi, width=15)
        self.entry_target_peak.grid(row=1, column=6, padx=5)

        #10 boxes for waiting time and position
        frm_pw = ttk.Frame(self.cosmos_frame)
        frm_pw.pack(anchor="center", pady=10)

        #Position and Wait titles on the gui
        lbl_ph= ttk.Label(frm_pw, text="Position", font=("Arial", 10, "bold"))
        lbl_wh = ttk.Label(frm_pw, text="Wait (in minutes)", font=("Arial", 10, "bold"))
        lbl_tu = ttk.Label(frm_pw, text="Target Uncertaincy (%)", font=("Arial", 10, "bold"))
        lbl_ph.grid(row=0, column=0, padx=5)
        lbl_wh.grid(row=0, column=1, padx=5)
        lbl_tu.grid(row=0, column=2, padx=5)

        #Creating 10 boxes (input) for wait, position, uncertaincy
        self.pos_entries = []
        self.wait_entries = []
        self.uncertaincy_entries = []
        for i in range(10):
            epos = ttk.Entry(frm_pw, width=8)
            epos.grid(row=i+1, column=0, padx=5, pady=2)
            ewait = ttk.Entry(frm_pw, width=8)
            ewait.grid(row=i+1, column=1, padx=5, pady=2)
            euncert = ttk.Entry(frm_pw, width=8)
            euncert.grid(row=i+1, column=2, padx=5, pady=2)
            self.pos_entries.append(epos)
            self.wait_entries.append(ewait)
            self.uncertaincy_entries.append(euncert)

        #Frame for buttons
        frm_btn = ttk.Frame(self.cosmos_frame)
        frm_btn.pack(anchor="center", pady=5)

        #Clear button for clearing all sections
        self.btn_clear = ttk.Button(frm_btn, text="Clear", command=self.on_clear)
        self.btn_clear.grid(row=0, column=0, padx=5)

        #Button for run
        self.btn_run = ttk.Button(frm_btn, text="Run", command=self.on_run_sequence)
        self.btn_run.grid(row=0, column=1, padx=5)

        #Button for abort -> goes back to reference point
        self.btn_kill = ttk.Button(frm_btn, text="Abort", command=self.on_kill_motion)
        self.btn_kill.grid(row=0, column=2, padx=5)
        self.btn_kill.config(state="disabled")

        #Button for skip position -> skips current position and goes to next position
        self.btn_skip = ttk.Button(frm_btn, text="Next Position", command=self.on_skip_position)
        self.btn_skip.grid(row=0, column=3, padx=5)
        self.btn_skip.config(state="disabled")

        #Status for Cosmos
        self._update_status("Status: Ready")
    
    #Launches the application and returns its process ID.
    def launch_application(self):
        
        try:
            # Start the application using subprocess.Popen
            process = subprocess.Popen(r'')
            
            # Wait for the application to initialize
            time.sleep(1)  # Increased wait time to ensure the application is ready
            open_datasource()
            return process.pid
        except Exception as e:
            self._update_status_genie(f"Failed to launch application: {e}")
            self._update_status_genie(traceback.format_exc())
            return None

    def is_genie_maximized(self, process_id, window_title):
        try:
            app = Application().connect(process=process_id)
            window = app.window(title=window_title)
            return window.is_maximized()
        except Exception as e:
            self._update_status_genie(f"Failed to verify program is full screen mode: {e}")
            self._update_status_genie(traceback.format_exc())
            return False

    def is_genie_visible(self, process_id, window_title):
        try:
            app = Application().connect(process=process_id)
            window = app.window(title=window_title)
            hwnd = window.wrapper_object().handle  # Get window handle

            foreground_hwnd = win32gui.GetForegroundWindow()  # Get current active window handle

            if hwnd == foreground_hwnd:
                return True
            else:
                return False
        except Exception as e:
            self._update_status_genie(f"Failed to verify window visibility: {e}")
            return False

    def maximize_window(self, process_id, window_title):
        #Maximizes the window of an application given its process ID and window title.
        
        try:
            # Connect to the application with pywinauto
            app = Application().connect(process=process_id)
            
            # Access the main window using the exact title
            window = app.window(title=window_title)
            
            #time.sleep(10)  
            
            # Check if already maximized and visible
            if self.is_genie_maximized(process_id, window_title) and self.is_genie_visible(process_id, window_title):
                self._update_status_genie("✅ Window is already maximized and visible.")
                return

            self._update_status_genie("⚠️ Window is NOT maximized or NOT visible. Fixing now...")

            # Restore if hidden (ensures it's visible)
            if not self.is_genie_visible(process_id, window_title):
                self._update_status_genie("🔄 Window is not in foreground. Restoring it...")
                window.restore()
                time.sleep(1)

            # Ensure it's maximized
            if not self.is_genie_maximized(process_id, window_title):
                self._update_status_genie("🖥️ Window is NOT maximized. Maximizing now...")
                window.set_focus()
                window.maximize()
                time.sleep(1)

            # Final verification
            if self.is_genie_maximized(process_id, window_title) and self.is_genie_visible(process_id, window_title):
                self._update_status_genie("✅ Window is now maximized and visible.")
            else:
                self._update_status_genie("❌ Failed to ensure window is maximized and visible.")
        except Exception as e:
            self._update_status_genie(f"An error occurred: {e}")
            self._update_status_genie(traceback.format_exc())
        
    def datasource_checking(self, process_id, window_title, expected_error):
        try:
            app = Application().connect(process=process_id)
            window = app.window(title=window_title)
            
            #gets error message - Error: 278e2a. File is open and not sharable.
            error_text = window.child_window(title_re="Error:.*", class_name="Static").window_text()
            
            self._update_status_genie(f"Detected Error Message: {error_text}")
            
            if error_text.strip() == expected_error.strip():
                return True
            return False
        except Exception as e:
            self._update_status_genie(f"No error window detected: {e}")
            return False
    
    #Checks if the 'Start' button is grey (disabled).    
    def is_start_button_black(self, process_id, window_title="put/your/window/title/here"):  

        try:
            # Connect to the application window
            app = Application().connect(process=process_id)
            window = app.window(title=window_title)
            
            # Find the Start button
            start_button = window.child_window(title="Start", class_name="Button")

            # Check if the button is grey (disabled)
            return start_button.is_enabled()

        except Exception as e:
            self._update_status_genie(f"⚠️ Error checking Start button: {e}")
            return False  # Assume it's not grey if we can't detect it
    
    #Checks if the 'Stop' button is grey (disabled).    
    def is_stop_button_black(self, process_id, window_title="put/your/window/title/here"):
        try:
            # Connect to the application window
            app = Application().connect(process=process_id)
            window = app.window(title=window_title)
            
            # Find the Stop button
            stop_button = window.child_window(title="Stop", class_name="Button")

            # Check if the button is grey (disabled)
            return stop_button.is_enabled()

        except Exception as e:
            self._update_status_genie(f"⚠️ Error checking Start button: {e}")
            return False  # Assume it's not grey if we can't detect it

    def on_run_sequence(self):
        date_val = self.entry_date.get().strip()
        iso_val = self.entry_iso.get().strip()
        id_val = self.entry_id.get().strip()
        peak_val = self.entry_target_peak.get().strip()

        positions = []
        waits = []
        uncertaincy = []
        for i in range(10):
            ps=self.pos_entries[i].get().strip()
            ws=self.wait_entries[i].get().strip() 
            us = self.uncertaincy_entries[i].get().strip()

            # handling wait and position and uncertaincy boxes empty
            if not ps and not ws and not us:
                continue
            #one of the boxes filled but the other one not. Shows warning on the GUI
            if not ps:
                self._update_status(f"Row {i+1} partially filled. Must have position)")
                return
            
            #Checks whether the position is integer
            try:
                p_val = int(ps)
                if p_val< 10 or p_val> 70:
                    self._update_status("Position must be between 10 to 70") 
                    return
            except ValueError:
                self._update_status(f"Row {i+1}: invalid position '{ps}'")
                return
            
            #Checks whether the target peak energy is float and bigger than 0
            try:
                t_val = float(peak_val)
                if t_val < 0:
                    self._update_status("Target Energy must be bigger than 0")
                    return
            except ValueError:
                self._update_status(f"Invalid Target Peak Energy: {peak_val}")
                return
            
            has_wait = (ws != "")
            has_unc = (us != "")
            if has_wait and has_unc:
                self._update_status(f"Row {i+1}: Please fill only Wait Time or Uncertainty")
                return
            if not has_wait and not has_unc:
                self._update_status(f"Row {i+1}: Please fill either Wait Time or Uncertainty")
                return
            
            w_val = 0.0
            u_val = 0.0
            if has_wait:
                try:
                    w_val = float(ws)
                except ValueError:
                    self._update_status(f"Row {i+1}: invalid wait '{ws}'")
                    return
            else:
                try:
                    u_val = float(us)
                except ValueError:
                    self._update_status(f"Row {i+1}: invalid uncertainty '{us}'")
                    return
            
            positions.append(p_val)
            waits.append(w_val)
            uncertaincy.append(u_val)

        if not date_val or not iso_val or not id_val or not peak_val:
            self._update_status("Please enter date, isotope, id, and target peak")
            return
        
        if not positions:
            self._update_status("No valid rows entered")
            return
        
        #Disabling inputs, run button
        #Enabling abort button
        self.btn_run.config(state="disabled")
        self.entry_date.config(state="disabled")
        self.entry_id.config(state="disabled")
        self.entry_iso.config(state="disabled")
        self.entry_target_peak.config(state="disabled")
        #self.btn_kill.config(state="normal")
        self.btn_clear.config(state="disabled")
        self.skip_flag = False
        self.movement_flag = False
        self.abort_flag = False
        self.lbl_genie_warning.pack(pady=200)
        for i in range(10):
            self.pos_entries[i].config(state="disabled")
            self.wait_entries[i].config(state="disabled")
            self.uncertaincy_entries[i].config(state="disabled")

        #Starting a thread to run the entire sequence
        t = threading.Thread(target=self._automated_sequence_thread, args=(positions, waits, uncertaincy, date_val, iso_val, id_val, peak_val))
        t.start()

    def _automated_sequence_thread(self, positions, waits, uncertaincy, date_val, iso_val, id_val, peak_val):
        self._update_status(f"Resetting the reference position for Cosmos, please wait")
        setReference(port="put/your/port", baud=put/your/baudrate)
        try:
            pyautogui.FAILSAFE=False
            try:
                e_peak = float(peak_val)
            except ValueError:
                self._update_status_genie(f"Invalid target peak energy: {peak_val}")
                return

            ch_start = int((e_peak - 4 + 0.01919)/0.062539)
            ch_stop = int((e_peak + 4 + 0.01919)/0.062539)

            if ch_start<0:
                ch_start = 0
            self._update_status_genie(f"Target Peak {peak_val} keV => channels [{ch_start}, {ch_stop}]")

            for i in range(len(positions)):
                if self.abort_flag:
                    break

                pos = positions[i]
                w_min = waits[i]
                u_pct = uncertaincy[i]

                self.movement_flag = True
                self._update_status(f"Moving to {pos}")
                self.btn_kill.config(state="normal")
                move_to_position(pos, put/your/speed, put/your/port, put/your/baudrate)
                if self.abort_flag and self.movement_flag:
                    return_to_reference(speed=put/your/speed/here)
                if self.abort_flag:
                    break
                self.movement_flag = False
                self.btn_skip.config(state="normal")
                self.take_screenshot(f"after_move_pos{pos}", date_val, iso_val, str(pos))

                # Open Genie and start the measurement
                pid = self.launch_application()
                self.take_screenshot("launched_genie", date_val, iso_val, str(pos))
                click_ok_on_warning()
                self.take_screenshot("clicked_yes_on_warning_first_time", date_val, iso_val, str(pos))
                if pid:
                    # Use the correct window title
                    self.maximize_window(pid, 'put/your/window/title/here')
                    self.take_screenshot("max_genie_after_launching_it", date_val, iso_val, str(pos))
                    self._update_status_genie(f"Process ID: {pid}")

                else:
                    self._update_status_genie("Failed to retrieve a valid process ID.")
                    self.take_screenshot("not_valid_pid", date_val, iso_val, str(pos))
                    break
                
                if self.skip_flag:
                    self._update_status("Skipping current position")
                    self.skip_flag = False
                    continue

                if self.datasource_checking(pid, "Detector", EXPECTED_ERROR):
                    self.take_screenshot("after_check_datasource", date_val, iso_val, str(pos))
                    ok = messagebox.askokcancel("Detector in use", "Detector is in use. Please close it in Genie. Click OK to continue or Cancel to return reference position")
                    if not ok:
                        self._update_status("Returning back to reference position")
                        self.take_screenshot("clicked_cancel_return_reference", date_val, iso_val, str(pos))
                        break
                    else:
                        self.maximize_window(pid, 'put/your/window/title/here')
                        self.take_screenshot("max_genie_after_clicked_ok", date_val, iso_val, str(pos))
                        warning_datasource()
                        self.take_screenshot("clicked_datasource_warning", date_val, iso_val, str(pos))
                        open_datasource()
                        self.take_screenshot("connected_datasource", date_val, iso_val, str(pos))
                        click_ok_on_warning()
                        self.take_screenshot("clicked_yes_on_warning", date_val, iso_val, str(pos))
                        self._update_status_genie("User closed Detector and proceeding")
                
                if self.abort_flag:
                    break

                if w_min > 0:
                    self._update_status(f"Arrived at {pos} and will wait {w_min} minutes")
                    acquisition_setup_time(w_min)
                    self.take_screenshot("after_acquisition_time_setup", date_val, iso_val, str(pos))
                else:
                    total_counts = 0.0
                    if u_pct > 0:
                        total_counts = 6.13 * ((u_pct/100)**-1.76)
                    else:
                        self._update_status(f"Row {i+1}: invalid uncertainty {u_pct}")
                        break

                    self._update_status(f"Arrived at {pos} and will wait until total counts ({total_counts}) reach at target peak {peak_val}")
                    acquisition_setup_area(total_counts, ch_start, ch_stop)
                    self.take_screenshot("after_acquisition_area_setup", date_val, iso_val, str(pos))

                #self.maximize_window(pid, 'put/your/window/title/here')
                if self.is_start_button_black(pid):
                    self.take_screenshot("after_verify_start_button_black", date_val, iso_val, str(pos))
                    start_genie_measurement()
                    self.take_screenshot("after_started_acquisition", date_val, iso_val, str(pos))
                    self._update_status_genie("Acquisition started")
                else:
                    self._update_status_genie("Another acquisition is progress")
                    self.take_screenshot("start_button_not_black", date_val, iso_val, str(pos))
                
                edit_sample_info(iso_val, id_val, pos)    
                self.take_screenshot("edited_sample_info", date_val, iso_val, str(pos))            
                
                #Back to the GUI window, Genie is down
                gui_hover_open() #to be changed once we have an .exe
                self.take_screenshot("program_foreground", date_val, iso_val, str(pos)) 
                self._update_status(f"Position {pos}: Starting Acquisition")
                initial_count = count_number_of_files()
                while True:
                    if self.abort_flag:
                        self.maximize_window(pid, 'put/your/window/title/here')
                        stop_genie_measurement()
                        self.take_screenshot("stopped_genie_after_abort_button", date_val, iso_val, str(pos)) 
                        self._update_status_genie("Acquisition Stopped Forcibly")
                        self._update_status("Acquisition Stopped Manually")
                        self.measurement_warning_disappear()
                        gui_hover_open()
                        self.take_screenshot("after_gui_front", date_val, iso_val, str(pos))
                        self._update_status("Returning to reference position. Genie stopped already")
                        return_to_reference(speed=put/your/speed/here)
                        self.take_screenshot("return_reference_after_abort", date_val, iso_val, str(pos)) 
                        self._update_status("Arrived reference position")
                        break
                    time.sleep(5)
                    if self.skip_flag:
                        self._update_status_genie("Stopping Measurement and saving files")
                        self.maximize_window(pid, 'put/your/window/title/here')
                        self.take_screenshot("max_genie_after_skip_button", date_val, iso_val, str(pos)) 
                        if self.is_stop_button_black(pid):
                            self.take_screenshot("verify_stop_button_black", date_val, iso_val, str(pos)) 
                            stop_genie_measurement()
                            self.take_screenshot("stopped_genie_after_skip_button", date_val, iso_val, str(pos)) 
                            self._update_status_genie("Stop button is black. Acquisition was progress and forcibly stopped")
                        else:
                            self._update_status_genie("Acquisition has already been stopped")
                            self.take_screenshot("stop_button_grey", date_val, iso_val, str(pos)) 
                        self.measurement_warning_disappear()
                        self.take_screenshot("remove_measurement_warning_on_program", date_val, iso_val, str(pos)) 
                        self.skip_flag = False
                        break
                    current_count = count_number_of_files()
                    self.take_screenshot("got_current_count", date_val, iso_val, str(pos)) 
                    if current_count > initial_count:
                        self._update_status_genie("New cnf file has been created and that means acquisition stopped")
                        self.take_screenshot("new_cnf_found", date_val, iso_val, str(pos)) 
                        break               
                
                #measurement is done, so disable next position. Will enable after reach to the next position
                self.btn_skip.config(state="disabled")
                                
                # Now that we have a file Name, reopen Genie 2K to save the file
                # Save the file              
                filename = f"{date_val}_{iso_val}_{id_val}_pos{pos}"
                Final_filename = self.find_unique_name(date_val, iso_val, filename)
                self.take_screenshot("found_unique_filename", date_val, iso_val, str(pos)) 
                self._update_status_genie(f"Final name will be'{Final_filename}'")
                self.maximize_window(pid, 'put/your/window/title/here')
                self.take_screenshot("max_genie_for_saving_files", date_val, iso_val, str(pos)) 
                try:
                    save_genie_files(Final_filename)
                    self.take_screenshot("saved_files", date_val, iso_val, str(pos)) 
                except Exception as e:
                    self._update_status_genie(f"Could not save the file: {e}, proceeding")
                    self.take_screenshot("couldnt_save_files", date_val, iso_val, str(pos)) 

                # Determine is IEC file exist
                fileNameWithEXT = f"{Final_filename}.IEC"
                fullpath = os.path.join(G2K_base_folder, fileNameWithEXT)
                if not os.path.isfile(fullpath):
                    self._update_status_genie(f"The file '{fullpath}' was not found")                 
                    filename = f"{date_val}_{iso_val}_{id_val}_pos{pos}"
                    Final_filename = self.find_unique_name(date_val, iso_val, filename)
                    self.take_screenshot("found_unique_filename_after_didnt_find_IEC", date_val, iso_val, str(pos)) 
                    self._update_status_genie(f"Final name will be'{Final_filename}'")
                    self.maximize_window(pid, 'put/your/window/title/here')
                    self.take_screenshot("max_genie_to_save_files_with_final_filename", date_val, iso_val, str(pos)) 
                    try:
                        save_genie_files(Final_filename)
                        self.take_screenshot("saved_files_with_finalname", date_val, iso_val, str(pos)) 
                    except Exception as e:
                        self._update_status_genie(f"Could not save the file: {e}, proceeding")
                        self.take_screenshot("didnt_save_files_after_final_filename", date_val, iso_val, str(pos)) 

                if not os.path.isfile(fullpath):
                    self._update_status_genie(f"The file '{fullpath}' is still not created, this was our last")
                    self.take_screenshot("last_try_to_save_files", date_val, iso_val, str(pos)) 

                # If yes, Close Genie, Move files
                # Make sure G2K is up!
                self.maximize_window(pid, 'put/your/window/title/here')
                self.take_screenshot("max_genie_to_close", date_val, iso_val, str(pos)) 
                close_genie()
                self.take_screenshot("closed_genie", date_val, iso_val, str(pos)) 

                # ADD Verify if G2K is up and with Detector open
                self.moved_Files(date_val, iso_val, Final_filename)
                self.take_screenshot("moved_files", date_val, iso_val, str(pos)) 

                # Genie is now close and we are ready to proceed with the next position
            
            if self.abort_flag: 
                self._update_status("Process completed with abort")
            else:
                self.movement_flag = True
                self._update_status("Returning to reference position (76944)")
                return_to_reference(speed=put/your/speed/here)
                self.take_screenshot("return_reference_position_after_acquisition", date_val, iso_val, str(pos)) 
                #All positions done
                self.movement_flag = False
                self._update_status("All positions processed")
                self._update_status_genie("All measurements processed")
                
        except Exception as e:
            self._update_status(f"Error: {str(e)}")
            self.take_screenshot("couldnt_perform_movement", date_val, iso_val, str(pos)) 
        #re-enabling button and input
        self.after(0, self._enable_controls)
        self.take_screenshot("enable_buttons", date_val, iso_val, str(pos)) 

    def find_unique_name(self, date_val, iso_val, filename_base):
         # Extension
        extension=['IEC', 'CNF']
         # Folder
        Destination_base_folder_ISO=os.path.join(Destination_base_folder, iso_val)
        if not os.path.exists(Destination_base_folder_ISO):
            os.makedirs(Destination_base_folder_ISO)
            self._update_status_genie(f"Created new source folder as '{Destination_base_folder_ISO}'")
        else: 
            self._update_status_genie(f"Folder already exist: '{Destination_base_folder_ISO}'")

        Destination_base_folder_ISOdate=os.path.join(Destination_base_folder_ISO, date_val)
        if not os.path.exists(Destination_base_folder_ISOdate):
            os.makedirs(Destination_base_folder_ISOdate)
            self._update_status_genie(f"Created new source folder as '{Destination_base_folder_ISOdate}'")
        else: 
            self._update_status_genie(f"Folder already exist: '{Destination_base_folder_ISOdate}'")            

        folderName=[G2K_base_folder, Destination_base_folder_ISOdate]

        # Initialize a counter
        counter = 0

        # Check if the file exists             
        counter = 0
        unique_name_found = False
        while not unique_name_found:
            unique_name_found = True
            fileName = f"{filename_base}_{counter}" if counter > 0 else filename_base
            for ext in extension:
                for foldName in folderName:
                    # Construct the full file path
                    fileNameWithEXT = f"{fileName}.{ext}"
                    fullpath = os.path.join(foldName, fileNameWithEXT)
                    self._update_status_genie(f"Checking for this file: '{fullpath}'")

                    # Check if the file exists
                    if os.path.exists(fullpath):
                        self._update_status_genie(f"File already exists: '{fullpath}'")
                        unique_name_found = False
                        break  # No need to check other folders/extensions for this counter

                if not unique_name_found:
                    break

            if not unique_name_found:
                counter += 1  # Increment the counter only if the name was not unique

        # At this point, `fileName` is unique across all folders and extensions
        self._update_status_genie(f"Unique file name found: '{fileName}'")
        return fileName

    def moved_Files(self, date_val, iso_val, filename):
        # try to move files
        extension=['IEC', 'CNF']
        notfoldName = os.path.join(Destination_base_folder, iso_val)
        foldName = os.path.join(notfoldName, date_val)
        self._update_status_genie(f"This is the RadNuc folder Name'{foldName}'")
        for ext in extension:
            Final_filenameWithExt = f"{filename}.{ext}"
            CamFolder_File = os.path.join(G2K_base_folder, Final_filenameWithExt)
            RadNucFolder_File = os.path.join(foldName, Final_filenameWithExt)
            try:
                shutil.move(CamFolder_File, RadNucFolder_File)
            except Exception as e:
                self._update_status_genie(f"Was not able to move the file '{Final_filenameWithExt}'") 
                self._update_status_genie(e)      

    def on_kill_motion(self):
        self.abort_flag = True
        self._update_status("Process Aborted. Please wait...")
        if self.abort_flag and self.movement_flag:
            self._update_status("Motion aborted, after reaching to the position, slide will return to reference position")

        #disabling abort and skip button
        self.btn_kill.config(state="disabled")
        self.btn_skip.config(state="disabled")

    #clears all the fields -> date, isotope, id, position, wait
    def on_clear(self):
        self.entry_date.delete(0, tk.END)
        self.entry_iso.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)
        self.entry_target_peak.delete(0, tk.END)
        for i in range(10):
            self.pos_entries[i].delete(0, tk.END)
            self.wait_entries[i].delete(0, tk.END)
            self.uncertaincy_entries[i].delete(0, tk.END)
        self._update_status("All fields cleared")

    #skips current position and goes to next position
    def on_skip_position(self):
        self.skip_flag = True
        self._update_status("Skipping current position")

    #Updating status on cosmos
    def _update_status(self, text: str):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {text}\n"
        #enabling editing and put new 
        self.log_frame_cosmos.config(state='normal')
        self.log_frame_cosmos.insert(tk.END, line)
        self.log_frame_cosmos.see(tk.END)
        self.log_frame_cosmos.config(state='disabled')
    
    #Updating status on Genie
    def _update_status_genie(self, text: str):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        line = f"{timestamp} {text}\n"
        #enabling editing and put new 
        self.log_frame_genie.config(state='normal')
        self.log_frame_genie.insert(tk.END, line)
        self.log_frame_genie.see(tk.END)
        self.log_frame_genie.config(state='disabled')
    
    #Re-enabling controls
    def _enable_controls(self):
        self.btn_run.config(state="normal")
        self.entry_date.config(state="normal")
        self.entry_id.config(state="normal")
        self.entry_iso.config(state="normal")
        self.entry_target_peak.config(state="normal")
        self.btn_kill.config(state="disabled")
        self.btn_clear.config(state="normal")
        self.btn_skip.config(state="disabled")
        self.lbl_genie_warning.pack_forget()
        for i in range(10):
            self.pos_entries[i].config(state="normal")
            self.wait_entries[i].config(state="normal")
            self.uncertaincy_entries[i].config(state="normal")
    
    #New Routine
    def on_new_routine(self):
        p_strs = []
        w_strs = []
        u_strs = []
        for i in range(10):
            ps = self.pos_entries[i].get().strip()
            ws = self.wait_entries[i].get().strip()
            us = self.uncertaincy_entries[i].get().strip()
            if not ps and not ws and not us:
                continue
            if (not ps or not ws) and (not ps or not us):
                self._update_status(f"Row {i+1} partially filled, cannot create routine")
                return
            p_strs.append(ps)
            w_strs.append(ws)
            u_strs.append(us)
        iso_val = self.entry_iso.get().strip()
        id_val = self.entry_id.get().strip()
        peak_val = self.entry_target_peak.get().strip()

        #Gives error on the gui window
        if not iso_val or not id_val or not peak_val or  not p_strs or not w_strs or not u_strs:
            self._update_status("Cannot create new routine. Fill positions, waits, isotope, target peak, and id")
            return
        
        positions_str = ",".join(p_strs)
        waits_str = ",".join(w_strs)
        uncertainties_str = ','.join(u_strs)
        
        d = RoutineNameDialogue(self,"New Routine","Enter routine name:")
        self.wait_window(d)

        r_name = d.result_name

        if not r_name:
            self._update_status("New routine canceled.")
            return
        
        found_index = -1
        for i,r in enumerate(self.routines_list):
            if r["name"] == r_name:
                found_index = i
                break

        if found_index >=0:
            ans = messagebox.askyesno("Overwrite Routine?", f"Routine '{r_name}' already exists. \nDo you want to overwrite it?")
            if ans:
                self.routines_list[found_index]["positions"]= positions_str
                self.routines_list[found_index]["wait_times"]= waits_str
                self.routines_list[found_index]["uncertainty"]= uncertainties_str
                self.routines_list[found_index]["ID"]= id_val
                self.routines_list[found_index]["isotope"]= iso_val
                self.routines_list[found_index]["peak"]= peak_val
            else:
                self._update_status("Save Routine canceled")
                return
        else:
            newr = {
                "name":r_name,
                "positions":positions_str,
                "wait_times":waits_str,
                "uncertainty":uncertainties_str,
                "isotope":iso_val,
                "ID":id_val,
                "peak":peak_val
            }
            self.routines_list.append(newr)
        save_routines(self.routines_list)
        self._update_status(f"New routine '{r_name}' saved.")

    #Loading Routine
    def on_load_routine(self):
        if not self.routines_list:
            self._update_status("No routines to load.")
            return

        d = SelectRoutineDialogue(self, "Load Routine", "Select Routine to Load:",
                                [r["name"] for r in self.routines_list])
        
        self.wait_window(d)
        sel = d.result_name

        if not sel:
            self._update_status("Load canceled.")
            return
        
        routine_obj = None

        for r in self.routines_list:
            if r["name"] == sel:
                routine_obj = r
                break
        
        if not routine_obj:
            self._update_status("Routine not found")
            return
        
        #Parsing fields
        positions_str = routine_obj.get("positions", "")
        waits_str = routine_obj.get("wait_times", "")
        uncertainties_str = routine_obj.get("uncertainty", "")
        iso_val = routine_obj.get("isotope", "")
        id_val = routine_obj.get("ID", "")
        peak_val = routine_obj.get("peak", "")

        #Deleting isotope area and after inserting the value from saved routine
        self.entry_iso.delete(0, tk.END)
        self.entry_iso.insert(0, iso_val)

        #Deleting ID and after inserting the value from saved routine
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, id_val)

        #Deleting Target Peak and after inserting the value from saved routine
        self.entry_target_peak.delete(0, tk.END)
        self.entry_target_peak.insert(0, peak_val)

        #Clearing boxes
        for i in range(10):
            self.pos_entries[i].delete(0, tk.END)
            self.wait_entries[i].delete(0, tk.END)
            self.uncertaincy_entries[i].delete(0, tk.END)
        
        if positions_str:
            pos_list = positions_str.split(",")
        else:
            pos_list = []
        
        if waits_str:
            wait_list = waits_str.split(",")
        else:
            wait_list = []

        if uncertainties_str:
            uncertainty_list = uncertainties_str.split(",")
        else:
            uncertainty_list = []

        for i in range(min(len(pos_list), 10)):
            self.pos_entries[i].insert(0, pos_list[i])

        for i in range(min(len(wait_list), 10)):
            self.wait_entries[i].insert(0, wait_list[i])

        for i in range(min(len(uncertainty_list), 10)):
            self.uncertaincy_entries[i].insert(0, uncertainty_list[i])

        self._update_status(f"Routine '{sel}' loaded")

    #Renaming routine from saved routines
    def on_rename_routine(self):
        if not self.routines_list:
            self._update_status("No routines to rename")
            return
        
        d = SelectRoutineDialogue(self, "Rename Routine", "Select Routine to Rename:",
                                [r["name"] for r in self.routines_list])
        
        self.wait_window(d)
        old_name = d.result_name

        if not old_name:
            self._update_status("Rename canceled")
            return
        
        routine_obj = None
        for r in self.routines_list:
            if r["name"] == old_name:
                routine_obj =r
                break

        if not routine_obj:
            self._update_status("Routine not found.")
            return
        
        d2 = RoutineNameDialogue(self, "Rename Routine", f"New name for '{old_name}':")
        self.wait_window(d2)
        new_name = d2.result_name

        if not new_name:
            self._update_status("Rename canceled")
            return
        
        for rr in self.routines_list:
            if rr["name"] == new_name:
                self._update_status("Name already used. Rename aborted.")
                return
        
        routine_obj["name"] = new_name
        save_routines(self.routines_list)

        self._update_status(f"Renamed '{old_name}' to '{new_name}'")

    #Deleting routine
    def on_delete_routine(self):
        if not self.routines_list:
            self._update_status("No routines to delete")
            return
        
        d = SelectRoutineDialogue(self, "Delete Routine", "Select Routine to Delete:",
                                [r["name"] for r in self.routines_list])
        self.wait_window(d)
        del_name = d.result_name
        
        if not del_name:
            self._update_status("Delete canceled")
            return
        
        new_list = []
        found = False
        for r in self.routines_list:
            if r["name"] == del_name:
                found = True
            else:
                new_list.append(r)
        
        if not found:
            self._update_status("Routine not found. Nothing deleted")
            return
        
        self.routines_list = new_list
        save_routines(self.routines_list)
        self._update_status(f"Routine '{del_name}' deleted")

class RoutineNameDialogue(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.result_name = None

        lbl = ttk.Label(self, text=prompt)
        lbl.pack(padx=10,pady=5)

        self.entry_name = ttk.Entry(self, width=30)
        self.entry_name.pack(padx=10,pady=5)

        frm = ttk.Frame(self)
        frm.pack(pady=5)

        btn_ok = ttk.Button(frm, text="OK", command=self.on_ok)
        btn_ok.pack(side=tk.LEFT,padx=5)
        btn_cancel = ttk.Button(frm, text="Cancel", command=self.on_cancel)
        btn_cancel.pack(side=tk.LEFT,padx=5)

        self.update_idletasks()
        x = parent.winfo_rootx()+50
        y = parent.winfo_rooty()+50
        self.geometry(f"+{x}+{y}")
        self.grab_set()
        self.entry_name.focus()

    def on_ok(self):
        nm = self.entry_name.get().strip()
        self.result_name = nm if nm else None
        self.destroy()

    def on_cancel(self):
        self.result_name = None
        self.destroy()

class SelectRoutineDialogue(tk.Toplevel):
    def __init__(self, parent, title, prompt, routine_names):
        super().__init__(parent)
        self.title = title
        self.result_name = None

        lbl=ttk.Label(self,text=prompt)
        lbl.pack(padx=10,pady=5)

        self.routine_var = tk.StringVar()
        self.combo = ttk.Combobox(self, textvariable=self.routine_var,
                                  values=routine_names,
                                  state="readonly")
        self.combo.pack(padx=10,pady=5)

        frm = ttk.Frame(self)
        frm.pack(pady=5)

        btn_ok=ttk.Button(frm,text="OK",command=self.on_ok)
        btn_ok.pack(side=tk.LEFT,padx=5)
        btn_cancel=ttk.Button(frm,text="Cancel",command=self.on_cancel)
        btn_cancel.pack(side=tk.LEFT,padx=5)

        self.update_idletasks()
        x=parent.winfo_rootx()+50
        y=parent.winfo_rooty()+50
        self.geometry(f"+{x}+{y}")
        self.grab_set()
        self.combo.focus()

    def on_ok(self):
        sel = self.routine_var.get().strip()
        self.result_name = sel if sel else None
        self.destroy()

    def on_cancel(self):
        self.result_name = None
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
