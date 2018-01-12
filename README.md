# marantz_receiver
Simple python API to connect to Marantz receivers through the RS232 interface. For the RS232 interface use the MarantzReceiver class.

Note that the RS232 interface is only tested with the Marantz SR6004.

The supported commands can easily be extended for receivers which support more commands.

For more information see the official documentation

Usage:
```
receiver = NADReceiver(serial_port)  # e.g. /dev/ttyUSB0

receiver.main_volume(':', '1')  #  will increase volume with 1 and return new value
receiver.main_volume(':', '2')  #  will decrease volume with 1 and return new value
receiver.main_volume(':', '-20')  # specify dB, will return new value
print(receiver.main_volume(':', '?'))  # will return current value


```

supported commands with supported operators for the RS232 interface

* main_volume [ : ]
* main_mute [ : ]
* main_power [ : ]
* main_source [ : ]
