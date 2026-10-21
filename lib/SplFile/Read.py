import pyfastfile as pf


def ReadFile(path:str): return pf.read(path)
def ReadBytes(path:str): return pf.readbytes(path)

