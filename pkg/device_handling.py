import time
import pyautogui

from pkg.cheat_codes import perform_cheat_codes
from pkg.click_handling import click_exam_row
from pkg.serial_nuke import reset_all_serial_devices
from pkg.window_management import close_application, initialize_application


def check_device_connection(with_mouse_move=False):
    """
    Check if the device is connected by sampling the color at a specific location
    on the screen that indicates the device's connection status.

    The location checked (200px left and 100px down from the top-right corner)
    typically displays green when the device is connected.

    Returns:
        bool: True if the color at the specified location indicates the device
        is connected (predominantly green), False otherwise.
    """
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Coordinates to check for the device's connection indicator
    x = screen_width - 85  # 85 pixels left from the right edge
    y = 82  # 82 pixels down from the top edge

    if with_mouse_move:
        # Move the mouse to the specified coordinates
        pyautogui.moveTo(x, y, duration=0.8)

    # Sample the color at the specified screen coordinates
    color = pyautogui.pixel(x, y)

    # Return True if the color is predominantly green, otherwise return False
    return is_color_green(color)


def is_color_green(color):
    """
    Determine if the sampled color is predominantly green by checking if the
    green component is significantly higher than the red and blue components.

    Args:
        color (tuple): A tuple representing the RGB values of the sampled color.

    Returns:
        bool: True if the green component is at least 30 units higher than both
        the red and blue components, indicating the color is predominantly green.
    """
    r, g, b = color  # Unpack the RGB values of the sampled color

    # Return True if green is significantly higher than red and blue
    return g > r + 30 and g > b + 30


def handle_connection_issue():
    """
    Handle connection issues by resetting the serial USB devices and restarting
    the application. This function is called when it's determined that the
    device has disconnected or the app is unresponsive.

    It performs the following actions in sequence:
    1. Resets all serial devices (using RTS/DTR signals).
    2. Closes the application if it's open.
    3. Reinitializes the application.
    """
    # Log the connection issue for debugging purposes
    print("Device or app disconnected. Resetting devices.")

    # Reset all serial USB devices by toggling RTS/DTR signals
    reset_all_serial_devices()

    # Close the application if it's still running
    close_application()

    time.sleep(1) # Wait for the application to close

    # Initialize the application (or raise an error if it can't be opened)
    initialize_application()

    time.sleep(5) # Wait for the application to load

    # Check for the device connection at startup
    if not check_device_connection():
        print("Connection issue detected at re-start!")
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
