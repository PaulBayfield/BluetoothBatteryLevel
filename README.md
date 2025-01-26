<div align="center">
<img src="logo.png" alt="Bluetooth Logo"/>
  
# Bluetooth Battery Level Indicator (Windows)
A repository for a simple Windows script that displays the battery level of your Bluetooth devices.

</div>
  
# 📖 • Table of contents

- [🚀 • Presentation](#--presentation)
- [📦 • Installation](#--installation)
- [📄 • Usage](#--usage)
- [📃 • Credits](#--credits)
- [📝 • License](#--license)

# 🚀 • Presentation

Another random project I made to get the battery level of my Bluetooth devices. This script is made for Windows and uses powershell commands to:
1. Get the list of all Bluetooth devices
2. Get the instance ID of each device
3. Get the status of each device
4. Get the battery level of each device

# 📦 • Installation

Clone the repository.

```bash
git clone https://PaulBayfield/BluetoothBatteryLevel.git
cd BluetoothBatteryLevel
```

# 📄 • Usage

Run the [`bluetooth.py`](bluetooth.py) file.

```bash	
python3 bluetooth.py
```

You should see an output similar to this:

```bash
Initialising bluetooth...
Getting bluetooth devices...
Found 2 bluetooth devices
Getting bluetooth devices status...
Getting instances IDs...
> Phone - False - 
> Headphones - True - BTHENUM\{000...}_VID&000... 

Updating bluetooth devices...
[✘] Phone
[✔] Headphones - 30%
```


# 📃 • Credits

Made by [Paul Bayfield](https://github.com/PaulBayfield).

# 📝 • License

This project is under the [Apache 2.0](LICENSE) license.

```
Copyright 2025 Paul Bayfield

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
