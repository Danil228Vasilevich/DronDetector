import numpy
import libSweep
import time

def test_call_back(power, freq):
    print(power, freq)


if __name__ == "__main__":
    data = libSweep(test_call_back,binSize=1)
    data.Start()
    time.sleep(5)
    power, freq = data.getData(10)
    print(power)
    
    print(123)