import pyautogui
import time

def check_for_popups(initial_color_at_popup_position):
    """
    Check for the presence of a popup by comparing the current color at a specific
    screen position (700, 325) with an initial reference color. Popups will typically
    change the screen's appearance, and this color check helps detect them.

    Args:
        initial_color_at_popup_position (tuple): The reference RGB color value of the
        screen at the position (700, 325) when no popup is present.

    Returns:
        bool: True if the color at position (700, 325) has changed, indicating a popup,
        otherwise False.
    """
    # Get the current color at screen position (700, 325)
    current_color = pyautogui.pixel(700, 325)

    # Compare the current color with the initial color
    if current_color != initial_color_at_popup_position:
        # Popup detected, the color has changed
        return True

    # No popup detected, the color hasn't changed
    return False


def handle_popups(initial_color_at_popup_position):
    """
    Handle popups by simulating the pressing of the 'Enter' key to dismiss them.
    This function checks for a popup at position (700, 325) and, if found, dismisses
    it by pressing 'Enter' once or twice, depending on how persistent the popup is.

    Args:
        initial_color_at_popup_position (tuple): The reference RGB color value of the
        screen at the position (700, 325) when no popup is present.
    """
    # Press 'Enter' to dismiss the first popup (if any)
    pyautogui.press('enter')
    time.sleep(0.5)  # Wait a moment for the popup to disappear

    # Check the color again at position (700, 325)
    current_color = pyautogui.pixel(700, 325)

    # If the color still differs from the initial color, press 'Enter' again
    if current_color != initial_color_at_popup_position:
        pyautogui.press('enter')  # Handle the second popup (if another persists)
        time.sleep(0.5)  # Wait to ensure the popup is fully dismissed
