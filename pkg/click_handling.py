import pyautogui
import time


def click_exam_row(screen_width):
    """
    Click the necessary buttons to navigate to the exam row.
    This assumes a 1366x768 resolution and clicks at adjusted positions.
    """
    # First click: Order button (custom X and Y positions based on screen width)
    order_x = screen_width // 2 - 10  # Adjust X coordinate
    order1_y = 200  # Y coordinate for the first exam row
    mouse_move_duration = 0.8  # Duration for mouse movement
    after_click_delay = 0.1  # Delay after clicking

    # Move and click the first exam row
    pyautogui.moveTo(order_x, order1_y, duration=mouse_move_duration)
    pyautogui.click()
    print(f"Clicked at exam row position ({order_x}, {order1_y})")
    time.sleep(after_click_delay)

    # Second click: Click on the second position
    order2_y = 310  # Y coordinate for the second row
    pyautogui.moveTo(order_x, order2_y, duration=mouse_move_duration)
    pyautogui.click()
    print(f"Clicked at second row position ({order_x}, {order2_y})")
    time.sleep(after_click_delay)

    # Third click: Final button to confirm the action
    button1_x = screen_width // 2 - 225  # Adjust X coordinate
    exam_row_y = 222  # Final Y coordinate for the exam row
    pyautogui.moveTo(button1_x, exam_row_y, duration=mouse_move_duration)
    pyautogui.click()
    print(f"Clicked at final exam row position ({button1_x}, {exam_row_y})")
    time.sleep(after_click_delay)
