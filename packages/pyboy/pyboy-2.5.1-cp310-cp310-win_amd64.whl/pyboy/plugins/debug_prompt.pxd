#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

from pyboy.logging.logging cimport Logger
from pyboy.plugins.base_plugin cimport PyBoyPlugin


cdef Logger logger

cdef class DebugPrompt(PyBoyPlugin):
    cdef dict rom_symbols
    cdef void handle_breakpoint(self) noexcept
