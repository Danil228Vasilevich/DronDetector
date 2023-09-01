import numpy
import libSweep
import time

from server.server import Server


server = Server()

server.send([obj1, obj2, obj3])

# send_data = []

# for data in datas:
#     json = f"freq = {data.freq}, power = {data. power}"
    
#     send_data.append(json)


# self._send(send_data)

# #from DataClasses.DataFreq import DataFreq

#object1 = DataFreq(2.43, -40.1)




class Detect:
    def __init__(self, ranges, ) -> None:
        self._ranges = ranges

        self._data = 

    def data_call_back(self, data):
        pass


if __name__ == "__main__":
    data = libSweep.ReadPower(call_back_func = test_call_back, len_answer_buf =  10, binSize=1)
    data.Start()
    time.sleep(5)
    power, freq = data.getData(10)
   