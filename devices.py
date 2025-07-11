import hashlib


class Device:
    """
    Class to represent a bluetooth device
    """
    def __init__(self, name: str) -> None:
        """
        Initialise a bluetooth device
        
        :param name: The name of the device
        """
        self.__name = name
        self.__status = False
        self.__instanceID = ""
        self.__batteryLevel = -1


    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def status(self):
        return self.__status


    @status.setter
    def status(self, value):
        self.__status = value


    @property
    def instanceID(self):
        return self.__instanceID


    @instanceID.setter
    def instanceID(self, value):
        self.__instanceID = value


    @property
    def batteryLevel(self):
        return self.__batteryLevel


    @batteryLevel.setter
    def batteryLevel(self, value):
        self.__batteryLevel = value


    @property
    def state(self) -> str:
        """
        Get the state of the device.
        
        :return: The state of the device
        :rtype: str
        """
        return hashlib.blake2b(
            f"{self.name}{self.status}{self.instanceID}{self.batteryLevel}".encode(),
            digest_size=16
        ).hexdigest()


class Devices:
    """
    Class to represent a list of bluetooth devices
    """
    def __init__(self, devices: list) -> None:
        """
        Initialise a list of bluetooth devices
        """
        self.__devices = devices


    @property
    def devices(self):
        return self.__devices


    def add(self, device: Device):
        self.__devices.append(device)


    def remove(self, device: Device):
        self.__devices.remove(device)


    def __getitem__(self, name):
        for device in self.__devices:
            device: Device
            if device.name == name:
                return device

        return None


    def __iter__(self):
        return iter(self.__devices)
    

    def __str__(self) -> str:
        return str(self.__devices)
    

    def __repr__(self) -> str:
        return str(self.__devices)
    

    def __len__(self) -> int:
        return len(self.__devices)
