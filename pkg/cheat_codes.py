import pyautogui
import time

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
