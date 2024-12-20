# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
base_flasher.py
"""
import os
import typing
from serial import Serial
from serial.serialutil import SerialException
from serial.tools import list_ports
from src.utils.trigger import Trigger
from src.utils.kboot.build.ktool import KTool


class BaseFlasher(Trigger):
    """
    Base class to flash kboot.kfpkg on devices
    """

    VALID_BOARDS = ("goE", "dan")
    VALID_BAUDRATES = (
        9600,
        19200,
        28800,
        38400,
        57600,
        76800,
        115200,
        230400,
        460800,
        576000,
        921600,
        1500000,
    )

    def __init__(self):
        super().__init__()
        self.ktool = KTool()
        self.stop_thread = False

    @property
    def firmware(self) -> str:
        """Getter for firmware's full path"""
        self.debug(f"firmware::getter={self._firmware}")
        return self._firmware

    @firmware.setter
    def firmware(self, value: str):
        """Setter for firmware's firmware's full path"""
        if not os.path.exists(value):
            raise ValueError(f"File do not exist: {value}")

        self.debug(f"firmware::setter={value}")
        self._firmware = value

    @property
    def port(self) -> str:
        """Getter for device port system full path"""
        self.debug(f"ports::getter={self._port}")
        return self._port

    @port.setter
    def port(self, value: str):
        """Setter for available ports's full path by giving device name"""
        if value in ("amigo", "amigo_tft", "amigo_ips", "m5stickv", "bit", "cube"):
            vid = "0403"

        elif value in ("dock", "yahboom", "wonder_mv"):
            vid = "7523"

        else:
            raise ValueError(f"Device not implemented: {value}")

        self._available_ports_generator = list_ports.grep(vid)
        port = next(self._available_ports_generator)
        self._port = port.device
        self.debug(f"ports::setter={self._port}")

    @property
    def board(self) -> str:
        """Return a new instance of board"""
        self.debug(f"board::getter={self._board}")
        return self._board

    @board.setter
    def board(self, value: str):
        """Setter for board giving device name"""
        if value in (
            "amigo",
            "amigo_tft",
            "amigo_ips",
            "m5stickv",
            "bit",
            "yahboom",
            "cube",
        ):
            self._board = "goE"
            self.debug(f"board::setter={self._board}")

        elif value in ("dock", "wonder_mv"):
            self._board = "dan"
            self.debug(f"board::setter={self._board}")

        else:
            raise ValueError(f"Device not implemented: {value}")

    @property
    def baudrate(self) -> int:
        """Getter for baudrate"""
        self.debug(f"baudrate::getter={self._baudrate}")
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value: int):
        """Setter for baudrate"""
        if value in BaseFlasher.VALID_BAUDRATES:
            self.debug(f"baudrate::setter={value}")
            self._baudrate = value
        else:
            raise ValueError(f"Invalid baudrate: {str(value)}")

    @property
    def print_callback(self):
        """
        Getter for print_callback. KTool have two callbacks:
            - print_callback: a property of an instance of KTool that do KTool.log calls
            - callback: an argument of `process` method that parse the progress of flash
        """
        self.debug(f"print_callback::getter={self._print_callback}")
        return self._print_callback

    @print_callback.setter
    def print_callback(self, value: typing.Callable):
        """
        Getter for print_callback. KTool have two callbacks:
            - print_callback: a property of an instance of KTool that do KTool.log calls
            - callback: an argument of `process` method that parse the progress of flash
        """
        self.debug(f"print_callback::setter={value}")
        self._print_callback = value

    def is_port_working(self, port) -> bool:
        """Check if a port is working"""
        try:
            serialport = Serial(port)
            serialport.close()
            return True
        except SerialException:
            return False
