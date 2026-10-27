from .Append import *
from .Read import *
from .Write import *


def ClearFile(path:str): Write.OwerWrite(path, "")