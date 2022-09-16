
from types import FunctionType
from pathlib import Path

# import the shared library built using the build_bindings.sh script
# usually something along the lines of protoserial.cpython-310-x86_64-linux-gnu.so
# needs to be placed in the same directory as this file
from protoserial import interface_identifier as _interface_identifier
from protoserial import uart_interface as _uart_interface

from pyprotoserial.data import bytesbuff, fragment


class interface_identifier(_interface_identifier):
    pass

uart_interface_instance_count = 0

class uart_interface:
    def __init__(self, path: Path, address: int, broadcast_address: int, baud = 115200, 
        max_queue_size = 25, max_fragment_size = 64, buffer_size = 4096) -> None:

        assert path.exists() and path.is_block_device()
        assert address > 0
        assert broadcast_address > 0
        assert baud > 0
        assert max_queue_size > 0
        assert max_fragment_size >= 32
        assert buffer_size >= 128

        global uart_interface_instance_count
        
        self._obj = _uart_interface(
            str(path), 
            baud,
            uart_interface_instance_count,
            address,
            broadcast_address,
            max_queue_size,
            max_fragment_size,
            buffer_size
        )
        
        uart_interface_instance_count += 1


    def on_fragment_receive(self, callback: FunctionType) -> None:
        self._obj.on_fragment_receive(callback)

    def transmit_fragment(self, f: fragment) -> None:
        self._obj.transmit_fragment(f)



