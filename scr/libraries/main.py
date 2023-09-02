import numpy as np
from libSweep import ReadPower
import time
import sys


sys.path.append("../DataClasses/")
from DataFreq import DataFreq


# server = Server()

# server.send([obj1, obj2, obj3])

# send_data = []

# for data in datas:
#     json = f"freq = {data.freq}, power = {data. power}"
    
#     send_data.append(json)


# self._send(send_data)

# #from DataClasses.DataFreq import DataFreq

#object1 = DataFreq(2.43, -40.1)




class Detect:
    def __init__(self, ranges) -> None:
        self._ranges = ranges

        self._nume_range =  0 

        self._sdr_data = ReadPower(call_back_func=self.data_call_back,
                                   len_answer_buf=10,
                                   startFreq=self._ranges[self._nume_range][0],
                                   stopFreq=self._ranges[self._nume_range][1])
        
        self._sdr_data.Start()

        self._qeu = list()


    def data_call_back(self, data):
        self._qeu.append(data)
        self._nume_range += 1
        if self._nume_range >= len(self._ranges): self._nume_range = 0

        self._sdr_data.Stop()
        self._sdr_data = ReadPower(call_back_func=self.data_call_back,
                                   len_answer_buf=10,
                                   startFreq=self._ranges[self._nume_range][0],
                                   stopFreq=self._ranges[self._nume_range][1])
        self._sdr_data.Start()

    def procces(self):
        
        if len(self._qeu) < 1: return
        
        test = self._qeu[0]
        self._qeu = self._qeu[1:]
        
        self._analysis(test)
            

    def _analysis(self, data):
        powers = np.array(data[0])
        freq = data[1]

        print(powers, freq)



if __name__ == "__main__":
    detect = Detect([(2401,2483), (3300, 3500)])
    while True:
        detect.procces()