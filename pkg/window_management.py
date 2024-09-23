import os
import subprocess
import pyautogui
import pygetwindow
import shutil
import time


def initialize_application(skip_launch=False):
    """
    Initialize the 'Hermeto Pascoal' application by either launching it or re-focusing
    it, depending on whether it's already running. If the application is not running
    and 'skip_launch' is False, it will attempt to launch the application.

    Args:
        skip_launch (bool): If True, the function will not attempt to launch the
        application, only re-focus it if it exists. This is useful when re-focusing
        the app after stopping the script with 'Ctrl+C'.
    """
    # Define the application window title
    window_title = 'Hermeto Pascoal'

    # Search for windows with the specified title
    windows = pygetwindow.getWindowsWithTitle(window_title)

    if windows:
        # If the window is found, activate it
        window = windows[0]
        window.activate()
        print(f"Activated window titled '{window_title}'")
    else:
        print(f"No window found with title '{window_title}'")

        # If skip_launch is True, do not attempt to relaunch the application
        if skip_launch:
            raise Exception("Application window not found and skip_launch is True")

        # Locate the executable for 'Hermeto Pascoal'
        executable_name = 'Hermeto Pascoal.exe'
        executable_path = shutil.which(executable_name)

        # If the executable is not found in the system path, build the path manually
        if not executable_path:
            program_files = os.environ.get('ProgramFiles')
            if program_files:
                executable_path = os.path.join(program_files, 'Hermeto', 'Pascoal', executable_name)
            else:
                raise Exception("Cannot find %ProgramFiles% environment variable")

        # If the executable is found, launch the application
        if os.path.exists(executable_path):
            subprocess.Popen([executable_path])
            print(f"Launched '{executable_path}'")

            # Wait for the application window to appear (with a timeout)
            max_wait_time = 5  # Maximum wait time in seconds
            wait_interval = 0.5  # Interval between checks
            elapsed_time = 0

            # Keep checking for the window until it appears or the timeout is reached
            while elapsed_time < max_wait_time:
                windows = pygetwindow.getWindowsWithTitle(window_title)
                if windows:
                    window = windows[0]
                    window.activate()
                    print(f"Activated window titled '{window_title}'")
                    break
                else:
                    time.sleep(wait_interval)
                    elapsed_time += wait_interval
            else:
                raise Exception(f"Still no window found with title '{window_title}' after launching the application")
        else:
            raise Exception(f"Executable not found at '{executable_path}'")

        # After launching the app, simulate a click at position (700, 325)
        pyautogui.moveTo(700, 325, duration=0.15)
        pyautogui.click()

    # Maximize the application window once it's active
    window.maximize()
    print("Maximized the window")


def close_application():
    """
    Close the 'Hermeto Pascoal' application by attempting to close its window.
    After issuing the close command, it handles a potential popup that asks for
    confirmation by simulating the pressing of 'Enter'.
    """
    # Define the application window title
    window_title = 'Hermeto Pascoal'

    # Search for windows with the specified title
    windows = pygetwindow.getWindowsWithTitle(window_title)

    if windows:
        # If the window is found, close it
        window = windows[0]
        window.close()
        print(f"Closed window titled '{window_title}'")

        time.sleep(1) # Wait briefly after closing the window

        # After attempting to close, handle any confirmation popup by pressing 'Enter'
        pyautogui.press('enter')
        time.sleep(0.5)  # Wait briefly to ensure the popup is handled
    else:
        # If no window is found, log that the application is not running
        print(f"No window found with title '{window_title}'")
