import serial.tools.list_ports
import re

def get_serial_devices():
    # List all serial ports
    ports = serial.tools.list_ports.comports()

    # Iterate through all serial ports and gather details
    for port in ports:
        device = port.device
        hwid = port.hwid

        print(f"Device: {device}")

        # Updated regex to handle "VID:PID=XXXX:YYYY" format
        vid_pid_match = re.search(r'VID:PID=([0-9A-F]+):([0-9A-F]+)', hwid, re.I)
        if vid_pid_match:
            vid_hex = vid_pid_match.group(1)
            pid_hex = vid_pid_match.group(2)
            vid_dec = int(vid_hex, 16)
            pid_dec = int(pid_hex, 16)

            print(f"VID: {vid_dec} (0x{vid_hex.upper()})")
            print(f"PID: {pid_dec} (0x{pid_hex.upper()})")
        else:
            print("No VID/PID found")

        # Print additional information from port (such as description, manufacturer, etc.)
        print(f"Description: {port.description}")
        print(f"Manufacturer: {port.manufacturer}")
        print(f"HWID: {hwid}")
        print(f"Location: {port.location}")
        print(f"Serial Number: {port.serial_number}")
        print("-" * 40)

if __name__ == "__main__":
    get_serial_devices()
