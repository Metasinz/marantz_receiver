from  marantz_receiver import MarantzReceiver

receiver = MarantzReceiver('COM3')  # e.g. /dev/ttyUSB0 or COM?

receiver.main_volume(':', '1')  #  will increase volume with 1 and return new value as string
receiver.main_volume(':', '2')  #  will decrease volume with 1 and return new value as string
receiver.main_volume(':', '-20')  # specify dB, will return new value

print(receiver.main_volume(':', '?'))  # will return current value as string
