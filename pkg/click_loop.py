import pyautogui
import time
from pkg.popup_handling import check_for_popups, handle_popups
from pkg.device_handling import check_device_connection, handle_connection_issue

def perform_loop_actions(initial_color_at_popup_position, screen_width):
    """
    Perform the loop actions while detecting popups and connection issues.
    """
    button1_x = screen_width // 2 - 225  # X position of first button
    button_y = 222 + 355  # Y position of the first button
    button2_x = button1_x + 200  # X position of second button
    mouse_move_duration = 0.1  # Mouse movement duration
    after_click_delay = 0.05  # Delay after clicks
    between_button_clicks_delay = 2.5  # Delay between button clicks
    exam_wait_time = 15  # Total wait time (in seconds) for the exam to finish
    popup_check_interval = 5  # Check for popups and connection every 5 seconds

    try:
        while True:
            # Click the first button
            pyautogui.moveTo(button1_x, button_y, duration=mouse_move_duration)
            pyautogui.click()
            print(f"Clicked first button at ({button1_x}, {button_y})")
            time.sleep(after_click_delay)
            time.sleep(between_button_clicks_delay)

            # Wait for the exam activity to complete, checking for popups
            total_wait_time = 0
            while total_wait_time < exam_wait_time:
                print(f"Waiting for {exam_wait_time - total_wait_time} seconds...")
                time.sleep(popup_check_interval)
                total_wait_time += popup_check_interval

                # Check for popups
                if check_for_popups(initial_color_at_popup_position):
                    handle_popups(initial_color_at_popup_position)

                # Check for device connection issues
                if not check_device_connection():
                    print("Connection issue detected!")
                    handle_connection_issue()

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
                handle_connection_issue()

    except KeyboardInterrupt:
        print("Loop interrupted by user.")
