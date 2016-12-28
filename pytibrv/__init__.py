##
# pytibrv use Python standard library : ctypes as the wrapper to TIBRV C API
# It is not a Python Extension, not required to re-compile C Source(Python Extension) 
# for deployment. 
# 
# In practice,
# TIBRV would be installed at /opt/tibco/tibrv for multiple version
# 
# /opt/tibco/tibrv/
#                  8.4.1/
#                  8.4.2/
#                  8.4.5/
# 
# The environment variable LD_LIBRARY_PATH, would be set to indicate specific TIBRV version.
# ex:
#   TIBRV_HOME=/opt/tibco/tibrv/8.4.5
#   LD_LIBRARY_PATH=${TIBRV_HOME}/lib:$LD_LIBRARY_PATH
# 
# For Windows, it would like as 
# 
# d:\tibco\tibrv\
#                8.4.1\
#                8.4.2\
#                8.4.5\
# 
# The environment variable Path, would be set to indicate specific TIBRV version.
# ex:
#   set TIBRV_HOME=d:\tibco\tibrv\8.4.5
#   set Path=%TIBRV_HOME%\bin;%Path%
# 
# ctypes LoadLibrary behave different for OS
#
# In Darwin(OSX)
#   find_library() would search in LD_LIBRARY_PATH and return the full path
#   ex: 
#   lib = find_library('tibrv64') -> '/opt/tibco/tibrv/8.4.5/lib/libtibrv64.dylib'
#   _rv = ctypes.cdll.LoadLibrary(lib) 
# 
# In Linux
#   find_library() use 'ldconfig -p' to find the lib name
#   ex: 
#   find_library('tibrv64')       -> None 
#   find_library('libtibrv64.so') -> None 
#
#   ldconfig use for global linking library, not suitable for multiple version of TIBRV
#   just call LoadLibrary(lib_name) 
#   ex: 
#   _rv = ctypes.cdll.LoadLibrary('libtibrv64.so') 
# 
# In Windows
#   find_library() would search DLL in Path and return full path
#   lib = find_library('tibrv')   -> 'd:\\tibco\\tibrv\\8.4.5\\bin\\tibrv.dll' 
#   _rv = ctypes.windll.LoadLibrary(lib)
# 
#
from .version import version as __version__
__all__ = ['api', 'status', 'tport', 'queue', 'events', 'disp', 'msg']


import ctypes as __ctypes
from ctypes.util import find_library as __find_library
import sys as __sys
from platform import architecture as __arch

#if __sys.version_info[0] < 3:
#    raise SystemError('Sorry, PYTIBRV support for Python 3.x only')

# module variables
_func = None                # ctype func cast, OS dependent

# detech OS and ARCH
__lib_bit = lambda: '64' if __arch()[0] == '64bit' else ''

if __sys.platform[:5] == "linux" or __sys.platform[:3] == "aix":
    # Unix/Linux
    _func = __ctypes.CFUNCTYPE
    __lib_name = lambda name: 'lib' + name + __lib_bit() + '.so'

elif __sys.platform == "darwin":
    # MAC OS X
    _func = __ctypes.CFUNCTYPE
    __lib_name = lambda name: name + __lib_bit()

elif __sys.platform == 'win32':
    # Windows
    _func = __ctypes.WINFUNCTYPE
    __lib_name = lambda name: name

else:
    raise SystemError(__sys.platform + ' is not supported')


def _load(name: str):
    lib = None

    if __sys.platform[:5] == "linux" or __sys.platform[:3] == "aix":
        # Unix/Linux/AIX
        lib = __ctypes.cdll.LoadLibrary(__lib_name(name))

    elif __sys.platform == "darwin":
        # MAC OS X
        lib = __ctypes.cdll.LoadLibrary(__find_library(__lib_name(name)))

    elif __sys.platform == 'win32':
        # Windows
        lib = __ctypes.windll.LoadLibrary(__find_library(__lib_name(name)))

    else:
        raise SystemError(__sys.platform + ' is not supported')

    return lib

