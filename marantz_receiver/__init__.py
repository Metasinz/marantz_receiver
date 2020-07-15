"""
Marantz has an RS232 interface to control the receiver.

Not all receivers have all functions.
Functions can be found on in the xls file within this repository
"""
# import sys

# for p in sys.path:
#     print(p)


import codecs
import socket
from time import sleep 
from marantz_receiver.marantz_commands import CMDS # pylint: disable=import-error
import serial  
import threading
import telnetlib
import logging

DEFAULT_TIMEOUT = 0.5
DEFAULT_WRITE_TIMEOUT = 0.5

#logging.basicConfig(filename = 'debug.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s') #comment out for no file and default Level WARNING

class MarantzReceiver(object):
    """Marantz receiver."""

    def __init__(self, serial_port, timeout=DEFAULT_TIMEOUT,
                 write_timeout=DEFAULT_WRITE_TIMEOUT):
        """Create RS232 connection."""
        self.ser = serial.Serial(serial_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=timeout,
                                 write_timeout=write_timeout)
        self.lock = threading.Lock()

    def exec_command(self, domain, function, operator, value=None):
        """
        Write a command to the receiver and read the value it returns.
        The receiver will always return a value, also when setting a value.
        """
        raw_command = CMDS[domain][function]['cmd']
        if operator in CMDS[domain][function]['supported_operators']:
            if value is None:
                raise ValueError('No value provided')
            else:
                cmd = ''.join([raw_command, operator, str(value)])

        else:
            raise ValueError('Invalid operator provided %s' % operator)

        if not self.ser.is_open:
            self.ser.open()

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.lock.acquire()

        # Marantz uses the prefix @ and the suffix \r, so add those to the above cmd.
        final_command = ''.join(['@', cmd, '\r']).encode('utf-8')
        logging.debug ('Send Command %s',final_command)

        self.ser.write(final_command)

        msg = self.ser.read_until(bytes('\r'.encode()))
        self.lock.release()

        logging.debug ('Response from read msg %s', msg.decode())

        split_string = msg.decode().strip().split(':')

        logging.debug("Decoded split string %s", split_string)
        logging.debug ("Original command: %s\n", raw_command)
        # Check return value contains the same command value as requested. Sometimes the marantz gets out of sync. Ignore if this is the case
        if split_string[0] != ('@' + raw_command):
            logging.debug ("Send & Response command values dont match %s != %s - Ignoring returned value", split_string[0], '@' + raw_command )
            return None
        else:
             return split_string[1]
             # b'AMT:0\r will return 0

    def main_mute(self, operator, value=None):
        """Execute Main.Mute."""
        return self.exec_command('main', 'mute', operator, value)

    def main_power(self, operator, value=None):
        """Execute Main.Power."""
        return self.exec_command('main', 'power', operator, value)

    def main_volume(self, operator, value=None):
        """
        Execute Main.Volume.
        Returns string
        """
        vol_result = self.exec_command('main', 'volume', operator, value)
        if vol_result != None:
            return vol_result

    def main_source(self, operator, value=None):
        """Execute Main.Source."""
        result = self.exec_command('main', 'source', operator, value)
        """
        The receiver often returns the source value twice. If so take the
        second value as the source, otherwise return original
        """
        if result != None and len(result) == 2:
            logging.debug("Source Result: %s", result[1])
            return result[1]
        else:
            return result

    def main_autostatus (self, operator, value=None):
        """
        Execute autostatus.
        Not currently used but will allow two-way communications in future

        Returns int
        """
        return int(self.exec_command('main', 'autostatus', operator, value))
