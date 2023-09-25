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
    freq = RangeFreq(2401, 2484, 0.5)
    task = PowerTask(freq, 100)
    stack = CircularStack([task])
    power_source = SweepPower
    detect = PowerRecorder(stack, power_source, "data/")
    detect.start()


def render():
    data = []
    path = "data/"
    files = os.listdir(path)

    for file in files:
        with open(path + file, "rb") as f:
            data.append(pickle.load(f))

    fig, axes = plt.subplots(3)
    camera = Camera(fig)

    power_data = data[0].get_data()

    power_data = np.rot90(power_data)
    mean_signal = signal.medfilt2d(power_data, kernel_size=11)

    for number in range(len(power_data)):
        axes[0].plot(power_data[number], color="green")
        axes[1].plot(signal.medfilt(power_data[number], kernel_size=15), color="blue")
        axes[0].plot(mean_signal[number], color="red")
        camera.snap()

    animation = camera.animate()
    plt.show()
    # animation.save("celluloid_subplots.gif", writer="imagemagick")


if __name__ == "__main__":
    render()

    # main()
