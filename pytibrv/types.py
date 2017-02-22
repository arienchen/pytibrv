##
# pytibrv/types.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.1 20170220 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
# 1. declare CONSTANTS and Data Type as tibrv/types.h
#
# 2. Python only support native data type for int(64), float(64), str
#    Using Python int to represent C int32,uint32, void *
#
# 3. Python does not support enum
#    redefine as Python int
#
# 4. naming conversion exactly as TIBRV types.h
#
# 5. class tibrvMsgDateTime, tibrvMsgField
#    represent same C struct in tibrv/types.h
#
# 6. tibrvMsgField is not suggested
#    tibrvMsg_GetXXX are recommended
#    TIBRV will do format conversion if necessary
#    for example:
#      field data type is int16,
#      when you tibrvMsg_GetString(), TIBRV will convert int to string for you.
#
#    in practice,
#    you have to chceck tibrvMsgField.type before access tibrvMsgField.data
#    and do conversion as your own.
#
#    I create some property method(getter/setter) for tibrvMsgField
#    ex: tibrvMsgField.int8, str, msg
#
#    when data format conversion not supported or failed
#
#    getter:
#      it will return None
#
#    setter:
#      (1) scalar: int, float
#          it will assign 0 as default
#          fld.int16 = '1234'  -> fld.data = int(1234)
#          fld.int16 = 'ABC'   -> fld.data = 0
#
#      (2) string: all object could be convert to str, never failed
#
#      (3) tibrvMsg:
#          tibrvMsg is C void * (a POINTER) == integer
#          if it is integer, there is no error.
#          if it can't convert to integer, is would be assign to None(= 0)
#
#
# CHANGED LOGS
##-----------------------------------------------------------------------------
# 20170220 V1.1 ARIEN arien.chen@gmail.com
#   REMOVE TIBRV C Header
#
# 20161224 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
##
import ctypes as _ctypes
import time as _time
from typing import NewType, Callable, List, Any

##-----------------------------------------------------------------------------
# TIBRV Data Types for Python
##-----------------------------------------------------------------------------
tibrv_status            = NewType('tibrv_status', int)              # int
tibrvId                 = NewType('tibrvId', int)                   # int
tibrvMsg                = NewType('tibrvMsg', int)                  # c_void_p
tibrvEvent              = NewType('tibrvEvent', int)                # tibrvId
tibrvDispatchable       = NewType('tibrvDispatchable', int)         # tibrvId
tibrvQueue              = NewType('tibrvQueue', int)                # tibrvId
tibrvQueueGroup         = NewType('tibrvQueueGroup', int)           # tibrvId
tibrvTransport          = NewType('tibrvTransport', int)            # tibrvId
tibrvDispatcher         = NewType('tibrvDispatcher', int)           # tibrvId
tibrvEventType          = NewType('tibrvEventType', int)            # enum(int)
tibrvQueueLimitPolicy   = NewType('tibrvQueueLimitPolicy', int)     # enum(int)
tibrvIOType             = NewType('tibrvIOType', int)               # enum(int)


##-----------------------------------------------------------------------------
# GLOBAL CONSTANTS
##-----------------------------------------------------------------------------
TIBRV_TRUE                  = 1
TIBRV_FALSE                 = 0
TIBRV_TIMER_EVENT           = tibrvEventType(1)
TIBRV_IO_EVENT              = tibrvEventType(2)
TIBRV_LISTEN_EVENT          = tibrvEventType(3)
TIBRV_DEFAULT_QUEUE         = tibrvQueue(1)
TIBRV_PROCESS_TRANSPORT     = 10
TIBRVQUEUE_DISCARD_NONE     = tibrvQueueLimitPolicy(0)
TIBRVQUEUE_DISCARD_NEW      = tibrvQueueLimitPolicy(1)
TIBRVQUEUE_DISCARD_FIRST    = tibrvQueueLimitPolicy(2)
TIBRVQUEUE_DISCARD_LAST     = tibrvQueueLimitPolicy(3)
TIBRV_WAIT_FOREVER          = -1.0
TIBRV_NO_WAIT               = 0.0

TIBRVMSG_FIELDNAME_MAX      = 127

TIBRV_INVALID_ID            = 0

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
# CALLBACK
##-----------------------------------------------------------------------------
tibrvEventCallback          = Callable[[tibrvEvent, tibrvMsg, object], None]
tibrvEventVectorCallback    = Callable[[List[tibrvMsg], int], None]
tibrvEventOnComplete        = Callable[[tibrvEvent, object], None]
tibrvQueueOnComplete        = Callable[[tibrvQueue, object], None]
tibrvQueueHook              = Callable[[tibrvQueue, object], None]

class tibrvMsgDateTime:
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
        t = _time.time()
        dt = tibrvMsgDateTime()
        dt.sec = int(t)
        dt.nsec = int((t - dt.sec) * 1000000000)
        return dt


class tibrvMsgField:
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
            return self._data

        try:
            val = _ctypes.c_int8(self._data)
            return val.value
        except:
            return None

    @int8.setter
    def int8(self, n: int):
        self._type = TIBRVMSG_I8
        self._size = 1
        self._data = 0

        try:
            n = _ctypes.c_int8(n)
            self._data = n.value
        except:
            pass

    @property
    def uint8(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_uint8(self._data)
            return val.value
        except:
            return None

    @uint8.setter
    def uint8(self, n: int):
        self._type = TIBRVMSG_U8
        self._size = 1
        self._data = 0

        try:
            n = _ctypes.c_uint8(n)
            self._data = n.value
        except:
            pass

    @property
    def int16(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_int16(self._data)
            return val.value
        except:
            return None

    @int16.setter
    def int16(self, n: int):
        self._type = TIBRVMSG_I16
        self._size = 2
        self._data = 0

        try:
            n = _ctypes.c_int16(n)
            self._data = n.value
        except:
            pass

    @property
    def uint16(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_uint16(self._data)
            return val.value
        except:
            return None


    @uint16.setter
    def uint16(self, n: int):
        self._type = TIBRVMSG_U16
        self._size = 2
        self._data = 0

        try:
            n = _ctypes.c_uint16(n)
            self._data = n.value
        except:
            pass

    @property
    def int32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_int32(self._data)
            return val.value
        except:
            return None

    @int32.setter
    def int32(self, n: int):
        self._type = TIBRVMSG_I32
        self._size = 4
        self._data = 0

        try:
            n = _ctypes.c_int32(n)
            self._data = n.value
        except:
            pass

    @property
    def uint32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_uint32(self._data)
            return val.value
        except:
            return None

    @uint32.setter
    def uint32(self, n: int):
        self._type = TIBRVMSG_U32
        self._size = 4
        self._data = 0

        try:
            n = _ctypes.c_uint32(n)
            self._data = n.value
        except:
            pass

    @property
    def int64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_int64(self._data)
            return val.value
        except:
            return None

    @int64.setter
    def int64(self, n: int):
        self._type = TIBRVMSG_I64
        self._size = 8
        self._data = 0

        try:
            n = _ctypes.c_int64(n)
            self._data = n.value
        except:
            pass

    @property
    def uint64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        try:
            val = _ctypes.c_uint64(self._data)
            return val.value
        except:
            return None

    @uint64.setter
    def uint64(self, n: int):
        self._type = TIBRVMSG_U64
        self._size = 1
        self._data = 0

        try:
            n = _ctypes.c_uint64(n)
            self._data = n.value
        except:
            pass

    @property
    def f32(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        if TIBRVMSG_F32 <= self._type <= TIBRVMSG_F64:
            return self.data

        try:
            val = _ctypes.c_f32(self._data)
            return val.value
        except:
            return None

    @f32.setter
    def f32(self, n: float):
        self._type = TIBRVMSG_F32
        self._size = 4
        self._data = 0

        try:
            n = _ctypes.c_f32(n)
            self._data = n.value
        except:
            pass

    @property
    def f64(self):
        if TIBRVMSG_I8 <= self._type <= TIBRVMSG_U64:
            return self._data

        if TIBRVMSG_F32 <= self._type <= TIBRVMSG_F64:
            return self._data

        try:
            val = _ctypes.c_f64(self._data)
            return val.value
        except:
            return None


    @f64.setter
    def f64(self, n: float):
        self._type = TIBRVMSG_F64
        self._size = 8
        self._data = 0

        try:
            n = _ctypes.c_f64(n)
            self._data = n.value
        except:
            pass

    @property
    def str(self):
        if self._type == TIBRVMSG_STRING:
            return self._data

        return str(self._data)

    @str.setter
    def str(self, s: str):
        n = str(s)
        self._type = TIBRVMSG_STRING
        self._size = len(n)
        self._data = n

    @property
    def msg(self):
        if self._type == TIBRVMSG_MSG:
            return self._data

        return None

    @msg.setter
    def msg(self, m: tibrvMsg):
        self._type = TIBRVMSG_MSG
        self._size = 0
        self._data = None

        try:
            n = _ctypes.c_void_p(m)
            self._data = n.value
        except:
            pass

