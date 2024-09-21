import os
import subprocess
import shutil
import time
import ctypes

import pyautogui
import pygetwindow


def main():
    # Ensure PyAutoGUI failsafe is enabled
    pyautogui.FAILSAFE = True

    # Initialize the application
    initialize_application()

    # Perform initial cheat codes
    perform_cheat_codes()

    screen_width, screen_height = pyautogui.size()

    # Check for expected resolution
    if screen_width != 1366 or screen_height != 768:
        raise Exception(f"Screen resolution is {screen_width}x{screen_height}, expected 1366x768.")

    # Click on the exam row
    click_exam_row(screen_width)

    # Get the initial color at position (700, 325)
    initial_color = pyautogui.pixel(700, 325)

    # Start the loop actions
    perform_loop_actions(initial_color, screen_width)

    # Initialize the application again but skip launching
    initialize_application(skip_launch=True)

    time.sleep(1)

    # Close cheat codes at the end
    close_cheat_codes()
    print("Script completed successfully.")


def initialize_application(skip_launch=False):
    # Focus on the application with the title 'Hermeto Pascoal'
    window_title = 'Hermeto Pascoal'
    windows = pygetwindow.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.activate()
        print(f"Activated window titled '{window_title}'")
    else:
        print(f"No window found with title '{window_title}'")
        if skip_launch:
            raise Exception("Application window not found and skip_launch is True")
        # Try to find the executable in the system PATH
        executable_name = 'Hermeto Pascoal.exe'
        executable_path = shutil.which(executable_name)
        if not executable_path:
            # Construct the path using %ProgramFiles%
            program_files = os.environ.get('ProgramFiles')
            if program_files:
                executable_path = os.path.join(
                    program_files, 'Hermeto', 'Pascoal', 'Hermeto Pascoal.exe')
            else:
                raise Exception("Cannot find %ProgramFiles% environment variable")

        if os.path.exists(executable_path):
            # Launch the application
            subprocess.Popen([executable_path])
            print(f"Launched '{executable_path}'")
            # Wait for the application window to appear
            max_wait_time = 5  # Maximum wait time in seconds
            wait_interval = 0.5  # Interval between checks
            elapsed_time = 0

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
                raise Exception(
                    f"Still no window found with title '{window_title}' after launching the application")
        else:
            raise Exception(f"Executable not found at '{executable_path}'")

        pyautogui.moveTo(700, 325, duration=0.15)
        pyautogui.click()

    # Maximize the window using pygetwindow
    window.maximize()
    print("Maximized the window")


def perform_cheat_codes():
    # Define minimal sleep times
    key_press_delay = 0.005  # Time between keyDown and keyUp
    post_key_press_delay = 0.05  # Time after releasing keys before next action
    type_interval = 0.005  # Interval between keystrokes when typing
    after_type_delay = 0.1  # Delay after typing and pressing enter

    # First Cheat Code Call
    # Call the cheat code box (Ctrl+Alt+S+C+G)
    print("First Cheat Code Call")
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "debug" and press Enter
    print("Typing debug")
    pyautogui.typewrite('debug', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)

    # Call the cheat code box again
    print("Second Cheat Code Call")
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "del breaths" and press Enter
    print("Typing del breaths")
    pyautogui.typewrite('del breaths', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)

    # Press Ctrl+Alt+G
    print("Call to navigation")
    for key in ['ctrl', 'alt', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Call the CLOSING cheat code box to end "debug" mode
    print("Third cheat code call")
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Press Ctrl+E
    print("Exam tab")
    for key in ['ctrl', 'e']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'e']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Press Ctrl+Alt+G to turn off the navigation
    print("Close navigation")
    for key in ['ctrl', 'alt', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "debug" and press Enter
    print("Typing debug to close")
    pyautogui.typewrite('debug', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)


def click_exam_row(screen_width):
    # Define the positions
    # Assuming screen resolution is 1366x768
    button1_x = screen_width // 2 - 225  # Adjust as needed
    exam_row_y = 222  # Adjusted value based on where the exam row is
    mouse_move_duration = 0.4
    after_click_delay = 0.1

    # Move to exam_row_y and click
    pyautogui.moveTo(button1_x, exam_row_y, duration=mouse_move_duration)
    pyautogui.click()
    print(f"Clicked at exam row position ({button1_x}, {exam_row_y})")
    time.sleep(after_click_delay)


def perform_loop_actions(initial_color, screen_width):
    # Define the positions
    # Assuming screen resolution is 1366x768
    button1_x = screen_width // 2 - 225  # Slightly to the left of center (adjust as needed)
    button_y = 222 + 355  # Adjusted value based on the last click
    button2_x = button1_x + 200  # Adjusted value based on the last click
    # Define the timings
    mouse_move_duration = 0.1  # Duration for mouse movements
    after_click_delay = 0.05  # Delay after clicking
    between_button_clicks_delay = 2.5  # Delay between button clicks
    exam_wait_time = 15  # Total wait time (15 seconds)
    popup_check_interval = 5  # Check every 5 seconds

    try:
        while True:
            # Move to button1 and click
            pyautogui.moveTo(button1_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked at button1 position ({button1_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            # Wait for the activity to finish, checking for popups
            total_wait_time = 0
            while total_wait_time < exam_wait_time:
                print(f"Waiting for {exam_wait_time - total_wait_time} seconds...")
                time.sleep(popup_check_interval)
                total_wait_time += popup_check_interval
                if check_for_popups(initial_color):
                    handle_popups(initial_color)
            print("Exam activity completed.")

            # Move to button2 and click
            pyautogui.moveTo(button2_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked at button2 position ({button2_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            time.sleep(popup_check_interval)
            if check_for_popups(initial_color):
                handle_popups(initial_color)

    except KeyboardInterrupt:
        print("Loop interrupted by user.")
        # Place any cleanup or continuation code here


def check_for_popups(initial_color):
    current_color = pyautogui.pixel(700, 325)
    if current_color != initial_color:
        print("Popup detected!")
        return True
    else:
        return False


def handle_popups(initial_color):
    # Press Enter to close the first popup
    pyautogui.press('enter')
    time.sleep(0.5)
    # Check again for the second popup
    current_color = pyautogui.pixel(700, 325)
    if current_color != initial_color:
        # Press Enter to close the second popup
        pyautogui.press('enter')
        print("Second popup detected and closed.")
        time.sleep(0.5)
    else:
        print("No second popup detected.")


def close_cheat_codes():
    # Define minimal sleep times
    key_press_delay = 0.005
    post_key_press_delay = 0.05
    type_interval = 0.005
    after_type_delay = 0.1

    # Call the cheat code box to end "del breaths" mode
    print("Fourth cheat code call")
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "del breaths" and press Enter
    print("Typing del breaths to close")
    pyautogui.typewrite('del breaths', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        # Bring the message box to the foreground (doesn't work)
        MB_ICONHAND = 0x00000010
        MB_TOPMOST = 0x00040000
        MB_SETFOREGROUND = 0x00010000
        uType = MB_ICONHAND | MB_TOPMOST | MB_SETFOREGROUND
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", uType)

