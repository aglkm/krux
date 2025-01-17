# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

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
import sys
from unittest import mock
from Maix import GPIO
from fpioa_manager import fm
import pygame as pg

PRESSED = 0
RELEASED = 1


class TactileButtons:
    """Interface with Buttons"""

    def __init__(self):
        self.enter = None
        self.page = None
        self.page_prev = None
        self.enter_event_flag = False
        self.page_event_flag = False
        self.page_prev_event_flag = False

    def init_enter(self, pin):
        """Register ENTER button IO"""
        fm.register(pin, fm.fpioa.GPIOHS21)
        self.enter = GPIO(GPIO.GPIOHS21, GPIO.IN, GPIO.PULL_UP)

    def init_page(self, pin):
        """Register PAGE button IO"""
        fm.register(pin, fm.fpioa.GPIOHS22)
        self.page = GPIO(GPIO.GPIOHS22, GPIO.IN, GPIO.PULL_UP)

    def init_page_prev(self, pin):
        """Register PAGE_PREV button IO"""
        fm.register(pin, fm.fpioa.GPIOHS0)
        self.page_prev = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)


buttons_control = TactileButtons()  # Singleton

sequence_executor = None

def register_sequence_executor(s):
    global sequence_executor
    sequence_executor = s

class Button:
    """Generic button handler format"""

    def __init__(self) -> None:
        pass

    def value(self):
        """Returns IO state"""
        return RELEASED

    def event(self):
        """Returns event state"""
        return False


class ButtonEnter:
    """Class to manage button ENTER state and events"""

    def __init__(self, pin) -> None:
        buttons_control.init_enter(pin)

    def value(self):
        """Returns the ENTER IO state"""
        if buttons_control.enter is not None:
            return buttons_control.enter.value()
        return RELEASED

    def event(self):
        """Returns the ENTER event state"""
        if buttons_control.enter is not None:

            if (
                sequence_executor
                and sequence_executor.key is not None
                and sequence_executor.key == pg.K_RETURN
                ):
                sequence_executor.key = None
                return True
            if buttons_control.enter_event_flag:
                buttons_control.enter_event_flag = False
                return True
        return False


class ButtonPage:
    """Class to manage button PAGE state and events"""

    def __init__(self, pin) -> None:
        buttons_control.init_page(pin)

    def value(self):
        """Returns the PAGE IO state"""
        if buttons_control.page is not None:
            return buttons_control.page.value()
        return RELEASED

    def event(self):
        """Returns the PAGE event state"""
        if buttons_control.page is not None:
            if (
                sequence_executor
                and sequence_executor.key is not None
                and sequence_executor.key == pg.K_DOWN
                ):
                sequence_executor.key = None
                return True
            if buttons_control.page_event_flag:
                buttons_control.page_event_flag = False
                return True
        return False


class ButtonPagePrev:
    """Class to manage button PAGE_PREV state and events"""

    def __init__(self, pin) -> None:
        buttons_control.init_page_prev(pin)

    def value(self):
        """Returns the PAGE_PREV IO state"""
        if buttons_control.page_prev is not None:
            return buttons_control.page_prev.value()
        return RELEASED

    def event(self):
        """Returns the PAGE_PREV event state"""
        if buttons_control.page_prev is not None:
            if (
                sequence_executor
                and sequence_executor.key is not None
                and sequence_executor.key == pg.K_UP
                ):
                sequence_executor.key = None
                return True
            if buttons_control.page_prev_event_flag:
                buttons_control.page_prev_event_flag = False
                return True
        return False


if "krux.buttons" not in sys.modules:
    sys.modules["krux.buttons"] = mock.MagicMock(
        TactileButtons=TactileButtons,
        ButtonEnter=ButtonEnter,
        ButtonPage=ButtonPage,
        ButtonPagePrev=ButtonPagePrev,
        PRESSED=PRESSED,
        RELEASED=RELEASED,
    )
