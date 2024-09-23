# python_vento_automation

Python script to automate vento software procedures and perform tests.

## _(setup)_ Check Python Version

This is just to keep note of the version of Python you are using.

```cmd
py --version
```

This was tested with **Python 3.11.8**.

*Note:* Using `py` instead of `python` is deliberate; it's a Windows thing.

## _(setup)_ Create a Virtual Environment

```cmd
py -m venv .venv
```

## **(ALWAYS RUN BEFORE THE SCRIPTS)** Activate the Virtual Environment

```cmd
.\.venv\Scripts\activate
```

## _(setup)_ Upgrade pip

```cmd
py -m pip install --upgrade pip
```

## _(setup)_ Manually Install the Required Packages

```cmd
py -m pip install pyautogui
```

## Run the Script

```cmd
py main.py
```

## Troubleshooting

If you run into trouble because you pressed or forgot to press `Ctrl+C`, changed windows, or did something during the start or the end of the execution, and the **DEV: Cancelar sopros** is still showing or the script doesn't run anymore as it's supposed to, stop the script with `Ctrl+C` (if it's running), and close the application (opening again is optional).

---

# After You Finish the Tests

Navigate to the `python_rescue_breaths` directory to run the script that undeletes breaths and associated gas readings in the SQLite database for the latest exam.

## Navigate to the `python_rescue_breaths` Directory

```cmd
cd python_rescue_breaths
```

## Run the Script

Since we're using the same virtual environment, you don't need to create a new one. Ensure you're still in the activated virtual environment.

```cmd
py main.py
```

## What the Script Does

- **Connects to the SQLite Database:**
  - Located at `%AppData%\HermetoPascoal\db\vento-1.3.2.db`.
- **Finds the Latest Exam:**
  - Queries the `exams` table for the highest `id`.
- **Undeletes Breaths and Gas Readings:**
  - For breaths associated with that exam where `deleted_at` is not `NULL`:
    - Sets `deleted_at` to `NULL` in both `breaths` and `breath_gas` tables.
    - Updates `breath_confirm` to one second after `date_time_finish`.
    - Updates `alert_start` to one second after `breath_confirm`.
- **Prints Breaths and Associated Gases:**
  - Outputs to the console and writes to a timestamped text file.

## Output

The script will generate an output similar to:

```
breaths.id 9
- breath_gas.gas H2 | breath_gas.ppm 22.5
- breath_gas.gas CH4 | breath_gas.ppm 22.1
breaths.id 10
- breath_gas.gas H2 | breath_gas.ppm 23.0
- breath_gas.gas CH4 | breath_gas.ppm 21.8
...
```

An output file with a name like `breaths_rescue_20240919_153045.txt` will be created in the same directory.

## Notes

- **Permissions:**
  - Ensure the script has the necessary permissions to read and write to the database file and the output directory.
- **Database Location:**
  - The database file is located at `%AppData%\HermetoPascoal\db\vento-1.3.2.db`.
  - `%AppData%` typically refers to `C:\Users\<YourUsername>\AppData\Roaming` on Windows.
- **Gases Enum:**
  - The `gas` column in `breath_gas` is an integer:
    - `1` corresponds to `H2`.
    - `2` corresponds to `CH4`.
    - Any other value is considered `unknown`.

## Troubleshooting

- **Database Not Found:**
  - Ensure that the database file exists at the specified location.
- **Permission Issues:**
  - Run the script with appropriate permissions if you encounter access denied errors.
- **Date Parsing Errors:**
  - If the `date_time_finish` format is unexpected, the script may raise an exception. Check the date formats in the database.
- **No Breaths Found:**
  - If the script outputs `No breaths with deleted_at IS NOT NULL for exam_id X`, it means there are no deleted breaths for the latest exam.

## Additional Information

- **Timestamped Output Files:**
  - Each time the script runs, it creates a new output file with a unique timestamp. This prevents overwriting previous outputs and helps track script executions.
- **Virtual Environment:**
  - Using a virtual environment ensures that dependencies are managed and the system Python installation remains unaffected.
- **No External Dependencies:**
  - The script uses only Python's standard library modules (`os`, `sqlite3`, `ctypes`, `datetime`).

---

By following the steps above, you should be able to successfully automate the vento software procedures, perform tests, and undelete breaths and their associated gas readings in your SQLite database.

If you have any questions or need further assistance, feel free to reach out!
