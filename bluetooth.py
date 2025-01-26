import subprocess

from devices import Devices, Device


class Bluetooth:
    """
    Class to represent the bluetooth devices
    """
    def __init__(self) -> None:
        """
        Initialise the bluetooth devices
        """
        print("Initialising bluetooth...")
        self.devices: Devices = Devices()


        print("Getting bluetooth devices...")
        for device in self.getAllDevices():
            self.devices.add(Device(device))

        print(f"Found {len(self.devices)} bluetooth devices")


        print("Getting bluetooth devices status...")
        self.getStatusAudioDevices()


        print("Getting instances IDs...")
        for device in self.devices:
            device: Device
            device.instanceID = self.getInstanceId(device.name)

            print(f"> {device.name} - {device.status} - {device.instanceID}")


    def getAllDevices(self) -> list:
        """
        Get all bluetooth devices
        
        :return: A list of bluetooth devices
        """
        bluetoothDevices = subprocess.check_output(
            [
                "powershell",
                "$bluetoothDeviceIdPattern = 'BTHENUM\\DEV_';",
                "$bluetoothDevices = Get-PnpDevice -Class 'Bluetooth' | Where-Object { $_.DeviceID -like \"$bluetoothDeviceIdPattern*\" };",
                "if ($bluetoothDevices) {",
                "$uniqueNames = $bluetoothDevices | Select-Object -ExpandProperty FriendlyName -Unique;",
                "foreach ($name in $uniqueNames) {",
                "Write-Host \"$name\"",
                "}",
                "}",
            ]
        ).decode("utf-8", errors="replace")

        return bluetoothDevices.strip().split("\n")


    def getStatusAudioDevices(self) -> list:
        """
        Get the status of the audio devices
        
        :return: A list of bluetooth devices
        """
        try:
            services = subprocess.check_output(
                [
                    "powershell",
                    "Get-PnPDevice",
                    "|",
                    "Where-Object",
                    "-FilterScript",
                    "{",
                    "$_.Class",
                    "-eq",
                    "'AudioEndpoint'",
                    "}",
                    "|",
                    "Select-Object",
                    "FriendlyName,",
                    "Status",
                ]
            ).decode("utf-8", errors="replace")
        except subprocess.CalledProcessError:
            return ""


        for service in services.strip().split("\r\n"):
            if "OK" in service:
                name = service.split("OK")[0].strip()

                for device in self.devices:
                    device: Device
                    if device.name in name:
                        device.status = True
                        break
            else:
                name = service.split("Unknown")[0].strip()

                for device in self.devices:
                    device: Device
                    if device.name in name:
                        device.status = False
                        break

        return self.devices


    def getInstanceId(self, deviceName: str) -> str:
        """
        Get the instance ID of a bluetooth device
        
        :param deviceName: The name of the bluetooth device
        :return: The instance ID of the bluetooth device
        """
        isinstanceId = subprocess.check_output(
            [
                "powershell",
                "Get-PnpDevice",
                "-FriendlyName",
                f"\"*{deviceName}*\"",
                "|",
                "ForEach-Object",
                "{",
                "$local:test = $_ |",
                "Get-PnpDeviceProperty",
                "-KeyName",
                "\"{104EA319-6EE2-4701-BD47-8DDBF425BBE5} 2\"",
                "|",
                "Where",
                "Type",
                "-ne",
                "Empty;",
                "if",
                "($test)",
                "{",
                "$($test.InstanceId)",
                "}",
                "}",
            ]
        ).decode("utf-8")

        return isinstanceId.strip()


    def getBatteryLevel(self, device: Device) -> int:
        """
        Get the battery level of a bluetooth device
        
        :param device: The bluetooth device
        :return: The battery level of the bluetooth device
        """
        battery_level = subprocess.check_output(
            [
                "powershell",
                "Get-PnpDeviceProperty",
                "-InstanceId",
                f"\"{device.instanceID}\"",
                "-KeyName",
                "\"{104EA319-6EE2-4701-BD47-8DDBF425BBE5} 2\"",
                "|",
                "%",
                "Data",
            ]
        ).decode("utf-8")

        device.batteryLevel = int(battery_level)

        return device.batteryLevel


    def refreshBatteryLevel(self) -> None:
        """
        Refresh the battery level of all bluetooth devices
        """
        for device in self.devices:
            device: Device
            if device.status:
                self.getBatteryLevel(device)


    def refresh(self) -> None:
        """
        Refresh the bluetooth devices status and battery level
        """
        self.getStatusAudioDevices()
        self.refreshBatteryLevel()


    def run(self) -> None:
        """
        Run the bluetooth devices
        """
        print("\nUpdating bluetooth devices...")
        self.refresh()

        for device in self.devices:
            device: Device
            if device.status:
                print(f"[✔] {device.name} - {device.batteryLevel}%")
            else:
                print(f"[✘] {device.name}")


if __name__ == "__main__":
    """
    Run the bluetooth devices
    """
    bluetooth = Bluetooth()

    while True:
        bluetooth.run()
