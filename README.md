# ATerm
This project, ATerm, is a simple serial terminal implemented in Python and Qt. \
ATerm not only can send/recive ascii text but also send file(binary).

![](https://i.imgur.com/iVVejkq.png)

## Setting
This section will talk about how to config ATerm(e.g., priority of ports, default baud rate, etc.) through writing the setting file.
The setting file is a YAML file and place in directory of program. There are following options in file.
* priority: a list. ATerm will compare available com ports with this list and select the highest priority and available port on refresh bottom clicked.
* baud: the key/value pairs. Key is the port name. Value is the baud rate.
* path: a string. Default directory of open file dialog of sending file.

### example
```yaml
---
baud:
  ch340: 9600
  cp210: 115200

path: D:/terminal/

priority:
- cp210
- ch340
```

> note: The name in baud and priority don't need identical to the name in ports combobox.

## Requirement
* python==3.6
* pyserial==3.4
* PySide2==5.13.2
* PyYAML==5.2