from numpy import ndarray
import struct
import numpy as np

class PowerBuffer:
    def __init__(self, list_freq:ndarray) -> None:
        self._buffer = []
        self._list_freq = list_freq
        self._bin_size = list_freq[1] - list_freq[0]

    def __len__(self):
        return len(self._buffer)
    
    def get_freq(self) -> ndarray:
        return self._list_freq

    def append(self, data:bytes) -> None:
        self.buffering(data)

    def buffering(self, data:bytes) -> None:
        self._buffer.append(data)

    def get_data(self) -> ndarray:
        data = self._unpack_data()
        return data
    
    def zeroing_data(self) -> None:
        self._buffer = []
    
    def _unpack_data(self) -> ndarray:
        data = np.frombuffer(self._buffer[0][16:], dtype='<f4')
        quantity_freq = len(data)
        
        size_y =  int((len(self._buffer) * quantity_freq) / len(self._list_freq))
        size_x = len(self._list_freq)
        size_buf = (size_x, size_y)
        print(size_buf)
        
        unpack_data =np.full(size_buf, None, dtype="float32")
        for buf in self._buffer:
            freq = struct.unpack('QQ', buf[:16])
            
            point_data =  int((int(freq[0]*10e-7) - self._list_freq[0]) // self._bin_size)
            
            data = np.frombuffer(buf[16:], dtype='<f4')
            
            for i in range(len(data)):
                if(point_data + i) >= len(self._list_freq):
                    continue
                
                line = unpack_data[point_data + i]
                unpack_data[point_data + i] = np.hstack((data[i], line[:-1]))
                
        
        return unpack_data
