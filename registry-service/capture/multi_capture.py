from typing import *

import capture


def multy_capture(indexList: Optional[list] = None):
    if indexList is None:
        for i in range(3):
            print(f"当前使用设备: {i}")
            capture.capture(i)
    else:
        for index in indexList:
            print(index)
            capture.capture(index)


deviceList = {"front": 2, "up": 0, "left": 1}

if __name__ == "__main__":
    index = ["front", "up", "left"]
    indexList = [deviceList[i] for i in index]
    multy_capture(indexList)
