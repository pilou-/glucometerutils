# -*- coding: utf-8 -*-
"""Common routines and base driver class for serial-based meters.
"""

__author__ = 'Diego Elio Pettenò'
__email__ = 'flameeyes@flameeyes.eu'
__copyright__ = 'Copyright © 2017, Diego Elio Pettenò'
__license__ = 'MIT'

import logging

import serial

from glucometerutils import exceptions


class SerialDevice(object):
    """A Serial-connected glucometer driver base.

    This class does not implement an actual driver by itself, but provides an
    easier access to the boilerplate code required for pyserial.

    This helper assumes that communication happens on a standard 8n1
    configuration, with variable baudrate and no hardware flow control.

    The actual drivers should set the following parameters:

      BAUDRATE: (int) the speed the serial port should be opened at.
      DEFAULT_CABLE_ID: (string) USB Vendor/Product ID pair, in format
        abcd:abcd, of the default cable for the meter, in case the user
        didn't pass an explicit device driver.

    Optional parameters available:

      TIMEOUT: (float, default: 1) the read timeout in seconds as defined by
        pyserial.

    After initialization, the following attributes can be used by the driver:
      serial_: (serial.Serial) the open Serial object.

    """

    BAUDRATE = None
    DEFAULT_CABLE_ID = None

    TIMEOUT = 1

    def __init__(self, device, with_ketone=False):
        assert self.BAUDRATE is not None

        self.with_ketone = with_ketone

        if not device and self.DEFAULT_CABLE_ID:
            logging.info(
                'No --device parameter provided, looking for default cable.')
            device = 'hwgrep://' + self.DEFAULT_CABLE_ID

        if not device:
            raise exceptions.CommandLineError(
                'No --device parameter provided, and no default cable known.')

        self.serial_ = serial.serial_for_url(
            device,
            baudrate=self.BAUDRATE,
            timeout=self.TIMEOUT,
            writeTimeout=None,
            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=True, rtscts=False, dsrdtr=False)
