import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from celluloid import Camera
from scipy import signal
import scipy
import os
import pickle
import time

from Detecter import Detecter, PowerRecorder, PowerTask, CircularStack, RangeFreq
from PowerReader import SweepPower


def main():
    freq = RangeFreq(2400, 2484, 0.1)
    task = PowerTask(freq, 100)
    stack = CircularStack([task])
    power_source = SweepPower
    detect = PowerRecorder(stack, power_source, "data/")
    detect.start()


def render():
    datas = []
    path = "data/"
    files = os.listdir(path)

    for file in files:
        with open(path + file, "rb") as f:
            datas.append(pickle.load(f))

    fig, axes = plt.subplots(1)
    camera = Camera(fig)

    power_data = datas[0].get_data()
    freq_list = datas[0].get_freq()

    power_data = np.rot90(power_data)
    null_kernel_size = 21

    filter_kernel_size = 41

    for i, data in enumerate(datas[0:1]):
        power_data = data.get_data()
        freq_list = data.get_freq()

        freq_list = freq_list[filter_kernel_size : -1 * filter_kernel_size]
        power_data = np.rot90(power_data)

        filer_signal = signal.medfilt2d(power_data, kernel_size=17)

        mean_signal = np.mean(filer_signal[:][null_kernel_size : -1 * null_kernel_size])

        exp_data = signal.medfilt(power_data[:][3:-3])
        exp_data -= mean_signal
        exp_data = np.exp(exp_data)

        for number in range(len(power_data)):
            axes[0].plot(power_data[number], color="green")
            plt.title = f"{i}:{number}"

            filer_data = signal.medfilt(
                power_data[number], kernel_size=filter_kernel_size
            )
            filer_data = filer_data[filter_kernel_size : -1 * filter_kernel_size]

            axes[0].plot(power_data[number], color="green")
            axes[1].plot(filer_data, color="red")
            axes[1].plot(np.ones(len(filer_data)) * mean_signal, color="blue")

            exp_data = filer_data - mean_signal

            exp_data = np.exp(exp_data)

            exp_data[exp_data > 100] = 100

            axes[2].plot(
                freq_list,
                exp_data,
            )

            camera.snap()

    animation = camera.animate()
    plt.show()
    # animation.save("celluloid_subplots.gif", writer="imagemagick")


def detect_matrix():
    datas = []
    path = "data/"
    files = os.listdir(path)

    for file in files:
        with open(path + file, "rb") as f:
            datas.append(pickle.load(f))

    fig, axes = plt.subplots(2)

    power_data = datas[0].get_data()
    freq_list = datas[0].get_freq()

    power_data = np.rot90(power_data)
    print(len(power_data))
    null_kernel_size = 21

    filter_kernel_size = 31
    # power_data = signal.medfilt2d(
    #     power_data[filter_kernel_size : -1 * filter_kernel_size]
    # )[:, 3:-3]
    print(len(power_data))
    freq_list = freq_list[filter_kernel_size : -1 * filter_kernel_size]

    filer_signal = signal.medfilt2d(power_data, kernel_size=null_kernel_size)[
        :, null_kernel_size : -1 * null_kernel_size
    ]

    mean_signal = np.mean(filer_signal)

    # power_data = signal.medfilt(power_data, kernel_size=filter_kernel_size)
    print(power_data)

    # exp_data = power_data[:, filter_kernel_size:-filter_kernel_size]

    null_data = power_data - mean_signal

    # exp_data = exp_data - 1

    one_line = 50
    for data in range(len(null_data)):
        line = null_data[data]
        line = signal.medfilt(line, kernel_size=filter_kernel_size)
        line = line[filter_kernel_size:-filter_kernel_size]

        line = np.exp(line)
        # print(line)
        line[line < one_line] = 0
        line[line > one_line] = 1
        axes[0].plot(line * (len(null_data) - data), "ro")

    # filter_data = signal.medfilt2d(power_data)
    filter_data = power_data
    for i, data in enumerate(power_data):
        filter_data[i] = signal.medfilt(data, kernel_size=filter_kernel_size)

    filter_data = filter_data[:, filter_kernel_size:-filter_kernel_size]
    filter_data = filter_data - mean_signal
    exp_data = np.power(4, filter_data)
    exp_data = np.power(exp_data, 0.5)

    exp_data -= 1
    exp_data[exp_data > 255] = 255
    axes[1].imshow(exp_data)

    plt.show()


if __name__ == "__main__":
    # main()
    # render()
    detect_matrix()

    # main()
