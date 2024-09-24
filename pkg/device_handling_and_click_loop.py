import time
from threading import Event

import pyautogui

from pkg.cheat_codes import perform_cheat_codes, close_cheat_codes
from pkg.click_handling import click_exam_row
from pkg.serial_nuke import reset_all_serial_devices
from pkg.window_management import close_application, initialize_application
from pkg.popup_handling import check_for_popups, handle_popups

def perform_loop_actions(initial_color_at_popup_position, screen_width, running_event: Event):
    """Perform the loop actions while detecting popups and connection issues."""
    button1_x = screen_width // 2 - 225  # X position of first button
    button_y = 222 + 355  # Y position of the first button
    button2_x = button1_x + 200  # X position of second button
    mouse_move_duration = 0.1  # Mouse movement duration
    after_click_delay = 0.05  # Delay after clicks
    between_button_clicks_delay = 2.5  # Delay between button clicks
    exam_wait_time = 15  # Total wait time (in seconds) for the exam to finish
    popup_check_interval = 5  # Check for popups and connection every 5 seconds

    try:
        while running_event.is_set():  # Run as long as the running_event is set
            # Click the first button
            pyautogui.moveTo(button1_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked first button at ({button1_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            # Wait for the exam activity to complete, checking for popups
            total_wait_time = 0
            while total_wait_time < exam_wait_time and running_event.is_set():  # Keep checking while running_event is set
                print(f"Waiting for {exam_wait_time - total_wait_time} seconds...")
                time.sleep(popup_check_interval)
                total_wait_time += popup_check_interval

                # Check for popups
                if check_for_popups(initial_color_at_popup_position):
                    handle_popups(initial_color_at_popup_position)

                # Check for device connection issues
                if not check_device_connection():
                    print("Connection issue detected!")
                    handle_connection_issue(running_event)

            if not running_event.is_set():
                break

            # Click the second button to continue
            pyautogui.moveTo(button2_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked second button at ({button2_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            # Check for popups and connection issues again before continuing
            time.sleep(popup_check_interval)
            if check_for_popups(initial_color_at_popup_position):
                handle_popups(initial_color_at_popup_position)
            if not check_device_connection():
                print("Connection issue detected!")
                handle_connection_issue(running_event)

    except KeyboardInterrupt:
        print("Loop interrupted by user.")


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


def handle_connection_issue(running_event: Event):
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

    # Close the application if it's still running
    close_application()

    time.sleep(1) # Wait for the application to close

    # Reset all serial USB devices by toggling RTS/DTR signals
    reset_all_serial_devices()

    time.sleep(1)

    # Initialize the application (or raise an error if it can't be opened)
    initialize_application()
    time.sleep(1)
    running_event.set()

    time.sleep(4) # Wait for the application to load

    connection_issue_detected = False
    # Check for the device connection at startup
    if not check_device_connection():
        print("Connection issue detected at re-start!")
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
