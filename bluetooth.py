import subprocess
import concurrent.futures
import threading

from devices import Devices, Device


class Bluetooth:
    """
    Class to represent the Bluetooth devices.
    """

    def __init__(self, automatically_refresh: bool = False) -> None:
        """
        Initialise the Bluetooth devices.

        :param automatically_refresh: Whether to automatically refresh the Bluetooth devices
        :type automatically_refresh: bool
        """
        self.__devices: Devices = Devices(
            [Device(device) for device in self.getAllDevices()]
        )

        self.getStatusAudioDevices()

        def __set_instance_id(device):
            device.instanceID = self.getInstanceId(device.name)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(__set_instance_id, self.__devices))

        self.refresh()

        if automatically_refresh:
            self.__stop_refresh = False
            self.__refresh_thread = threading.Thread(
                target=self.__auto_refresh_loop, daemon=True
            )
            self.__refresh_thread.start()


    @property
    def devices(self) -> Devices:
        """
        Get the Bluetooth devices.

        :return: The Bluetooth devices
        :rtype: Devices
        """
        return self.__devices.devices


    def getAllDevices(self) -> list:
        """
        Get all Bluetooth devices.

        :return: A list of Bluetooth devices
        :rtype: list
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
        Get the status of the audio devices.

        :return: A list of Bluetooth devices
        :rtype: list
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
                for device in self.__devices:
                    device: Device
                    if device.name in name:
                        device.status = True
                        break
            else:
                name = service.split("Unknown")[0].strip()
                for device in self.__devices:
                    device: Device
                    if device.name in name:
                        device.status = False
                        break

        return self.__devices


    def getInstanceId(self, deviceName: str) -> str:
        """
        Get the instance ID of a Bluetooth device.

        :param deviceName: The name of the Bluetooth device
        :type deviceName: str
        :return: The instance ID of the Bluetooth device
        :rtype: str
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
        Get the battery level of a Bluetooth device.

        :param device: The Bluetooth device
        :type device: Device
        :return: The battery level of the Bluetooth device
        :rtype: int
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
        Refresh the battery level of all Bluetooth devices.
        """
        def __update_battery(device):
            if device.status:
                self.getBatteryLevel(device)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            list(executor.map(__update_battery, self.__devices))


    def refresh(self) -> None:
        """
        Refresh the Bluetooth devices status and battery level.
        """
        self.getStatusAudioDevices()
        self.refreshBatteryLevel()


    def __auto_refresh_loop(self):
        """
        Continuously refresh the Bluetooth devices in the background.
        """
        while self.__stop_refresh is False:
            try:
                self.refresh()
            except Exception as e:
                print(f"[Auto Refresh Error] {e}")


    def stop_auto_refresh(self):
        """
        Stops the automatic refresh background thread.
        """
        self.__stop_refresh = True
        if hasattr(self, "__refresh_thread"):
            self.__refresh_thread.join(timeout=5)
