import serial
import time
import serial.tools.list_ports

def reset_device(port_name):
    """Reset the device on the given serial port by manipulating RTS/DTR signals."""
    ser: serial.Serial | None = None
    try:
        # Open the serial port with specific settings
        ser = serial.Serial(
            port=port_name,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=3,
            rtscts=False,
            dsrdtr=False
        )
    except Exception as e:
        print(f"Failed opening serial device with error: {e}")
        return
    try:
        # Reset in download mode (DTR needs to be propagated with a explicit RTS set)
        ser.dtr = False  # Ensure DTR is false
        time.sleep(0.1875)  # 187.5ms
        ser.rts = False  # Ensure RTS is false
        time.sleep(0.1875)  # Wait 187.5ms
        ser.dtr = True  # Set RTS to true to enter download mode flag
        time.sleep(0.1875)  # Hold for 500ms prepare to propagate DTR
        ser.rts = False  # Set RTS to true to propagate DTR
        time.sleep(0.5)  # Hold for 500ms to reset
        ser.rts = True # Set RTS to true to reset
        time.sleep(0.1875)  # Hold for 187.5ms to reset
        ser.dtr = False  # Release DTR to exit reset
        time.sleep(0.1875)  # Wait 187.5ms for the system to stabilize
        ser.rts = True  # Release RTS to propagate DTR
        time.sleep(0.5)  # Wait 500ms for the system to stabilize
        ser.rts = False  # Release RTS to exit reset and clear the download mode flag

        time.sleep(2)

        # Reset in SoC mode
        # Step-by-step manipulation of RTS and DTR signals with timing
        time.sleep(0.1875)  # 187.5ms
        ser.dtr = False  # Ensure DTR is false
        time.sleep(0.1875)  # Wait 187.5ms
        ser.rts = False  # Ensure RTS is false
        time.sleep(0.1875)  # Wait 187.5ms
        ser.rts = True  # Set RTS to true to reset
        time.sleep(0.5)  # Hold for 500ms to reset
        ser.rts = False  # Release RTS to exit reset
        time.sleep(0.25)  # Wait 250ms for the system to stabilize

        print(f"Device on {port_name} reset successfully.")
    except Exception as e:
        print(f"Error resetting device on {port_name}: {e}")
    finally:
        ser.close()


def reset_all_serial_devices():
    """Find all available serial ports and reset devices on each."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return

    for port in ports:
        print(port.pid)
        if port.pid == 0x1001 and port.vid == 0x303A:
            print(f"Resetting device on port: {port.device}")
            reset_device(port.device)

def main():
    reset_all_serial_devices()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error {e}")

