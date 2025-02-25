
import pkgutil
import io
import os
import sys

def loadFile(fname:str) -> io.BytesIO:
    return io.BytesIO(pkgutil.get_data('pylak', os.path.join('resources', fname)))

def getFilepathInResources(fname:str) -> str:
    d = os.path.dirname(sys.modules['pylak'].__file__) 
    return os.path.join(d, 'resources', fname)
