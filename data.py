
# import the shared library built using the build_bindings.sh script
# usually something along the lines of protoserial.cpython-310-x86_64-linux-gnu.so
# needs to be placed in the same directory as this file
from protoserial import bytesbuff as _bytesbuff
from protoserial import fragment as _fragment

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

    @classmethod
    def from_unwrapped(cls, obj: _bytesbuff):
        ret = cls()
        ret._obj = obj
        return ret
    
    def len(self) -> int:
        return self._obj.size()

    def __len__(self) -> int:
        return self.len()

    def as_list(self) -> list:
        return self._obj.as_list()

    def __getitem__(self, key: int) -> int:
        return self._obj.at(key)

    def __repr__(self) -> str:
        return str(self._obj)


class fragment:
    def __init__(self, destination=0, data=bytesbuff()) -> None:
        self._obj = _fragment(destination, data._obj)

    @classmethod
    def from_unwrapped(cls, obj: _fragment):
        ret = cls()
        ret._obj = obj
        return ret

    def get_data(self) -> bytesbuff:
        return bytesbuff.from_unwrapped(self._obj.data())

    def get_source(self) -> int:
        return self._obj.source()

    def get_destination(self) -> int:
        return self._obj.destination()

    def set_destination(self, addr: int) -> None:
        return self._obj.set_destination(addr)



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

