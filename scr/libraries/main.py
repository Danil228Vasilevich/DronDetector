import numpy
import libSweep
import time

#from DataClasses.DataFreq import DataFreq

#object1 = DataFreq(2.43, -40.1)



def test_call_back(data):
    print(data)


if __name__ == "__main__":
    data = libSweep.ReadPower(call_back_func = test_call_back, len_answer_buf =  10, binSize=1)
    data.Start()
    time.sleep(5)
    power, freq = data.getData(10)
   