
from types import FunctionType
from pathlib import Path

# import the shared library built using the build_bindings.sh script
# usually something along the lines of protoserial.cpython-310-x86_64-linux-gnu.so
# needs to be placed in the same directory as this file
from protoserial import bytesbuff as _bytesbuff
from protoserial import fragment as _fragment
from protoserial import interface_identifier as _interface_identifier
from protoserial import uart_interface as _uart_interface



class bytesbuff:
    int_init_error = "once the first argument is of type int, all following arguments must also by of type int"
    init_error = "none of the allowed argument combinations matched, refer to the doc string"

    def __init__(self, *args) -> None:
        # no arguments - default construct
        if not args:
            self._obj = _bytesbuff([])
        # single argument
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, bytearray) or isinstance(arg, bytes):
                self._obj = _bytesbuff(list(arg))
            elif isinstance(arg, list):
                self._obj = _bytesbuff(arg)
            elif isinstance(arg, str):
                self._obj = _bytesbuff(list(arg.encode('ascii')))
            else:
                assert False, self.init_error
        # n int arguments
        elif isinstance(args[0], int):
            assert all(isinstance(x, int) for x in args), self.int_init_error
            self._obj = _bytesbuff(list(args))

        else:
            assert False, self.init_error

    def len(self) -> int:
        return self._obj.size()

    def __len__(self) -> int:
        return self.len()

    def as_list(self) -> list:
        return self._obj.as_list()

    def __getitem__(self, key) -> int:
        return self._obj.at(key)

    def __repr__(self) -> str:
        return str(self._obj)


class interface_identifier(_interface_identifier):
    pass


class fragment:
    def __init__(self, destination=0, data=bytesbuff()) -> None:
        self._obj = _fragment(destination, data)

    def get_data(self) -> bytesbuff:
        return self._obj.data()

    def get_source(self) -> int:
        return self._obj.source()

    def get_destination(self) -> int:
        return self._obj.destination()

    def set_destination(self, addr: int) -> None:
        return self._obj.set_destination(addr)


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


if __name__ == "__main__":
    
    b = bytesbuff()
    assert len(b) == 0

    try:
        b = bytesbuff(1, 2, 'a')
        assert False
    except:
        pass

    b = bytesbuff('123')
    print(b)

    b = bytesbuff('42'.encode('ascii'))
    print(b)

    b = bytesbuff(1, 2, 3, 255)
    assert b[0] == 1
    assert len(b) == 4

    try:
        b[5]
        assert False
    except:
        pass

    print(b)
    print(list(b))




