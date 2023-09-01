import numpy
import libSweep
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

        self.sdr_data = libSweep(self.data_call_back, 10)

        self._qeu = numpy.array()



    def data_call_back(self, data):
        pass


if __name__ == "__main__":
    detect = Detect([0,1])
   