# -*- coding: utf-8 -*-

"""package scinstr
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2019-2024
license   GPL v3.0+
brief     API dedicated to handle the Keysight 34461A digital multimeter.
"""

import logging
import time
import struct
import usb.core
import usbtmc

from scinstr.dmm.constants import (
    SDM3065X_TIMEOUT,
    SDM3065X_ID,
    SDM3065X_VID,
    SDM3065X_PID,
)

MAX_REQUEST_RETRIES = 5
MAX_READ_FLUSH_ATTEMPT = 10

# Multimeter functions
(
    CAP,
    CURR,
    CURRDC,
    VOLTAC,
    VOLTDC,
    VOLTDCRAT,
    RES,
    FRES,
    FRE,
    PER,
    TEMPRTD,
    TEMPFRTD,
    DIOD,
    CONT,
) = (
    "CAP",
    "CURR",
    "CURR:DC",
    "VOLT:AC",
    "VOLT:DC",
    "VOLT:DC:RAT",
    "RES",
    "FRES",
    "FRE",
    "PER",
    "TEMP:RTD",
    "TEMP:FRTD",
    "DIOD",
    "CONT",
)

# Integration time
(PLC002, PLC02, PLC1, PLC10, PLC100) = ("0.02", "0.2", "1", "10", "100")

# Voltage input range
(RANGE10MV, RANGE1V, RANGE10V, RANGE100V, RANGE1000V) = (
    "0.1",
    "1",
    "10",
    "100",
    "1000",
)

# Trigger source
(IMM, EXT, BUS) = ("IMM", "EXT", "BUS")


# =============================================================================
class Sdm3065xAbstract:
    """Abstract class to handling Sdm3065x digital multimeter device. Derived
    classes need to re-implement specific-protocol methods: connect(), close(),
    _write(), _read()...
    """

    def __del__(self):
        self.local()

    def _write(self, data: str) -> int:
        """Abstract protocol write process. Derived classes must implement
        the write process dedicated to the specific protocol used.
        :param data: data writes to device (str)
        :returns: number of writed byte
        """
        raise NotImplementedError("Method not implemented by derived class")

    def _read(self) -> str:
        """Abstract protocol read process. Derived classes must implement
        the read process dedicated to the specific protocol used.
        :returns: Message reads from device (str)
        """
        raise NotImplementedError("Method not implemented by derived class")

    def write(self, data: str) -> int:
        """A basic write method: writes "data" to device.
        :param data: data writes to device (str)
        :returns: number of writed byte, -1 in case of error
        """
        try:
            retval = self._write(data)
        except Exception as ex:
            logging.error(f"Write message:{data}, error: {ex}")
            return -1
        logging.debug(f"write: {data}")
        return retval

    def read(self) -> str | None:
        """A basic read method: read a message from device.
        :param length: length of message to read (int)
        :returns: Message reads from device, None if error (str)
        """
        try:
            retval = self._read()
        except Exception as ex:
            logging.error(f"Read error: {ex}")
            return None
        logging.debug(f"read: {retval}")
        return retval

    def query(self, msg: str) -> str | None:
        if self.write(msg) < 0:
            return None
        return self.read()

    def flush(self) -> bool:
        """Flush DMM HW buffer"""
        read_flush_attempt = MAX_READ_FLUSH_ATTEMPT
        while read_flush_attempt >= 0:
            try:
                _ = self._read()
            except usb.core.USBTimeoutError:
                return True
            read_flush_attempt -= 1

            logging.critical(f"flush({read_flush_attempt})")

        logging.error("DMM flush failed")
        return False

    def reset(self) -> bool:
        """Resets meter to its power-on state, sets all bits to zero in
        status byte register and all event registers and clear error queue.
        :returns: None
        """
        try:
            self.write("ABOR")
            self.write("*RST")
            self.write("*CLS")
        except Exception as ex:
            logging.error("reset failed %r", ex)
            return False
        time.sleep(2.0)
        logging.info("DMM reseted")
        return True

    def get_error(self) -> list[str] | None:
        """Return list of current error.
        :returns: list of current error (list of str)
        """
        errors = []
        while True:
            error = self.query("SYST:ERR?")
            if error is None or error == "":
                logging.error(f"Get error from device failed.")
                return None
            if "No error" in error:
                break
            errors.append(error)
        return errors

    def check_interface(self) -> bool:
        """Basic interface connection test: check id of device.
        Return True if interface with device is OK.
        :returns: status of interface with device (bool)
        """
        id_ = self.query("*IDN?")
        if id_ is None:
            return False
        if SDM3065X_ID in id_:
            return True
        return False

    def local(self) -> None:
        self.query("SYST:LOC:REL")

    def data_read(self) -> float | None:
        """Takes a measurement the next time the trigger condition is met.
        After the measurement is taken, the reading is placed in the output
        buffer. "data_read" will not cause readings to be stored in the Meter’s
        internal memory.
        Read method convenient for slow measurement.
        :returns: data read in buffer (float)
        """
        data = self.query("READ?")
        if data is None:
            logging.error(f"READ? returns None")
            return None
        try:
            data = float(data)
        except ValueError:
            logging.error(f"Invalid data {data}")
            return None
        return data


# =============================================================================
class Sdm3065xUsb(Sdm3065xAbstract):
    """Handle DMM device through USB connection."""

    def __init__(
        self, vendor_id=SDM3065X_VID, product_id=SDM3065X_PID, timeout=SDM3065X_TIMEOUT
    ):
        self._dev = usbtmc.Instrument(vendor_id, product_id)
        self._dev.timeout = timeout

    def _write(self, data: str):
        """Specific USB writing process.
        :param data: data writes to device (str)
        :returns: number of bytes sent (int)
        """
        self._dev.write(data)
        return len(data)

    def _read(self) -> str:
        """Specific USB reading process.
        :param length: length of message to read (int)
        :returns: Message reads from device (str)
        """
        request_retry = MAX_REQUEST_RETRIES
        while True:
            try:
                msg = self._dev.read()
            except struct.error:
                print(f"request_retry: {request_retry}")
                request_retry -= 1
                if request_retry < 0:
                    raise ConnectionError("_read() failed")
                continue
            break
        return msg

    def ask(self, msg):
        return self.query(msg)

    @property
    def timeout(self):
        """Get timeout on socket operations.
        :returns: timeout value in second (float)
        """
        return self._dev.timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout on socket operations.
        :param timeout: timeout value in second (float)
        :returns: None
        """
        self._dev.timeout = timeout
