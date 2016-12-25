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
# 2. ctypes data type 
#    ctypes is just a wrapper to C,
#    it support data type: c_int, c_float, c_char_p
#    all present a piece of memory
#    actually, c_int, c_flaot are all Python Class
#    BUT 
#    ctypes DOES NOT overload the __eq__ function
#    
#    for example:
#    x = c_int32(0)
#    y = c_int32(0)
#
#    -> x != y              because x,y are 2 pointer ,although the content is same
#    -> x.value == y.value
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
#    x = "ABC"        -> you assign local variable x to a new string reference
#                     -> actually, x would be GC when change() returned  
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
#    but it support multiple objects in return
#
#    def tibrvTransport_Create(...) :
#       tx = ctypes.c_uint32(0)
#       status = _rv.tibrvTransportCreate(ctypes.byref(tx), ...)
#       return status, tx.value     -> type(tx.value) is Python int  
#
#    ...
#    status, ret = tibrvTransport_Create(...)
#
#
# 4. Python3 DOES NOT support c_char_p('text', 10)
#    In Python3,
#    c_char_p is char[], not a null-terminated string
#       you have to convert char[] <- -> str
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
#
#       for example
#       '12' -> char[] = [0x31, 0x32]
#       wchar would decode it as UTF16 0x3132 , and it is wrong  
# 
# 5. Naming Convension
#    pytibrv API use same naming exactly as TIBRV C
#    lowercase -> refer to TIBRV C include files(.h) 
#                 ex: tibrv_status, tibrv_Open(), ...
#    
#    pytibrv.Tibrv declare its own class, naming in capital
#    ex: TibrvMsg, TibrvMSgDateTime, TibrvQueue, ... 
#    
#    tibrvQueue -> API, refer to tibrvId = uint32 => Python int  
#    TibrvQueue -> Python Object 
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
# Python Class
# -----------------------------------------------------
# TibrvMsgDateTime          TIBRV C struct 
# TibrvMsgField             TIBRV C struct 
# Tibrv                     package for tibrv_XXXX
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161209 V1,0 ARIEN arien.chen@gmail.com
#   CREATED
#
##
from time import time as _time
import ctypes as _ctypes
from . import _load, _func
from .types import *

# module variable
_rv = _load('tibrv')


##-----------------------------------------------------------------------------
# tibrv/types.h
# declare _ctypes for internal use
##-----------------------------------------------------------------------------
_c_tibrv_i8                  = _ctypes.c_int8
_c_tibrv_u8                  = _ctypes.c_uint8
_c_tibrv_i16                 = _ctypes.c_int16
_c_tibrv_u16                 = _ctypes.c_uint16
_c_tibrv_i32                 = _ctypes.c_int32
_c_tibrv_u32                 = _ctypes.c_uint32
_c_tibrv_i64                 = _ctypes.c_int64
_c_tibrv_u64                 = _ctypes.c_uint64
_c_tibrv_f32                 = _ctypes.c_float
_c_tibrv_f64                 = _ctypes.c_double
_c_tibrv_bool                = _ctypes.c_int
_c_tibrv_ipport16            = _ctypes.c_uint16
_c_tibrv_ipaddr32            = _ctypes.c_uint32
_c_tibrv_str                 = _ctypes.c_char_p

_c_tibrv_status              = _ctypes.c_int32
_c_tibrvId                   = _ctypes.c_uint32
_c_tibrvMsg                  = _ctypes.c_void_p
_c_tibrvEvent                = _c_tibrvId
_c_tibrvDispatchable         = _c_tibrvId
_c_tibrvQueue                = _c_tibrvDispatchable
_c_tibrvQueueGroup           = _c_tibrvDispatchable
_c_tibrvTransport            = _c_tibrvId
_c_tibrvDispatcher           = _c_tibrvId
_c_tibrvEventType            = _ctypes.c_uint32
_c_tibrvQueueLimitPolicy     = _ctypes.c_int32
_c_tibrvIOType               = _ctypes.c_int32

# Array, C POINTER
_c_tibrv_bool_p              = _ctypes.POINTER(_c_tibrv_bool)
_c_tibrv_i8_p                = _ctypes.POINTER(_c_tibrv_i8)
_c_tibrv_u8_p                = _ctypes.POINTER(_c_tibrv_u8)
_c_tibrv_i16_p               = _ctypes.POINTER(_c_tibrv_i16)
_c_tibrv_u16_p               = _ctypes.POINTER(_c_tibrv_u16)
_c_tibrv_i32_p               = _ctypes.POINTER(_c_tibrv_i32)
_c_tibrv_u32_p               = _ctypes.POINTER(_c_tibrv_u32)
_c_tibrv_i64_p               = _ctypes.POINTER(_c_tibrv_i64)
_c_tibrv_u64_p               = _ctypes.POINTER(_c_tibrv_u64)
_c_tibrv_f32_p               = _ctypes.POINTER(_c_tibrv_f32)
_c_tibrv_f64_p               = _ctypes.POINTER(_c_tibrv_f64)
_c_tibrv_str_p               = _ctypes.POINTER(_c_tibrv_str)
_c_tibrvMsg_p                = _ctypes.POINTER(_c_tibrvMsg)

##
# Callback
# typedef void (*tibrvEventCallback) (
#                 tibrvEvent          event,
#                 tibrvMsg            message,
#                 void*               closure
#                );
#
_c_tibrvEventCallback = _func(_ctypes.c_void_p, _c_tibrvEvent, _c_tibrvMsg, _ctypes.c_void_p)

# typedef void (*tibrvEventVectorCallback) (
#                  tibrvMsg            messages[],
#                  tibrv_u32           numMessages
#                );
#
_c_tibrvEventVectorCallback = _func(None, _ctypes.POINTER(_c_tibrvMsg), _c_tibrv_u32)


# typedef void (*tibrvEventOnComplete) (
#                  tibrvEvent          event,
#                  void*               closure
#                );
#
_c_tibrvEventOnComplete = _func(None, _c_tibrvEvent, _ctypes.c_void_p)

# typedef void (*tibrvQueueOnComplete) (
#                  tibrvQueue          queue,
#                  void*               closure
#                 );
#
_c_tibrvQueueOnComplete = _func(None, _c_tibrvQueue, _ctypes.c_void_p)

_c_tibrvQueueHook = _func(None, _c_tibrvQueue, _ctypes.c_void_p)


# Helper Functions
def _cstr(sz: str, codepage = None) -> str:
    if sz is None:
        return None

    if codepage is None:
        return _c_tibrv_str(str(sz).encode())
    else:
        return _c_tibrv_str(str(sz).encode(codepage))

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



##
# tibrv/tibrv.h
# tibrv_status tibrv_Open(void)
#
_rv.tibrv_Open.argtypes = None
_rv.tibrv_Open.restype = _c_tibrv_status

def tibrv_Open() -> tibrv_status:
    status = _rv.tibrv_Open()
    return status

##
# tibrv/tibrv.h
# tibrv_status tibrv_Close(void)
#
_rv.tibrv_Close.argtypes = None
_rv.tibrv_Close.restype = _c_tibrv_status

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
