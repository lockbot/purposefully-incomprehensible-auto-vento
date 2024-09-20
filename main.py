import os
import subprocess
import shutil
import time
import ctypes

import pyautogui
import pygetwindow


def main():
    # Ensure PyAutoGUI failsafe is enabled (move mouse to top-left corner to abort)
    pyautogui.FAILSAFE = True

    # Focus on the application with the title 'Hermeto Pascoal'
    window_title = 'Hermeto Pascoal'
    windows = pygetwindow.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.activate()
        print(f"Activated window titled '{window_title}'")
    else:
        print(f"No window found with title '{window_title}'")
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

    # Maximize the window using pygetwindow
    window.maximize()
    print("Maximized the window")

    # Get screen size
    screen_width, screen_height = pyautogui.size()

    # Check for expected resolution
    if screen_width != 1366 or screen_height != 768:
        raise Exception(f"Screen resolution is {screen_width}x{screen_height}, expected 1366x768.")

    # Define minimal sleep times
    key_press_delay = 0.005  # Time between keyDown and keyUp
    post_key_press_delay = 0.05  # Time after releasing keys before next action
    #
    type_interval = 0.005  # Interval between keystrokes when typing
    after_type_delay = 0.1  # Delay after typing and pressing enter
    #
    mouse_move_duration = 0.4  # Duration for mouse movements
    after_click_delay = 0.1  # Delay after clicking
    #
    between_button_clicks_delay = 2.5  # Delay between button clicks
    exam_wait_time = 85  # 1 minute 25 seconds (85 seconds)

    # First Cheat Code Call
    # Call the cheat code box (Ctrl+Alt+S+C+G)
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)  # Wait between calling the cheat code box and typing

    # Type "debug" and press Enter
    pyautogui.typewrite('debug', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)  # Wait after pressing Enter

    # Call the cheat code box again
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "del breaths" and press Enter
    pyautogui.typewrite('del breaths', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)

    # Press Ctrl+Alt+G
    for key in ['ctrl', 'alt', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Call the CLOSING cheat code box to end "debug" mode
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Press Ctrl+E
    for key in ['ctrl', 'e']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'e']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Press Ctrl+Alt+G to turn off the navigation
    for key in ['ctrl', 'alt', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "debug" and press Enter
    pyautogui.typewrite('debug', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)

    # Now perform mouse clicks at positions defined by button1_x, exam_row_y, button1_y

    # Define the positions
    # Assuming screen resolution is 1366x768
    button1_x = screen_width // 2 - 225  # Slightly to the left of center (adjust as needed)
    exam_row_y = 220  # Adjusted value based on where the exam row is
    button_y = exam_row_y + 355  # Adjusted value based on the last click
    button2_x = button1_x + 200  # Adjusted value based on the last click

    # Move to exam_row_y and click
    pyautogui.moveTo(button1_x, exam_row_y, duration=mouse_move_duration)
    pyautogui.click()
    print(f"Clicked at exam row position ({button1_x}, {exam_row_y})")
    time.sleep(after_click_delay)

    # Define your variables
    button1_x = 500  # Example X-coordinate for button1
    button2_x = 600  # Example X-coordinate for button2
    button_y = 400  # Y-coordinate for both buttons
    mouse_move_duration = 0.1  # Duration for mouse movements
    after_click_delay = 0.05  # Delay after clicking

    try:
        while True:
            # Move to button1 and click
            pyautogui.moveTo(button1_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked at button1 position ({button1_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            # Wait for the activity to finish
            time.sleep(wait_interval)

            # Move to button2 and click
            pyautogui.moveTo(button2_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked at button2 position ({button2_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

    except KeyboardInterrupt:
        print("Loop interrupted by user.")
        # Place any cleanup or continuation code here

    # Call the CLOSING cheat code box again to end "del breaths" mode
    for key in ['ctrl', 'alt', 's', 'c', 'g']:
        pyautogui.keyDown(key)
    time.sleep(key_press_delay)
    for key in reversed(['ctrl', 'alt', 's', 'c', 'g']):
        pyautogui.keyUp(key)
    time.sleep(post_key_press_delay)

    # Type "del breaths" and press Enter
    pyautogui.typewrite('del breaths', interval=type_interval)
    pyautogui.press('enter')
    time.sleep(after_type_delay)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        # Display the error message in a Windows alert dialog box
        ctypes.windll.user32.MessageBoxW(0, f"Error: {e}", "Script Error", 0x10)
