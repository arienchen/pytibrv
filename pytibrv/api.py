##
# pytibrv/api.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.0 20161209 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# ---------------------------------------------------
# 1. Use ctypes for dynamic binding
#
# 2. ctypes is just a wrapper to C,
#    all ctypes data type: c_int, c_wchar_p
#    actually, it present a piece of memory
#    for example:
#    x = c_int32(0)
#    y = c_int32(0)
#
#    -> x != y              because x,y are 2 pointer ,although the content is same
#    -> x.value == y.value
#
#    Must be very aware to use ctypes data type.
#
# 3. Python Call By Reference
#
#    In Python,
#    ALL parameters are Call By Reference of Object
#    BUT parameters are not all mutable(writable)
#
#    for example
#    def change(x):
#        x = "ABC"
#
#    y = "123"
#    change(y)
#    print(y)         -> it is still "123"
#
#    in change()
#    x = "ABC"        -> you assign x to a new string reference
#
#    after change(y) returned, Python doest not affect the reference of y
#    y is still point to "123"
#
#    In TIBRV
#    All API return tibrv_status and use pointer to return new object
#    ex:
#       tibrv_status tibrvMsg_Create(tibrvMsg * msg)
#
#    In Python,
#    Although it is not support 'Call By Reference',
#    but it support multiple objects return
#
#    def tibrvTransport_Create(...) :
#       tx = ctypes.c_uint32(0)
#       status = _rv.tibrvTransportCreate(ctypes.byref(tx), ...)
#       return status, tx.value
#
#    ...
#    status, ret = tibrvTransport_Create(...)
#
#
# 4. Python3 DOES NOT support c_char_p('text', 10)
#    In Python3,
#    c_char_p is a char[](byte[]), not a null-terminated string
#       you have to convert byte[] <> str
#
#       this work in Python3
#       x = c_char_p(b'TEXT')
#
#       but
#       x = c_char_p('TEXT') not work
#
#       y = c_char_p('TEXT'.encode()) work
#
#    c_wchar_p is wchar[] for Unicode
#       although it represent Python str
#       But decode char[] as wchar[] would cause error
#       for example
#       '12' -> char[] = [0x31, 0x32]
#       wchar would decode it as UTF16 0x3132 , and it is wrong
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrv_Open
#   tibrv_Close
#   tibrv_Version
#
#  *tibrv_SetCodePages
#  *tibrv_SetRVParameters
#  *tibrv_OpenEx
#  *tibrv_IsIPM
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161209 ARIEN V1.0
#   CREATED
#
##
from time import time as _time
import ctypes as _ctypes

# FIND AND LOAD C Libraries
# Unix/Linux/OSX    : LD_LIBRARY_PATH
# Windows           : Path
from ctypes.util import find_library as _find_library

from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    # linux
    _rv = _ctypes.cdll.LoadLibrary('libtibrv64.so')
    _func=_ctypes.CFUNCTYPE
elif _platform == "darwin":
    # MAC OS X
    _rv = _ctypes.cdll.LoadLibrary(_find_library('tibrv64'))
    _func=_ctypes.CFUNCTYPE
elif _platform == 'win32':
    # Windows
    _rv = _ctypes.windll.LoadLibrary(_find_library('tibrv'))
    _func=_ctypes.WINFUNCTYPE
else:
    raise SystemError(_platform + ' is not supported')

##-----------------------------------------------------------------------------
# TIBRV Data Types for Python
# 1. Python only support native data type for int(64), float(64), str
#    Using Python int to represent C int32,uint32, void *
#
# 2. Python does not support enum
#    redefine as int
#
# 3.
##-----------------------------------------------------------------------------
tibrv_status            = int
tibrvId                 = int
tibrvMsg                = int
tibrvEvent              = tibrvId
tibrvDispatchable       = tibrvId
tibrvQueue              = tibrvId
tibrvQueueGroup         = tibrvId
tibrvTransport          = tibrvId
tibrvDispatcher         = tibrvId
tibrvEventType          = int
tibrvQueueLimitPoliy    = int                   # enum
tibrvIOType             = int                   # enum


class TibrvMsgDateTime:
    def __init__(self):
        self._sec = 0
        self._nsec = 0

    def __str__(self):
        return '{:d}.{:09d}'.format(self._sec, self._nsec % 1000000000)

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        return self._sec == other._sec and self._nsec == other._nsec

    @property
    def sec(self):
        return self._sec

    @sec.setter
    def sec(self, seconds: int):
        self._sec = seconds

    @property
    def nsec(self):
        return self._nsec

    @nsec.setter
    def nsec(self, nano: int):
        self._nsec = nano % 1000000000

    @staticmethod
    def now():
        t = _time()
        dt = TibrvMsgDateTime()
        dt.sec = int(t)
        dt.nsec = int((t - dt.sec) * 1000000000)
        return dt


class TibrvMsgField:
    def __init__(self, name: str = None, id: int = 0):
        self._name = name
        self._size = 0
        self._count = 0
        self._data = None
        self._id = id
        self._type = 0

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, sz: str):
        self._name = sz

    @property
    def size(self) -> int:
        return self._size

    @property
    def count(self) -> int:
        return self._count

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> int:
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def int8(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._date

        raise TypeError('type is not integer')

    @int8.setter
    def int8(self, n: int):
        n = _ctypes.c_int8(n)
        self._type = TIBRVMSG_I8
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def uint8(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @uint8.setter
    def uint8(self, n: int):
        n = _ctypes.c_uint8(n)
        self._type = TIBRVMSG_U8
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def int16(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @int16.setter
    def int16(self, n: int):
        n = _ctypes.c_int16(n)
        self._type = TIBRVMSG_I16
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def uint16(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @uint16.setter
    def uint16(self, n: int):
        n = _ctypes.c_uint16(n)
        self._type = TIBRVMSG_U16
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def int32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @int32.setter
    def int32(self, n: int):
        n = _ctypes.c_int32(n)
        self._type = TIBRVMSG_I32
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def uint32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @uint32.setter
    def uint32(self, n: int):
        n = _ctypes.c_uint32(n)
        self._type = TIBRVMSG_U32
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def int64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @int64.setter
    def int64(self, n: int):
        n = _ctypes.c_int64(n)
        self._type = TIBRVMSG_I64
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def uint64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        raise TypeError('type is not integer')

    @uint64.setter
    def uint64(self, n: int):
        n = _ctypes.c_uint64(n)
        self._type = TIBRVMSG_U64
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def f32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        if TIBRVMSG_F32 <= self._type <= TIBRVMSG_F64:
            return self.data

        raise TypeError('type is not float')

    @f32.setter
    def f32(self, n: float):
        n = _ctypes.c_float(n)
        self._type = TIBRVMSG_F32
        self._sizeof(n)
        self._data = n.value

    @property
    def f64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        if TIBRVMSG_F32 <= self._type <= TIBRVMSG_F64:
            return self._data

        raise TypeError('type is not float')

    @f64.setter
    def f64(self, n: float):
        n = _ctypes.c_double(n)
        self._type = TIBRVMSG_F64
        self._size = _ctypes.sizeof(n)
        self._data = n.value

    @property
    def str(self):
        if self._type == TIBRVMSG_STRING:
            return self._data

        # although int, float, msg could convert to str
        # suggest for explict data type
        # raise exception of non-str

        raise TypeError('can not convert to string')

    @str.setter
    def str(self, s: str):
        n = str(s)
        self._type = TIBRVMSG_STRING
        self._size = len(n)
        self._data = n


##-----------------------------------------------------------------------------
# GLOBAL CONSTANTS
##-----------------------------------------------------------------------------
TIBRV_TRUE                  = 1
TIBRV_FALSE                 = 0
TIBRV_TIMER_EVENT           = 1
TIBRV_IO_EVENT              = 2
TIBRV_LISTEN_EVENT          = 3
TIBRV_DEFAULT_QUEUE         = 1
TIBRV_PROCESS_TRANSPORT     = 10
TIBRVQUEUE_DISCARD_NONE     = 0
TIBRVQUEUE_DISCARD_NEW      = 1
TIBRVQUEUE_DISCARD_FIRST    = 2
TIBRVQUEUE_DISCARD_LAST     = 3
TIBRV_WAIT_FOREVER          = -1.0
TIBRV_NO_WAIT               = 0.0

TIBRVMSG_FIELDNAME_MAX      = 127

TIBRVMSG_MSG                = 1
TIBRVMSG_DATETIME           = 3
TIBRVMSG_OPAQUE             = 7
TIBRVMSG_STRING             = 8
TIBRVMSG_BOOL               = 9
TIBRVMSG_I8                 = 14
TIBRVMSG_U8                 = 15
TIBRVMSG_I16                = 16
TIBRVMSG_U16                = 17
TIBRVMSG_I32                = 18
TIBRVMSG_U32                = 19
TIBRVMSG_I64                = 20
TIBRVMSG_U64                = 21
TIBRVMSG_F32                = 24
TIBRVMSG_F64                = 25
TIBRVMSG_IPPORT16           = 26
TIBRVMSG_IPADDR32           = 27
TIBRVMSG_ENCRYPTED          = 32
TIBRVMSG_NONE               = 22
TIBRVMSG_I8ARRAY            = 34
TIBRVMSG_U8ARRAY            = 35
TIBRVMSG_I16ARRAY           = 36
TIBRVMSG_U16ARRAY           = 37
TIBRVMSG_I32ARRAY           = 38
TIBRVMSG_U32ARRAY           = 39
TIBRVMSG_I64ARRAY           = 40
TIBRVMSG_U64ARRAY           = 41
TIBRVMSG_F32ARRAY           = 44
TIBRVMSG_F64ARRAY           = 45
TIBRVMSG_XML                = 47
TIBRVMSG_STRINGARRAY        = 48
TIBRVMSG_MSGARRAY           = 49
TIBRVMSG_USER_FIRST         = 128
TIBRVMSG_USER_LAST          = 255
TIBRVMSG_NO_TAG             = 0

TIBRV_SUBJECT_MAX           = 255

TIBRVMSG_DATETIME_STRING_SIZE = 32

##-----------------------------------------------------------------------------
# tibrv/types.h
# declare _ctypes for internal use
##-----------------------------------------------------------------------------
c_tibrv_i8                  = _ctypes.c_int8
c_tibrv_u8                  = _ctypes.c_uint8
c_tibrv_i16                 = _ctypes.c_int16
c_tibrv_u16                 = _ctypes.c_uint16
c_tibrv_i32                 = _ctypes.c_int32
c_tibrv_u32                 = _ctypes.c_uint32
c_tibrv_i64                 = _ctypes.c_int64
c_tibrv_u64                 = _ctypes.c_uint64
c_tibrv_f32                 = _ctypes.c_float
c_tibrv_f64                 = _ctypes.c_double
c_tibrv_bool                = _ctypes.c_int
c_tibrv_ipport16            = _ctypes.c_uint16
c_tibrv_ipaddr32            = _ctypes.c_uint32
c_tibrv_str                 = _ctypes.c_char_p

c_tibrv_status              = _ctypes.c_int32
c_tibrvId                   = _ctypes.c_uint32
c_tibrvMsg                  = _ctypes.c_void_p
c_tibrvEvent                = c_tibrvId
c_tibrvDispatchable         = c_tibrvId
c_tibrvQueue                = c_tibrvDispatchable
c_tibrvQueueGroup           = c_tibrvDispatchable
c_tibrvTransport            = c_tibrvId
c_tibrvDispatcher           = c_tibrvId
c_tibrvEventType            = _ctypes.c_uint32
c_tibrvQueueLimitPolicy     = _ctypes.c_int32
c_tibrvIOType               = _ctypes.c_int32

# Array
c_tibrv_bool_p              = _ctypes.POINTER(c_tibrv_bool)
c_tibrv_i8_p                = _ctypes.POINTER(c_tibrv_i8)
c_tibrv_u8_p                = _ctypes.POINTER(c_tibrv_u8)
c_tibrv_i16_p               = _ctypes.POINTER(c_tibrv_i16)
c_tibrv_u16_p               = _ctypes.POINTER(c_tibrv_u16)
c_tibrv_i32_p               = _ctypes.POINTER(c_tibrv_i32)
c_tibrv_u32_p               = _ctypes.POINTER(c_tibrv_u32)
c_tibrv_i64_p               = _ctypes.POINTER(c_tibrv_i64)
c_tibrv_u64_p               = _ctypes.POINTER(c_tibrv_u64)
c_tibrv_f32_p               = _ctypes.POINTER(c_tibrv_f32)
c_tibrv_f64_p               = _ctypes.POINTER(c_tibrv_f64)
c_tibrv_str_p               = _ctypes.POINTER(c_tibrv_str)
c_tibrvMsg_p                = _ctypes.POINTER(c_tibrvMsg)

##
# Callback
# typedef void (*tibrvEventCallback) (
#                 tibrvEvent          event,
#                 tibrvMsg            message,
#                 void*               closure
#                );
#
c_tibrvEventCallback = _func(_ctypes.c_void_p, c_tibrvEvent, c_tibrvMsg, _ctypes.c_int64)

# typedef void (*tibrvEventVectorCallback) (
#                  tibrvMsg            messages[],
#                  tibrv_u32           numMessages
#                );
#
c_tibrvEventVectorCallback = _func(None, _ctypes.POINTER(c_tibrvMsg), c_tibrv_u32)


# typedef void (*tibrvEventOnComplete) (
#                  tibrvEvent          event,
#                  void*               closure
#                );
#
c_tibrvEventOnComplete = _func(None, c_tibrvEvent, _ctypes.c_void_p)

# typedef void (*tibrvQueueOnComplete) (
#                  tibrvQueue          queue,
#                  void*               closure
#                 );
#
c_tibrvQueueOnComplete = _func(None, c_tibrvQueue, _ctypes.c_void_p)

c_tibrvQueueHook = _func(None, c_tibrvQueue, _ctypes.c_void_p)


# Helper Functions
def _cstr(sz: str, codepage = None) -> str:
    if sz is None:
        return None

    if codepage is None:
        return c_tibrv_str(str(sz).encode())
    else:
        return c_tibrv_str(str(sz).encode(codepage))

def _ret(param: list, val: object = None, size: int = 1) -> None:
    while len(param) < size:
        param.append(None)

    if val is None:
        param[0] = None
        return

    # assign val -> param[0]
    if val is not list:
        param[0] = val
        return

    # assign val[] -> param[]
    for i in range(len(param)):
        if i < len(val):
            param[i] = val[i]
        else:
            param[i] = None

    return


def _pystr(sz: _ctypes.c_char_p, codepage = None) -> str:
    if sz is None:
        return None

    if type(sz) is bytes:
        ss = sz
    elif sz.value is None:
        return None
    else:
        ss = sz.value

    if codepage is None:
        return ss.decode()
    else:
        return ss.decode(codepage)



##-----------------------------------------------------------------------------
## Tibrv
##-----------------------------------------------------------------------------
##
# tibrv/tibrv.h
# tibrv_status tibrv_Open(void)
#
_rv.tibrv_Open.argtypes = None
_rv.tibrv_Open.restype = c_tibrv_status

def tibrv_Open() -> tibrv_status:
    status = _rv.tibrv_Open()
    return status

##
# tibrv/tibrv.h
# tibrv_status tibrv_Close(void)
#
_rv.tibrv_Close.argtypes = None
_rv.tibrv_Close.restype = c_tibrv_status

def tibrv_Close() -> tibrv_status:
    status = _rv.tibrv_Close()
    return status

##
# tibrv/tibrv.h
# const char * tibrv_Version(void)
#
_rv.tibrv_Version.argtypes = []
_rv.tibrv_Version.restype = _ctypes.c_char_p

def tibrv_Version() -> str :
    sz = _rv.tibrv_Version()
    return sz.decode()

class Tibrv:

    _exception = False
    _codepage = None

    @staticmethod
    def open() -> tibrv_status :
        status = tibrv_Open()
        return status

    @staticmethod
    def close() -> tibrv_status :
        status = tibrv_Close()
        return status

    @staticmethod
    def version():
        status = tibrv_Version()
        return status

# Define abstract class for scalar data type
class tibrv_type(object):
    def __new__(cls, *args, **kwargs):
        raise TypeError(cls.__name__ + ' is abstract class ')

class tibrv_i8(tibrv_type):
    pass

class tibrv_u8(tibrv_type):
    pass

class tibrv_i16(tibrv_type):
    pass

class tibrv_u16(tibrv_type):
    pass

class tibrv_i32(tibrv_type):
    pass

class tibrv_u32(tibrv_type):
    pass

class tibrv_i64(tibrv_type):
    pass

class tibrv_u64(tibrv_type):
    pass

class tibrv_f32(tibrv_type):
    pass

class tibrv_f64(tibrv_type):
    pass

class tibrv_str(tibrv_type):
    pass

