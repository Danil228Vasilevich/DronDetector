import numpy as np
from libSweep import ReadPower
import sys
from math import exp


#sys.path.append("../DataClasses/")
from DataClasses.DataFreq import DataFreq


# server = Server()

# server.send([obj1, obj2, obj3])

# send_data = []

# for data in datas:
#     json = f"freq = {data.freq}, power = {data. power}"

#     send_data.append(json)


# self._send(send_data)

# #from DataClasses.DataFreq import DataFreq

# object1 = DataFreq(2.43, -40.1)


class Detect:
    def __init__(self, ranges) -> None:
        self._ranges = ranges
        self._len_answer_buf = 100
        self._nume_range = 0
        self._binSize = 5

        self._sdr_data = ReadPower(
            call_back_func=self.data_call_back,
            len_answer_buf=self._len_answer_buf,
            startFreq=self._ranges[self._nume_range][0],
            stopFreq=self._ranges[self._nume_range][1],
            binSize=self._binSize,
        )

        self._sdr_data.Start()

        self._qeu = list()

    def data_call_back(self, data):
        self._qeu.append(data)
        self._nume_range += 1
        if self._nume_range >= len(self._ranges):
            self._nume_range = 0

        # self._sdr_data.new_freq(startFreq=self._ranges[self._nume_range][0], stopFreq=self._ranges[self._nume_range][1], binSize=1)
        self._sdr_data.Stop()
        del self._sdr_data
        self._sdr_data = ReadPower(
            call_back_func=self.data_call_back,
            len_answer_buf=self._len_answer_buf,
            startFreq=self._ranges[self._nume_range][0],
            stopFreq=self._ranges[self._nume_range][1],
            binSize=self._binSize,
        )
        self._sdr_data.Start()

    def procces(self):
        if len(self._qeu) < 1:
            return

        test = self._qeu[0]
        self._qeu = self._qeu[1:]

        self._analysis(test)

    def _analysis(self, data):
        powers = np.array(data[0])
        powers = np.transpose(powers)
        freq = data[1]
        mask_power = np.zeros((len(powers), len(powers[0])))

        list_lower_mean = np.mean(powers, axis=1)

        for i in range(len(powers)):
            line = powers[i].copy()

            # list_lower_mean[i] = np.mean(line[line < list_lower_mean[i]])
            mask_power[i] = np.where(powers[i] > list_lower_mean[i], 1, mask_power[i])

        mask_power = np.mean(mask_power, axis=0)

        mean_mask = np.mean(mask_power) * 10

        print("---" * 80)
        for i in range(len(mask_power)):
            print(
                str(freq[i])
                + (int((exp((mask_power[i] - np.mean(mask_power)) * 20))) * "#")
            )


if __name__ == "__main__":
    detect = Detect([(2401, 2483)])
    while True:
        detect.procces()
