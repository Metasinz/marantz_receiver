"""
Marantz has an RS232 interface to control the receiver.

Not all receivers have all functions.
Functions can be found on the
"""

import codecs
import socket
from time import sleep
from marantz_receiver.marantz_commands import CMDS
import serial  # pylint: disable=import-error
import threading
import telnetlib
import logging

DEFAULT_TIMEOUT = 1
DEFAULT_WRITE_TIMEOUT = 1

_LOGGER = logging.getLogger(__name__)

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
            if operator is ':' and value is None:
                raise ValueError('No value provided')

            if value is '?':
                cmd = ''.join([CMDS[domain][function]['cmd'], operator, str('?')])
            else:
                cmd = ''.join(
                    [CMDS[domain][function]['cmd'], operator, str(value)])
        else:
            raise ValueError('Invalid operator provided %s' % operator)

        if not self.ser.is_open:
            self.ser.open()

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.lock.acquire()

        final_command = ''.join(['@', cmd, '\r']).encode('utf-8')
        _LOGGER.info ('Send Command %s',final_command)
        self.ser.write(final_command)

        # Marantz uses the prefix @ and the suffix \r.
        msg = self.ser.read_until(bytes('\r'.encode()))
        self.lock.release()
        _LOGGER.info ('Response %s', msg.decode())

        split_string = msg.decode().strip().split(':')
        _LOGGER.info("Split String %s", split_string)
        _LOGGER.info ("Command: %s", raw_command)
        if split_string[0] != ('@' + raw_command):
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

        Returns int
        """
        vol_result = self.exec_command('main', 'volume', operator, value)
        if vol_result != None:
            return int(self.exec_command('main', 'volume', operator, value))

    def main_source(self, operator, value=None):
        """
        Execute Main.Source.

        Returns int
        """
        result = self.exec_command('main', 'source', operator, value)
        if result != None and len(result) == 2:
            _LOGGER.info("Source Result: %s", result[1])
            return result[1]
        else:
            return result

    def main_autostatus (self, operator, value=None):
        """
        Execute autostatus

        Returns int
        """
        return int(self.exec_command('main', 'autostatus', operator, value))
