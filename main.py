import os
import time
import ctypes
import pyautogui
from threading import Thread, Event
from tkinter import Tk, Button, Label, Entry

from pkg.window_management import initialize_application, close_application
from pkg.cheat_codes import perform_cheat_codes, close_cheat_codes
from pkg.device_handling_and_click_loop import check_device_connection, handle_connection_issue, perform_loop_actions
from pkg.click_handling import click_exam_row
from pkg.rescue_and_export_breaths import rescue_and_export_breaths
from pkg.db_handling import cleanup_excess_breaths, copy_last_exam
from pkg.config_offset import config


# Event object to control the loop safely between threads
running_event = Event()
thread: None | Thread = None  # Thread object to run the automation

# Declare the input fields as global variables
x_offset_entry = None
y_offset_entry = None


def start_automation():
    global running_event, thread
    running_event.set()  # Signal that the automation is running
    update_button_states()  # Disable relevant buttons
    thread = Thread(target=start_automation_main_call)  # Run the start_automation_main_call function in a separate thread
    thread.start()


def stop_automation():
    global running_event, thread
    running_event.clear()  # Signal that the automation should stop
    time.sleep(3)
    # Force close the "main" thread if it's still running
    if thread is not None and thread.is_alive():
        thread.join(timeout=0)
        thread = None
    # Force close the application if it's still running
    close_application()
    print("Automation stopped by the user.")
    update_button_states()  # Enable relevant buttons

    # Force quit the entire process
    os._exit(0)


def run_rescue_and_export_breaths():
    disable_all_buttons()  # Disable all buttons while running
    print("Running Rescue and Export Breaths script...")
    rescue_and_export_breaths()
    update_button_states()  # Re-enable buttons when done


def disable_all_buttons():
    """Disables all buttons on the UI."""
    start_button.config(state='disabled')
    stop_button.config(state='disabled')
    rescue_and_export_button.config(state='disabled')


def update_button_states():
    global running_event
    """Updates the state of buttons based on whether the automation is running."""
    if running_event.is_set():
        # Disable everything but the stop button while automation is running
        start_button.config(state='disabled')
        stop_button.config(state='normal')
        rescue_and_export_button.config(state='disabled')
    else:
        # Enable everything except the stop button when automation is not running
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        rescue_and_export_button.config(state='normal')


def on_closing():
    """Safely stop the automation and close the application when the window is closed."""
    stop_automation()  # Stop the automation loop
    root.quit()  # Close the Tkinter UI


def update_offsets():
    """Updates the x_offset and y_offset based on the input fields."""
    global x_offset_entry, y_offset_entry
    try:
        x_offset = int(x_offset_entry.get())  # Retrieve x_offset from the input field
        y_offset = int(y_offset_entry.get())  # Retrieve y_offset from the input field
        config.set_offsets(x_offset, y_offset)  # Update offsets in the config file
        print(f"Offsets updated: x_offset={x_offset}, y_offset={y_offset}")
    except ValueError:
        print("Please enter valid integer values for offsets.")


def start_automation_main_call():
    global running_event
    # Enable PyAutoGUI failsafe (moving the mouse to the corner stops execution)
    pyautogui.FAILSAFE = True

    # Copy the last exam in the database
    copy_last_exam()

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
            ctypes.windll.user32.MessageBoxW(0, "Screen resolution is not 1366x768.", "Error", 0)
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
        # First, call cleanup_excess_breaths at startup
        cleanup_excess_breaths()

        # Tkinter UI setup
        root = Tk()
        root.title("Automation Control")
        # Set the background color
        root.configure(bg='#F0F8FF')

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Window size
        window_width = 300
        window_height = 350  # Adjusted to accommodate new input fields

        # Calculate x and y positions to place the window at the bottom left
        x_position = 0
        y_position = screen_height - window_height

        # Set window geometry (widthxheight+x_offset+y_offset)
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Keep the window always on top without taking focus
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.9)  # Optional transparency

        # Labels and Buttons
        label = Label(root, text="Automation Control Panel", bg='#F0F8FF')
        label.pack(pady=10)

        start_button = Button(root, text="Start PyAutoPascoal", command=start_automation,
                              bg='#208FC8', activebackground='#F0F8FF')
        start_button.pack(pady=5)

        stop_button = Button(root, text="Stop PyAutoPascoal", command=stop_automation,
                             bg='#208FC8', activebackground='#F0F8FF')
        stop_button.pack(pady=5)

        rescue_and_export_button = Button(root, text="Rescue and Export Breaths", command=run_rescue_and_export_breaths,
                                          bg='#208FC8', activebackground='#F0F8FF')
        rescue_and_export_button.pack(pady=5)

        # Entry fields for x_offset and y_offset (declared as global earlier)
        x_offset_label = Label(root, text="X Offset:", bg='#F0F8FF')
        x_offset_label.pack(pady=5)
        x_offset_entry = Entry(root)
        x_offset_entry.pack(pady=5)
        x_offset_entry.insert(0, str(config.config.get('x_offset', 0)))  # Pre-populate with current value

        y_offset_label = Label(root, text="Y Offset:", bg='#F0F8FF')
        y_offset_label.pack(pady=5)
        y_offset_entry = Entry(root)
        y_offset_entry.pack(pady=5)
        y_offset_entry.insert(0, str(config.config.get('y_offset', 0)))  # Pre-populate with current value

        # Button to update the offsets
        update_button = Button(root, text="Update Offsets", command=update_offsets,
                               bg='#208FC8', activebackground='#F0F8FF')
        update_button.pack(pady=10)

        # Bind the closing action to stop automation safely
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Set initial button states
        update_button_states()

        # Mainloop to run the UI
        root.mainloop()

    except Exception as e:
        # Output error and display message box in case of failure
        print(f"Error: {e}")
        # Bring the message box to the foreground
        MB_ICONHAND = 0x00000010
        MB_TOPMOST = 0x00040000
        MB_SETFOREGROUND = 0x00010000
        uType = MB_ICONHAND | MB_TOPMOST | MB_SETFOREGROUND
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", uType)
