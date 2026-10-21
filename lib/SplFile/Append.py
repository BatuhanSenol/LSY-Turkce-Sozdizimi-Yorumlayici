import pyfastfile as pf


def Append(path:str, data:str): pf.append(path, data)
def AppendWithoutNewline(path:str, data:str): pf.append(path, data, False)