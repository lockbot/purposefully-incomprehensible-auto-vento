import time
import ctypes
import pyautogui
from pkg.window_management import initialize_application
from pkg.cheat_codes import perform_cheat_codes, close_cheat_codes
from pkg.device_handling import check_device_connection, handle_connection_issue
from pkg.click_handling import click_exam_row
from pkg.click_loop import perform_loop_actions

def main():
    # Enable PyAutoGUI failsafe (moving the mouse to the corner stops execution)
    pyautogui.FAILSAFE = True

    # Initialize the application (or raise an error if it can't be opened)
    initialize_application()

    time.sleep(3) # Wait for the application to load

    # Check for the device connection at startup
    if not check_device_connection(with_mouse_move=True):
        print("Connection issue detected at startup!")
        handle_connection_issue()

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
    perform_loop_actions(initial_color_at_popup_position, screen_width)

    # After finishing, initialize the application again (skipping the launch)
    initialize_application(skip_launch=True)

    # Give a short delay before wrapping up
    time.sleep(1)

    # Close cheat codes at the end to reset any debug state
    close_cheat_codes()
    print("Script completed successfully.")


# Exception handling for errors that occur during execution
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Output error and display message box in case of failure
        print(f"Error: {e}")
        # Bring the message box to the foreground (though this may not always work)
        MB_ICONHAND = 0x00000010
        MB_TOPMOST = 0x00040000
        MB_SETFOREGROUND = 0x00010000
        uType = MB_ICONHAND | MB_TOPMOST | MB_SETFOREGROUND
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", uType)
