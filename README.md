# Purposefully Incomprehensible Auto Vento
## A pyautogui test in a mysterious closed app in a state that will cease to exist very soon

# Check python version
#### This is just to keep note of the version of python you are using
```cmd
py --version
```
#### This was tested with Python 3.11.8 btw
#### Using py instead of python is deliberate, it's a Windows thing in case you are using mingw, wsl, or something else

# Create a virtual environment
```cmd
py -m venv .venv
```

# Activate the virtual environment
```cmd
.\.venv\Scripts\activate
```
### or (probably not)
```cmd
.\.venv\bin\activate
```
_whichever works_

# Upgrade pip
```cmd
py -m pip install --upgrade pip
```

# Install the required packages
```cmd
py -m pip install -r requirements.txt
```
### or
### Manually install the required packages
```cmd
py -m pip install pyautogui
```
[//]: # (py -m pip install pygetwindow # not needed it seems)

# Run the script
```cmd
py main.py
```
