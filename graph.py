
import interfaces, data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

interface = None
for i in range(3):
    path = f'/dev/ttyACM{i}'
    try:
        interface = interfaces.uart(path, 2, 255)
        print(f'connected on {path}')
        break
    except Exception as e:
        print(f'failed to connect on {path}: {e}')


if not interface:
    print('unable to connect')
    exit(1)


def pad_left(whatever, width):
    s = str(whatever)
    return (' ' * (width - len(s))) + s

myo_data = [0] * 100

def rx_callback(f: data.fragment):
    data = f.get_data().as_list()
    if len(data) == 2:
        print('act:', pad_left(data[0] - 64, 3), 'amp:', pad_left(data[1] - 64, 3))
        myo_data.append(data[1] - 64)
        myo_data.pop(0)


fig, ax = plt.subplots()
line, = ax.plot(myo_data)
ax.set_ylim(0, 180)

interface.on_fragment_receive(rx_callback)

def update(data):
    line.set_ydata(data)
    return line,


def data_gen():
    while True:
        interface.main_task()
        yield myo_data


ani = animation.FuncAnimation(fig, update, data_gen, interval=50)
plt.show()

interface.close()
