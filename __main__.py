from bluetooth import Bluetooth
from devices import Devices, Device


if __name__ == "__main__":
    """
    Run the bluetooth devices
    """
    print("Starting Bluetooth Battery Level Checker...")

    bluetooth = Bluetooth(
        automatically_refresh=True
    )

    print("Bluetooth devices initialised.")

    devices: Devices = bluetooth.devices

    print(f"Found {len(devices)} bluetooth devices:")

    for device in devices:
        device: Device
        print(f"> {device.name} - {device.status} - {device.instanceID}")

    old_devices = []
    while True:
        new_devices = [device.state for device in bluetooth.devices]

        # Compare the current state with the previous state
        if new_devices != old_devices:
            print("Bluetooth devices have changed:")

            for device in bluetooth.devices:
                device: Device
                if device.status:
                    print(f"[✔] {device.name} - {device.batteryLevel}%")
                else:
                    print(f"[✘] {device.name}")

            old_devices = new_devices

        # Check if all devices are offline and shutdown the auto-refresh loop
        # Only to demonstrate the auto-refresh functionality
        if all(not device.status for device in bluetooth.devices):
            break

    bluetooth.stop_auto_refresh()
