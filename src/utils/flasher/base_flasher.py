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
from ..trigger import Trigger


class BaseFlasher(Trigger):
    """
    Base class to flash kboot.kfpkg on devices
    """

    VALID_BOARDS = ("goE", "dan")

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
    def ports(self) -> typing.Generator:
        """Getter for firmware's full path"""
        self.debug(f"ports::getter={self._ports}")
        return self._ports

    @ports.setter
    def ports(self, value: typing.Generator):
        """Setter for available ports's full path"""
        self.debug(f"port::setter={value}")
        self._ports = value

    @property
    def board(self) -> str:
        """Return a new instance of board"""
        self.debug(f"board::getter={self._board}")
        return self._board

    @board.setter
    def board(self, value: str):
        """Setter for board"""
        if value in BaseFlasher.VALID_BOARDS:
            self.debug(f"board::setter={value}")
            self._board = value
        else:
            raise ValueError(f"Invalid board: {value}")
