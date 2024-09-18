import pyautogui
import pygetwindow
from time import sleep

# Focus on the application with the title 'Hermeto Pascoal'
# First, go to an exam full screen before running this script...
window_title = 'Hermeto Pascoal'
windows = pygetwindow.getWindowsWithTitle(window_title)
window = windows[0]
window.activate()
sleep(1)

x, y = 700, 325  # Coordinates at the ~center of a 1366x768 screen

print("Color at the center of the screen: ")
print(pyautogui.pixel(x, y))

# Define the positions
# Assuming screen resolution is 1366x768
button1_x = (1366 // 2) - 150  # Slightly to the left of center (adjust as needed)
exam_row_y = 220  # Adjusted value based on where the exam row is
button1_y = exam_row_y + 355  # Adjusted value based on the last click

# Move mouse to the button1
pyautogui.moveTo(button1_x, button1_y, duration=0.25)
# Click
pyautogui.click()
sleep(1)

print("Color at the center of the screen with first error popup: ")
print(pyautogui.pixel(x, y))

# Move the mouse to the center of the screen just to show where it is
pyautogui.moveTo(x, y, duration=0.35)

# Press enter to close the error popup
pyautogui.press('enter')
sleep(1)

print("Color at the center of the screen with the second error popup: ")
print(pyautogui.pixel(x, y))

# Press enter to close the error popup
pyautogui.press('enter')
sleep(1)
