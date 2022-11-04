
from time import sleep
import interfaces, data

interface = interfaces.uart('/dev/ttyACM0', 2, 255)

def pad_left(whatever, width):
    s = str(whatever)
    return (' ' * (width - len(s))) + s

def rx_callback(f: data.fragment):
    data = f.get_data().as_list()
    if len(data) == 2:
        print('act:', pad_left(data[0] - 64, 3), 'amp:', pad_left(data[1] - 64, 3))
    else:
        print('rx:', f)
        with open('values.txt', 'a') as file:
            for d in data:
                file.write(f'{d - 64}\n')

interface.on_fragment_receive(rx_callback)

try:
    while True:
        interface.main_task()
        sleep(0.001)
except Exception as e:
    print(e)

interface.close()
