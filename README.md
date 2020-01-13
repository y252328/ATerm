# ATerm
This project, ATerm, is a simple serial terminal implemented in Python and Qt. \
ATerm not only can send/receive ascii text but also send file(binary).

![](https://i.imgur.com/2acN4NY.png)

## Looking for the C++ version ATerm
For C++ version, click [here](https://github.com/y252328/ATerm-CPP)

## Requirement
* python==3.6
* pyserial==3.4
* PySide2==5.13.2
* PyYAML==5.2

## Setting
This section will talk about how to config ATerm(e.g., priority of ports, default baud rate, etc.) through writing the setting file.
The setting file is a YAML file and place in the directory of program. There are following options in file.
* __priority__: a list of string. ATerm will compare available com ports with this list and select the highest priority and available port on refresh bottom clicked.
* __baud__: the key/value pairs. Key is the port name. Value is the baud rate.
* __path__: a string. Default directory of open file dialog of sending file.
* __custom_baud__: a list of integer. ATerm will add this list into the baud rate combo box.(1.3.0+)

### Example
```yaml
---
baud:
  ch340: 9600
  cp210: 115200

path: D:/terminal/

custom_baud:
- 15151

priority:
- cp210
- ch340
```

> note: The name in baud and priority don't need identical to the name in ports combo box.
