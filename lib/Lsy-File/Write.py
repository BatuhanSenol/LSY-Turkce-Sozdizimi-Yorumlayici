import pyfastfile as pf


def OwerWrite(path:str, data:str): pf.overwrite(path, data)
def Touch(path:str): pf.touch(path, existserror=False)
