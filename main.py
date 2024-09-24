import os
# import sys
import time
import ctypes
import pyautogui
# import subprocess
from threading import Thread, Event
from tkinter import Tk, Button, Label

from pkg.window_management import initialize_application, close_application
from pkg.cheat_codes import perform_cheat_codes, close_cheat_codes
from pkg.device_handling_and_click_loop import check_device_connection, handle_connection_issue, perform_loop_actions
from pkg.click_handling import click_exam_row
from pkg.show_all_breaths import show_all_breaths
from pkg.rescue_breaths import rescue_breaths


# Event object to control the loop safely between threads
running_event = Event()
thread: None | Thread = None  # Thread object to run the automation


def start_automation():
    global running_event, thread
    running_event.set()  # Signal that the automation is running
    update_button_states()  # Disable relevant buttons
    thread = Thread(target=main)  # Run the main function in a separate thread
    thread.start()


def stop_automation():
    global running_event, thread
    running_event.clear()  # Signal that the automation should stop
    time.sleep(3)
    # Force close tha "main" thread if it's still running
    if thread is not None and thread.is_alive():
        thread.join(timeout=0)
        thread = None
    # Force close the application if it's still running
    close_application()
    print("Automation stopped by the user.")
    update_button_states()  # Enable relevant buttons

    # Force quit the entire process
    os._exit(0)

    # # Force quit the entire process
    # sys.exit(0)


def run_rescue_breaths():
    disable_all_buttons()  # Disable all buttons while running
    print("Running Rescue Breaths script...")
    # subprocess.run(['py', 'python_rescue_breaths/main.py'])
    rescue_breaths()
    update_button_states()  # Re-enable buttons when done


def run_show_all_breaths():
    disable_all_buttons()  # Disable all buttons while running
    print("Running Show All Breaths script...")
    # subprocess.run(['py', 'python_show_all_breaths/main.py'])
    show_all_breaths()
    update_button_states()  # Re-enable buttons when done


def disable_all_buttons():
    """Disables all buttons on the UI."""
    start_button.config(state='disabled')
    stop_button.config(state='disabled')
    rescue_breaths_button.config(state='disabled')
    show_all_breaths_button.config(state='disabled')


def update_button_states():
    global running_event
    """Updates the state of buttons based on whether the automation is running."""
    if running_event.is_set():
        # Disable everything but the stop button while automation is running
        start_button.config(state='disabled')
        stop_button.config(state='normal')
        rescue_breaths_button.config(state='disabled')
        show_all_breaths_button.config(state='disabled')
    else:
        # Enable everything except the stop button when automation is not running
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        rescue_breaths_button.config(state='normal')
        show_all_breaths_button.config(state='normal')


def on_closing():
    """Safely stop the automation and close the application when the window is closed."""
    stop_automation()  # Stop the automation loop
    root.quit()  # Close the Tkinter UI


def main():
    global running_event
    # Enable PyAutoGUI failsafe (moving the mouse to the corner stops execution)
    pyautogui.FAILSAFE = True

    # Initialize the application (or raise an error if it can't be opened)
    initialize_application()

    time.sleep(3)  # Wait for the application to load

    connection_issue_detected = False
    # Check for the device connection at startup
    if not check_device_connection(with_mouse_move=True):
        print("Connection issue detected at startup!")
        handle_connection_issue(running_event)
        connection_issue_detected = True

    if not connection_issue_detected:
        # Perform the necessary cheat codes to set the application state
        perform_cheat_codes()

        # Get the screen dimensions
        screen_width, screen_height = pyautogui.size()

        # Check for the expected resolution
        if screen_width != 1366 or screen_height != 768:
            raise Exception(f"Screen resolution is {screen_width}x{screen_height}, expected 1366x768.")

        # Click on the exam row
        click_exam_row(screen_width)

        # Get the initial color at a specific position to detect popups
        initial_color_at_popup_position = pyautogui.pixel(700, 325)

        # Perform actions in a loop and detect connection issues and popups
        perform_loop_actions(initial_color_at_popup_position, screen_width, running_event)

        # After finishing, initialize the application again (skipping the launch)
        initialize_application(skip_launch=True)

        # Give a short delay before wrapping up
        time.sleep(1)

        # Close cheat codes at the end to reset any debug state
        close_cheat_codes()

        # After finishing, close the application
        close_application()
        print("Script completed successfully.")


# Exception handling for errors that occur during execution
if __name__ == "__main__":
    try:
        # Tkinter UI setup
        root = Tk()
        root.title("Automation Control")

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Window size
        window_width = 300
        window_height = 250

        # Calculate x and y positions to place the window at the bottom left
        x_position = 0
        y_position = screen_height - window_height

        # Set window geometry (widthxheight+x_offset+y_offset)
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Keep the window always on top without taking focus
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.8)  # Optional transparency

        # Labels and Buttons
        label = Label(root, text="Automation Control Panel")
        label.pack(pady=10)

        start_button = Button(root, text="Start PyAutoPascoal", command=start_automation)
        start_button.pack(pady=5)

        stop_button = Button(root, text="Stop PyAutoPascoal", command=stop_automation)
        stop_button.pack(pady=5)

        rescue_breaths_button = Button(root, text="Run Rescue Breaths Script", command=run_rescue_breaths)
        rescue_breaths_button.pack(pady=5)

        show_all_breaths_button = Button(root, text="Run Show All Breaths Script", command=run_show_all_breaths)
        show_all_breaths_button.pack(pady=5)

        # Bind the closing action to stop automation safely
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Set initial button states
        update_button_states()

        # Mainloop to run the UI
        root.mainloop()

    except Exception as e:
        # Output error and display message box in case of failure
        print(f"Error: {e}")
        # Bring the message box to the foreground (though this may not always work)
        MB_ICONHAND = 0x00000010
        MB_TOPMOST = 0x00040000
        MB_SETFOREGROUND = 0x00010000
        uType = MB_ICONHAND | MB_TOPMOST | MB_SETFOREGROUND
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", uType)
