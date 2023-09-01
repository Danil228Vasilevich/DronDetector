import numpy as np
import threading
import subprocess
import sys
import struct
import time

class ReadPower:
    def __init__(self, startFreq=2401, stopFreq=2483, binSize=1,
            interval=0.0, gain=40, ppm=0, crop=0, singleShot=False,
            deviceIndex=0, sampleRate=20000000) -> None:
        self._startFreq = startFreq
        self._stopFreq = stopFreq
        self._binSize = binSize
        self._interval = interval
        self._ppm = ppm
        self._crop = crop
        self._singleShot = singleShot
        self._deviceIndex = deviceIndex
        self._sampleRate = sampleRate

        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        self._lnaGain = 8 * (gain // 18)
        self._vgaGain = 2 * ((gain - self._lnaGain) // 2)

        self._sizeHistoryBufer = 100

        self._numChanel = int((self._stopFreq - self._startFreq) / self._binSize) + 1

        self._historyBufer =np.full((self._numChanel , self._sizeHistoryBufer ), None, dtype="float32")
        print(len(self._historyBufer))
        self._listFreq = np.arange(self._startFreq + self._binSize/2, self._stopFreq - binSize/2, binSize)
        self._TreadRead = threading.Thread(target=self._readData)
        self._alive = False
        self._process = None

    def Start(self):
        cmdline = [
                        "hackrf_sweep",
                        "-f", "{}:{}".format(int(self._startFreq),
                                int(self._stopFreq)),
                        "-B",
                        "-w", "{}".format(int(self._binSize*1e6)),
                        "-l", "{}".format(int(self._lnaGain)),
                        "-g", "{}".format(int(self._vgaGain)),
                        
            ]
        
        
        self._process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=False)
        
        self._TreadRead.start()
        
        
    def SignalShot(self):
        self.Stop()
        cmdline = [
                        "hackrf_sweep",
                        "-f", "{}:{}".format(int(self._startFreq),
                                int(self._stopFreq)),
                        "-1",
                        "-w", "{}".format(int(self._binSize*1e6)),
                        "-l", "{}".format(int(self._lnaGain)),
                        "-g", "{}".format(int(self._vgaGain)),
            ]
        data = subprocess.check_output(cmdline, universal_newlines=False,  stderr=subprocess.DEVNULL)

        return data

    def Stop(self):
        self._alive = False
        while self._TreadRead.is_alive():
            #print(self._TreadRead.is_alive())
            continue

        if self._process:
            self._process.terminate()

    def getData(self, lenData):
        
        return self._historyBufer[:, :lenData if lenData < self._sizeHistoryBufer else (self._sizeHistoryBufer - 1)], self._listFreq
    

    def _readData(self):
        
        self._alive = True
        while self._alive:
            try:
                buf = self._process.stdout.read(4)
            except AttributeError as e:
                print(e, file=sys.stderr)
                continue

            if buf:
                (record_length,) = struct.unpack('I', buf)
                try:
                    buf = self._process.stdout.read(record_length)
                except AttributeError as e:
                    print(e, file=sys.stderr)
                    continue
                if buf:
                    freq = struct.unpack('QQ', buf[:16])
                    pointData =  (int(freq[0]*10e-7) - self._startFreq) // self._binSize
                    data = np.frombuffer(buf[16:], dtype='<f4')
                    for i in range(len(data)):
                        if(pointData + i) < self._numChanel:
                            line = self._historyBufer[pointData + i]
                            self._historyBufer[pointData + i] = np.hstack((data[i], line[:-1]))
                    #print(self._historyBufer)
                else:
                    break
            else:
                break

        


if __name__ == "__main__":
    data = ReadPower(binSize=1)
    data.Start()
    time.sleep(5)
    
    power, freq = data.getData(10)
    print(power)
    
    print(123)