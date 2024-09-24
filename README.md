I apologize for that! Here's the cleaned-up README without unnecessary formatting:

# python_vento_automation

Python script to automate vento software procedures and perform tests via a graphical user interface (GUI).

## Setup Instructions

### _(setup)_ Check Python Version

Ensure you're using Python **3.11.8** or a compatible version:

```cmd
py --version
```

*Note:* Using `py` instead of `python` is a Windows-specific convention.

### _(setup)_ Create a Virtual Environment

```cmd
py -m venv .venv
```

### **(ALWAYS RUN BEFORE THE SCRIPTS)** Activate the Virtual Environment

```cmd
.\.venv\Scripts\activate
```

### _(setup)_ Upgrade pip

```cmd
py -m pip install --upgrade pip
```

### _(setup)_ Install the Required Packages

```cmd
py -m pip install pyautogui
py -m pip install pyserial
py -m pip install pyinstaller
```

### Building the Executable

To package the entire application as an executable:

```cmd
pyinstaller --onefile --windowed --name PyAutoPascoal main.py
```

This creates an executable named `PyAutoPascoal.exe` inside the `dist` folder.

---

## Running the Application

Once the executable is built, double-click the `PyAutoPascoal.exe` to launch the graphical interface.

### The UI Features:

- **Start PyAutoPascoal**: Starts the automated vento software test procedure.
- **Stop PyAutoPascoal**: Safely stops the automation process.
- **Run Rescue Breaths Script**: Runs the script to undelete breaths and gas readings from the SQLite database.
- **Run Show All Breaths Script**: Runs the script to generate a CSV file with all breaths and gas readings where `deleted_at` is `NULL`.

---

## Troubleshooting

### Database Issues

- Ensure the SQLite database is located at the correct path: `%AppData%\HermetoPascoal\db\vento-1.3.2.db`.
- If the automation fails due to a missing or locked database, close the vento software and re-open it.

### Common Script Errors

If you encounter errors such as:

- **`Ctrl+C` required**: In earlier versions, you may have had to stop scripts with `Ctrl+C`. This UI approach eliminates the need for manually interrupting the script.
- **`DEV: Cancelar sopros` message in the software**: Restart the vento software if the test gets stuck.

---

## Additional Automation Scripts

### Rescue Breaths Script

This script rescues deleted breaths and gas readings from the latest exam in the SQLite database.

#### How to Run:

- Open the `PyAutoPascoal.exe` and click the **Run Rescue Breaths Script** button.
- It will generate a CSV file in the current directory named `breaths_rescue_<timestamp>.csv`.

### Show All Breaths Script

This script generates a CSV file with all breaths and gas readings where `deleted_at` is `NULL`.

#### How to Run:

- Open the `PyAutoPascoal.exe` and click the **Run Show All Breaths Script** button.
- It will generate a CSV file in the current directory named `all_breaths_<timestamp>.csv`.

---

## Notes

- **Permissions**: Ensure the application has permission to read/write to the database file and output directory.
- **Timestamped Output Files**: The generated CSV files have timestamps to avoid overwriting previous outputs.
- **Virtual Environment**: Using the virtual environment ensures the system Python installation is unaffected.

---

By following the steps above, you can automate vento software procedures, perform tests, rescue deleted breaths, and generate complete lists of breaths and gas readings.

If you have any questions or need further assistance, feel free to reach out!