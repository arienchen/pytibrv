##
# pytibrv/msg.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.0 20161211 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# ---------------------------------------------------
# 1. Data Type
#    API NOT SUPPOTR
#       TIBRVMSG_ENCRYPTED
#       TIBRVMSG_XML
#
#    TibrvMsg NOT SUPPORT
#       TIBRVMSG_ENCRYPTED
#       TIBRVMSG_XML
#       TIBRVMSG_IPPORT16
#       TIBRVMSG_IPADDR32
#
# 2. Array
#    although, Python support array()
#    but it is for numeric only,
#
#    TO KEEP IT SIMPLE
#    Python list[] would be used for array.
#
#    TibrvMsg.addXXX(), TibrvMsg.setXXX() accept for list
#    ex:
#       TibrvMsg.addI32('NUM', 123)     -> tibrvMsg_AddI32()
#       TibrvMsg.addI32('NUM', [1,2,3]) -> tibrvMsg_AddI32Array()
#
#    TibrvMsg.getI32()       -> tibrvMsg_GetI32()
#    TibrvMsg.listI32()      -> tibrvMsg_GetI32Array()
#
# 3. Data Type Conversion
#    ctypes provide data check
#    ex:
#       ctypes.c_int32(obj) would do type checking
#       and exception when obj unable convert to int
#
#    All tibrvMsg_AddXXX(), tibrvMsg_UpdateXXX()
#    let ctypes to validate type checking
#
#    (1) integer
#        ctypes would convert to I8, U8, I16, ..., I64, U64
#        there is no OVERFLOW checking
#
#        ex:
#           x = 0x1234
#           n = ctypes.c_int8(x)    -> n.value is 0x34 , and no error
#
#        ctypes do very well for negative integer
#        ex:
#           x = 0xFF
#           m = ctypes.c_int8(x)    -> m.value = -1
#           n = ctypes.c_uint8(x)   -> n.value = 255
#
#           type(m.value), type(n.value) are both Python <class 'int'>
#
#        actually, Python 'int' support long long long ... int
#        like as Java BigInteger
#        ex:
#           x = 123456789012345678901234567890      -> 30 digits, over int64
#           print(x)                                -> no trucatcation
#
#    (2) float/double
#        Python 'float' is F64 , same as C double
#        not likely as 'int' support for BigInteger
#        Python float is just F64
#
#        ex:
#           x = 1.2345678901234567890               -> over the precession of F64
#           print(x)                                -> 1.2345678901234567 , truncated
#
#           m = ctypes.c_float(x)
#           n = ctypes.c_double(x)
#           print(m.value)                          -> 1.2345678806304932
#           print(n.value)                          -> 1.2345678901234567
#
#           ctypes.c_float() would convert to F32 (C float)
#           then convert again to F64(C double, Python float)
#           BEWARE the truncation of precession
#
#       IMHO:
#           use F64, instead of F32
#           DONT use F32, unless you have strong reason to do it
#
#           Remember the precession of F64 is 17 digits,
#           use str to prevent truncation
#
#           m = ctypes.c_float(1.3)
#           n = ctypes.c_double(1.3)
#           print(m.value)                          -> 1.2999999523162842
#           print(n.value)                          -> 1.3
#
#           in messaging level,
#           I would use str '1.3'
#           Let consumer to decide conversion to F32/F64 by itself.
#
#           actually, this is no problem, all done by TIBRV API
#           producer : tibrvMsg_UpdateString('123.456')
#           consumer : tibrvMsg_GetI32(), tibrvMsg_GetF64()
#
# 4. CodePage Encoding
#
#    In general, we would assume producer/consumer are in same code page
#    so, encode/decode is unnecessary for both side.
#
#    The Easy Way : HostCodePage = NetworkCodePage
#       But when you reading a local file,
#       You have to read in byte[] and decode for data's codepage
#
#    For best practice,
#    (1) It is consumer's responsibility to decode.
#
#    (2) Suggest UTF-8 for producer. (Network Code Page)
#        Most modern language process string as UTF internally.
#        CodePage conversion would lose characters in some cases.
#
#        for example:
#        Network Code Page is BIG5 (messaging level)
#
#        ProgA is Java,
#        It must set Host Code Page to BIG5 (file.encoding=BIG5)
#        It tell Java to decode MSG byte[BIG5] to String(UTF)
#
#        When ProgA construct MSG(BIG5)
#        Java would  encode String(UTF) to byte[BIG5]
#
#        There is no codepage attribute in TibrvMsgField for String
#        Only data, size to indicate char * and length
#
#        typedef struct tibrvMsgField
#        {
#           const char*                 name;
#           tibrv_u32                   size;
#           tibrv_u32                   count;
#           tibrvLocalData              data;
#           tibrv_u16                   id;
#           tibrv_u8                    type;
#        } tibrvMsgField;
#
#     (3) Send/Recv for different codepage
#         Python:
#           tibrvMsg_AddString, tibrvMsg_UpdateString, tibrvMsg_GetString
#           tibrvMsg_ConvertToString
#
#           All support parameter:codepage as optional (default is None)
#
#         Subject, Field Name NOT Support Code Page Conversion
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvMsg_AddXXX
#   tibrvMsg_ConvertToString
#   tibrvMsg_Create
#   tibrvMsg_CreateCopy
#   tibrvMsg_CreateEx
#   tibrvMsg_Destroy
#   tibrvMsg_Detach
#   tibrvMsg_Expend
#   tibrvMsg_GetBytesSize
#   tibrvMsg_GetClosure
#   tibrvMsg_GetCurrentTime
#   tibrvMsg_GetEvent
#   tibrvMsg_GetXXX
#   tibrvMsg_GetFieldByIndex
#   tibrvMsg_GetFieldInstance
#   tibrvMsg_GetNumFields
#   tibrvMsg_GetReplySubject
#   tibrvMsg_GetSendSubject
#   tibrvMsg_RemoveField
#   tibrvMsg_RemoveFieldInstance
#   tibrvMsg_Reset
#   tibrvMsg_SetReplySubject
#   tibrvMsg_SetSendSubject
#   tibrvMsg_UpdateXXX
#
#  *DataType: Opaque, Xml, IPPort16, IPAddress32
#  *tibrvMsg_ClearReference
#  *tibrvMsg_CreateFromBytes
#  *tibrvMsg_GetAsBytes
#  *tibrvMsg_GetAsBytesCopy
#  *tibrvMsg_MarkReference
#  *tibrvMsg_SetHandler
#  *tibrbMsg_Write
#  *tibrvMsg_SetCommId
#  *tibrvMsg_GetCommId
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161211 ARIEN V1.0
#   CREATED
#

import ctypes as _ctypes
import inspect as _inspect

from .status import *
from .api import _rv, _cstr, _pystr


class c_tibrvMsgDateTime(_ctypes.Structure):
    _fields_ = [("sec", c_tibrv_i64),
                ("nsec", c_tibrv_u32)]

    def __init__(self, dt: TibrvMsgDateTime = None):
        if dt is None:
            return

        self.sec = dt.sec
        self.nsec = dt.nsec

    def castTo(self, dt: TibrvMsgDateTime):
        if dt is None:
            return
        dt.sec = self.sec
        dt.nsec = self.nsec


class c_tibrvLocalData(_ctypes.Union):
    _fields_ = [("msg", c_tibrvMsg),
                ("str", _ctypes.c_char_p),
                ("buf", _ctypes.c_void_p),
                ("array", _ctypes.c_void_p),
                ("boolean", c_tibrv_bool),
                ("i8", c_tibrv_i8),
                ("u8", c_tibrv_u8),
                ("i16", c_tibrv_i16),
                ("u16", c_tibrv_u16),
                ("i32", c_tibrv_i32),
                ("u32", c_tibrv_u32),
                ("i64", c_tibrv_i64),
                ("u64", c_tibrv_u64),
                ("f32", c_tibrv_f32),
                ("f64", c_tibrv_f64),
                ("ipport16", c_tibrv_ipport16),
                ("ipaddr32", c_tibrv_ipaddr32),
                ("date", c_tibrvMsgDateTime)]


class c_tibrvMsgField(_ctypes.Structure):
    _fields_ = [("name", _ctypes.c_char_p),
                ("size", c_tibrv_u32),
                ("count", c_tibrv_u32),
                ("data", c_tibrvLocalData),
                ("id", c_tibrv_u16),
                ("type", c_tibrv_u8)]

    def __init__(self, fld: TibrvMsgField = None):

        if fld is None:
            return

        self.name = _cstr(fld.name)
        self.size = fld.size
        self.count = fld.count
        self.id = fld.id
        self.type = fld.type

        if TIBRVMSG_I8 <= fld.type <= TIBRVMSG_U64:
            self.data.u64 = fld.data
            return

        if TIBRVMSG_F32 <= fld.type <= TIBRVMSG_F64:
            self.data.f64 = fld.data
            return

        if TIBRVMSG_STRING == fld.type:
            self.data.str = _cstr(fld.data)

            # TODO

    def castTo(self, obj: TibrvMsgField):

        obj.name = self.name
        obj._size = self.size
        obj._count = self.count
        obj._id = self.id
        obj._type = self.type

        if obj.type == TIBRVMSG_I8:
            obj.int8 = self.data.i8.value
            return

        if obj.type == TIBRVMSG_U8:
            obj.uint8 = self.data.u8.value
            return

        if obj.type == TIBRVMSG_I16:
            obj.int16 = self.data.i16.value
            return

        if obj.type == TIBRVMSG_U16:
            obj.uint16 = self.data.u16.value
            return

        if obj.type == TIBRVMSG_I32:
            obj.int32 = self.data.i32.value
            return

        if obj.type == TIBRVMSG_U32:
            obj.uint32 = self.data.U32.value
            return

        if obj.type == TIBRVMSG_I64:
            obj.int64 = self.data.i64
            return

        if obj.type == TIBRVMSG_U64:
            obj.uint64 = self.data.u64.value
            return

        if obj.type == TIBRVMSG_F32:
            obj.f32 = self.data.f32.value
            return

        if obj.type == TIBRVMSG_F64:
            obj.f64 = self.data.f64.value
            return

        if obj.type == TIBRVMSG_STRING:
            obj.str = self.data.str.decode()
            return

        if obj.type == TIBRVMSG_MSG:
            obj.msg = self.data.msg.value
            return

        if obj.type == TIBRVMSG_DATETIME:
            dt = TibrvMsgDateTime()
            dt.sec = self.data.date.sec.value
            dt.nsec = self.date.date.nsec.value
            obj.data = dt
            return

            # TODO array

##-----------------------------------------------------------------------------
## TibrvMsg
##-----------------------------------------------------------------------------
##
# tibrv/msg.h
# tibrv_status tibrvMsg_Create(
#                tibrvMsg*           message
#              );
#
# tibrv_status tibrvMsg_CreateEx(
#                tibrvMsg*           message,
#                tibrv_u32           initialStorage
#              );
#
_rv.tibrvMsg_Create.argtypes = [_ctypes.POINTER(c_tibrvMsg)]
_rv.tibrvMsg_Create.restype = c_tibrv_status

_rv.tibrvMsg_CreateEx.argtypes = [_ctypes.POINTER(c_tibrvMsg), c_tibrv_u32]
_rv.tibrvMsg_CreateEx.restype = c_tibrv_status

def tibrvMsg_Create(initialStorage: int=0) -> (tibrv_status, tibrvMsg):

    msg = c_tibrvMsg(0)
    if initialStorage == 0:
        status = _rv.tibrvMsg_Create(_ctypes.byref(msg))
    else:
        try:
            n = c_tibrv_u32(initialStorage)

        except:
            return TIBRV_INVALID_ARG

        status = _rv.tibrvMsg_CreateEx(_ctypes.byref(msg), n)

    return status, msg.value


##
# tibrv/msg.h
# tibrv_status tibrvMsg_Destroy(
#                tibrvMsg            message
#              );
#
_rv.tibrvMsg_Destroy.argtypes = [c_tibrvMsg]
_rv.tibrvMsg_Destroy.restype = c_tibrv_status

def tibrvMsg_Destroy(message:tibrvMsg) -> tibrv_status:

    msg = c_tibrvMsg(message)
    status = _rv.tibrvMsg_Destroy(msg)

    return status

##
# tibrv/msg.h
# tibrv_status tibrvMsg_Detach(
#                tibrvMsg            message
#              );
#
_rv.tibrvMsg_Detach.argtypes = [c_tibrvMsg]
_rv.tibrvMsg_Detach.restype = c_tibrv_status

def tibrvMsg_Detach(message:tibrvMsg) -> tibrv_status:

    msg = c_tibrvMsg(message)
    status = _rv.tibrvMsg_Detach(msg)

    return status

##
# tibrv/msg.h
# tibrv_status tibrvMsg_CreateCopy(
#                const tibrvMsg              message,
#                tibrvMsg*                   copy
#              );
#
_rv.tibrvMsg_CreateCopy.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrvMsg)]
_rv.tibrvMsg_CreateCopy.restype = c_tibrv_status

def tibrvMsg_CreateCopy(message:tibrvMsg) -> (tibrv_status, tibrvMsg):

    msg = c_tibrvMsg(message)
    cc  = c_tibrvMsg(0)

    status = _rv.tibrvMsg_CreateCopy(msg, _ctypes.byref(cc))

    return status, cc.value

##
# tibrv/msg.h
# tibrv_status tibrvMsg_Reset(
#                tibrvMsg            message
#              );
#
_rv.tibrvMsg_Reset.argtypes = [c_tibrvMsg]
_rv.tibrvMsg_Reset.restype = c_tibrv_status

def tibrvMsg_Reset(message:tibrvMsg) -> tibrv_status:

    msg = c_tibrvMsg(message)
    status = _rv.tibrvMsg_Reset(msg)

    return status

##
# tibrv/msg.h
# tibrv_status tibrvMsg_Expand(
#                tibrvMsg            message,
#                tibrv_i32           additionalStorage
#              );
#
_rv.tibrvMsg_Expand.argtypes = [c_tibrvMsg, c_tibrv_i32]
_rv.tibrvMsg_Expand.restype = c_tibrv_status

def tibrvMsg_Expand(message:tibrvMsg, additionalStorage:int) -> tibrv_status:

    msg = c_tibrvMsg(message)
    n = c_tibrv_u32(additionalStorage)

    status = _rv.tibrvMsg_Expand(msg, n)

    return status

##
# tibrv/msg.h
# tibrv_status tibrvMsg_SetSendSubject(
#                tibrvMsg            message,
#                const char*         subject
#              );
#
_rv.tibrvMsg_SetSendSubject.argtypes = [c_tibrvMsg, c_tibrv_str]
_rv.tibrvMsg_SetSendSubject.restype = c_tibrv_status

def tibrvMsg_SetSendSubject(message:tibrvMsg, subject:str) -> tibrv_status:

    msg = c_tibrvMsg(message)
    sz = _cstr(subject)

    status = _rv.tibrvMsg_SetSendSubject(msg, sz)

    return status


##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetSendSubject(
#                tibrvMsg            message,
#                const char**        subject
#              );
#
_rv.tibrvMsg_GetSendSubject.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrv_str)]
_rv.tibrvMsg_GetSendSubject.restype = c_tibrv_status

def tibrvMsg_GetSendSubject(message:tibrvMsg) -> (tibrv_status, str):

    msg = c_tibrvMsg(message)
    sz = c_tibrv_str(0)
    status = _rv.tibrvMsg_GetSendSubject(msg, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/msg.h
# tibrv_status tibrvMsg_SetReplySubject(
#                tibrvMsg            message,
#                const char*         replySubject
#              );
#
_rv.tibrvMsg_SetReplySubject.argtypes = [c_tibrvMsg, c_tibrv_str]
_rv.tibrvMsg_SetReplySubject.restype = c_tibrv_status

def tibrvMsg_SetReplySubject(message:tibrvMsg, subject:str) -> tibrv_status:

    msg = c_tibrvMsg(message)
    sz = _cstr(subject)
    status = _rv.tibrvMsg_SetReplySubject(msg, sz)

    return status

##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetReplySubject(
#                tibrvMsg            message,
#                const char**        replySubject
#              );
#
_rv.tibrvMsg_GetReplySubject.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrv_str)]
_rv.tibrvMsg_GetReplySubject.restype = c_tibrv_status

def tibrvMsg_GetReplySubject(message:tibrvMsg) -> (tibrv_status, str):

    msg = c_tibrvMsg(message)
    sz = c_tibrv_str(0)
    status = _rv.tibrvMsg_GetReplySubject(msg, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetEvent(
#                tibrvMsg            message,
#                tibrvEvent*         eventId
#              );
#
_rv.tibrvMsg_GetEvent.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrvEvent)]
_rv.tibrvMsg_GetEvent.restype = c_tibrv_status

def tibrvMsg_GetEvent(message: tibrvMsg) -> (tibrv_status,tibrvEvent):

    msg = c_tibrvMsg(message)
    n = c_tibrvEvent(0)

    status = _rv.tibrvMsg_GetEvent(msg, _ctypes.byref(n))

    return status, n.value


##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetClosure(
#                tibrvMsg            message,
#                void**              closure
#              );
#
_rv.tibrvMsg_GetClosure.argtypes = [c_tibrvMsg, _ctypes.POINTER(_ctypes.py_object)]
_rv.tibrvMsg_GetClosure.restype = c_tibrv_status

def tibrvMsg_GetClosure(message: tibrvMsg) -> (tibrv_status, object):

    ret = None
    msg = c_tibrvMsg(message)
    cz = _ctypes.py_object
    status = _rv.tibrvMsg_GetClosure(msg, _ctypes.byref(cz))

    # cast to Python Object
    if status == TIBRV_OK:
        ret = _ctypes.cast(cz, _ctypes.py_object).value

    return status, ret

##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetNumFields(
#                tibrvMsg            message,
#                tibrv_u32*          numFields
#              );
#
_rv.tibrvMsg_GetNumFields.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrv_u32)]
_rv.tibrvMsg_GetNumFields.restype = c_tibrv_status

def tibrvMsg_GetNumFields(message: tibrvMsg) -> (tibrv_status, int):

    msg = c_tibrvMsg(message)
    n = c_tibrv_u32(0)
    status = _rv.tibrvMsg_GetNumFields(msg, _ctypes.byref(n))

    return status, n.value


##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetByteSize(
#                tibrvMsg            message,
#                tibrv_u32*          byteSize
#              );
#
_rv.tibrvMsg_GetByteSize.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrv_u32)]
_rv.tibrvMsg_GetByteSize.restype = c_tibrv_status

def tibrvMsg_GetByteSize(message: tibrvMsg) -> (tibrv_status, int):

    msg = c_tibrvMsg(message)
    n = c_tibrv_u32(0)
    status = _rv.tibrvMsg_GetByteSize(msg, _ctypes.byref(n))

    return status, n.value



##
# tibrv/msg.h
# tibrv_status tibrvMsg_ConvertToString(
#                tibrvMsg            message,
#                const char**        string
#              );
#
_rv.tibrvMsg_ConvertToString.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrv_str)]
_rv.tibrvMsg_ConvertToString.restype = c_tibrv_status

def tibrvMsg_ConvertToString(message: tibrvMsg, codepage:str=None) -> (tibrv_status,str):

    msg = c_tibrvMsg(message)
    sz = c_tibrv_str(0)
    status = _rv.tibrvMsg_ConvertToString(msg, _ctypes.byref(sz))

    return status, _pystr(sz, codepage)


##
# tibrv/msg.h
# tibrv_status tibrvMsg_GetCurrentTime(
#                tibrvMsgDateTime* dateTime
#              );
#
# tibrv_status tibrvMsg_GetCurrentTimeString(
#                char* local,
#                char* gmt
#              );
#
_rv.tibrvMsg_GetCurrentTime.argtypes = [_ctypes.POINTER(c_tibrvMsgDateTime)]
_rv.tibrvMsg_GetCurrentTime.restype = c_tibrv_status

def tibrvMsg_GetCurrentTime() -> (tibrv_status, TibrvMsgDateTime):

    ret = None

    dt = c_tibrvMsgDateTime()
    status = _rv.tibrvMsg_GetCurrentTime(_ctypes.byref(dt))

    if status == TIBRV_OK:
        ret = TibrvMsgDateTime()
        dt.castTo(ret)

    return status, ret

_rv.tibrvMsg_GetCurrentTimeString.argtypes = [c_tibrv_str, c_tibrv_str]
_rv.tibrvMsg_GetCurrentTimeString.restype = c_tibrv_status

def tibrvMsg_GetCurrentTimeString() -> (tibrv_status, str, str):

    ret = None

    local_time = _ctypes.create_string_buffer(TIBRVMSG_DATETIME_STRING_SIZE)
    gmt_time = _ctypes.create_string_buffer(TIBRVMSG_DATETIME_STRING_SIZE)

    status = _rv.tibrvMsg_GetCurrentTimeString(local_time, gmt_time)

    if status != TIBRV_OK:
        return status, None, None

    return TIBRV_OK, _pystr(local_time), _pystr(gmt_time)


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddDateTimeEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrvMsgDateTime * value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateDateTimeEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrvMsgDateTime * value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetDateTimeEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsgDateTime*   value,
#                tibrv_u16           optIdentifier
#              );
#

_rv.tibrvMsg_AddDateTimeEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrvMsgDateTime), c_tibrv_u16]
_rv.tibrvMsg_AddDateTimeEx.restype = c_tibrv_status

def tibrvMsg_AddDateTime(message:tibrvMsg, fieldName:str, value:TibrvMsgDateTime, optIdentifier:int = 0) -> tibrv_status:

    if value is not None and type(value) is not TibrvMsgDateTime:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        dt = c_tibrvMsgDateTime(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddDateTimeEx(msg, name, _ctypes.byref(dt), id)

    return status

_rv.tibrvMsg_UpdateDateTimeEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrvMsgDateTime), c_tibrv_u16]
_rv.tibrvMsg_UpdateDateTimeEx.restype = c_tibrv_status

def tibrvMsg_UpdateDateTime(message:tibrvMsg, fieldName:str, value:TibrvMsgDateTime, optIdentifier:int = 0) -> tibrv_status:

    if value is not None and type(value) is not TibrvMsgDateTime:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        dt = c_tibrvMsgDateTime(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateDateTimeEx(msg, name, _ctypes.byref(dt), id)

    return status

_rv.tibrvMsg_GetDateTimeEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrvMsgDateTime), c_tibrv_u16]
_rv.tibrvMsg_GetDateTimeEx.restype = c_tibrv_status

def tibrvMsg_GetDateTime(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, TibrvMsgDateTime):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrvMsgDateTime()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetDateTimeEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = TibrvMsgDateTime()
        val.castTo(ret)

    return status, ret

##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddBoolEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_bool          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateBoolEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_bool          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetBoolEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_bool*         value,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddBoolEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_bool, c_tibrv_u16]
_rv.tibrvMsg_AddBoolEx.restype = c_tibrv_status

def tibrvMsg_AddBool(message:tibrvMsg, fieldName:str, value:bool, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_bool(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddBoolEx(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateBoolEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_bool, c_tibrv_u16]
_rv.tibrvMsg_UpdateBoolEx.restype = c_tibrv_status

def tibrvMsg_UpdateBool(message:tibrvMsg, fieldName:str, value:bool, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_bool(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateBoolEx(msg, name, val, id)

    return status


_rv.tibrvMsg_GetBoolEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_bool), c_tibrv_u16]
_rv.tibrvMsg_GetBoolEx.restype = c_tibrv_status

def tibrvMsg_GetBool(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, bool):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_bool()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetBoolEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddI8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i8            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i8            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_AddI8ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i8*     array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI8ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i8*     array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i8*           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI8ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i8**    array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddI8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i8, c_tibrv_u16]
_rv.tibrvMsg_AddI8Ex.restype = c_tibrv_status

def tibrvMsg_AddI8(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i8(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI8Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateI8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i8, c_tibrv_u16]
_rv.tibrvMsg_UpdateI8Ex.restype = c_tibrv_status

def tibrvMsg_UpdateI8(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i8(int(value))
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI8Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetI8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_i8), c_tibrv_u16]
_rv.tibrvMsg_GetI8Ex.restype = c_tibrv_status

def tibrvMsg_GetI8(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i8()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI8Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret

_rv.tibrvMsg_AddI8ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i8_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddI8ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddI8Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i8 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI8ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i8_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateI8ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateI8Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i8 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI8ArrayEx.argtypes = [c_tibrvMsg,
                                      _ctypes.c_char_p,
                                      _ctypes.POINTER(c_tibrv_i8_p),
                                      _ctypes.POINTER(c_tibrv_u32),
                                      c_tibrv_u16]
_rv.tibrvMsg_GetI8ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetI8Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i8_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI8ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddU8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u8            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u8            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU8ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u8*     array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU8Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u8*           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU8ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u8**    array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddU8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u8, c_tibrv_u16]
_rv.tibrvMsg_AddU8Ex.restype = c_tibrv_status

def tibrvMsg_AddU8(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u8(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU8Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateU8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u8, c_tibrv_u16]
_rv.tibrvMsg_UpdateU8Ex.restype = c_tibrv_status

def tibrvMsg_UpdateU8(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u8(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU8Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetU8Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_u8), c_tibrv_u16]
_rv.tibrvMsg_GetU8Ex.restype = c_tibrv_status

def tibrvMsg_GetU8(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u8()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU8Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU8ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u8_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU8ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddU8Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u8 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU8ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u8_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateU8ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateU8Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u8 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU8ArrayEx.argtypes = [c_tibrvMsg,
                                      _ctypes.c_char_p,
                                      _ctypes.POINTER(c_tibrv_u8_p),
                                      _ctypes.POINTER(c_tibrv_u32),
                                      c_tibrv_u16]
_rv.tibrvMsg_GetU8ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetU8Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u8_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU8ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddI16Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i16           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI16Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i16           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI16ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i16*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI16Ex(
#              tibrvMsg            message,
#              const char*         fieldName,
#              tibrv_i16*          value,
#              tibrv_u16           optIdentifier
#            );
#
# tibrv_status tibrvMsg_GetI16ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i16**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddI16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i16, c_tibrv_u16]
_rv.tibrvMsg_AddI16Ex.restype = c_tibrv_status

def tibrvMsg_AddI16(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i16(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI16Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateI16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i16, c_tibrv_u16]
_rv.tibrvMsg_UpdateI16Ex.restype = c_tibrv_status

def tibrvMsg_UpdateI16(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i16(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI16Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetI16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_i16), c_tibrv_u16]
_rv.tibrvMsg_GetI16Ex.restype = c_tibrv_status

def tibrvMsg_GetI16(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i16(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI16Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI16ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i16_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddI16ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddI16Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i16 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI16ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i16_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateI16ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateI16Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i16 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI16ArrayEx.argtypes = [c_tibrvMsg,
                                      _ctypes.c_char_p,
                                      _ctypes.POINTER(c_tibrv_i16_p),
                                      _ctypes.POINTER(c_tibrv_u32),
                                      c_tibrv_u16]
_rv.tibrvMsg_GetI16ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetI16Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i16_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI16ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddU16Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u16           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU16Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u16           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU16ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u16*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU16Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u16*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU16ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u16**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddU16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u16, c_tibrv_u16]
_rv.tibrvMsg_AddU16Ex.restype = c_tibrv_status

def tibrvMsg_AddU16(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u16(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u16, c_tibrv_u16]
_rv.tibrvMsg_UpdateU16Ex.restype = c_tibrv_status

def tibrvMsg_UpdateU16(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u16(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetU16Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_u16), c_tibrv_u16]
_rv.tibrvMsg_GetU16Ex.restype = c_tibrv_status

def tibrvMsg_GetU16(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u16(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU16Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU16ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u16_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU16ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddU16Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u16 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU16ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u16_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateU16ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateU16Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u16 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU16ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_u16_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetU16ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetU16Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u16_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU16ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddI32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i32*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i32*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i32**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#

_rv.tibrvMsg_AddI32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i32, c_tibrv_u16]
_rv.tibrvMsg_AddI32Ex.restype = c_tibrv_status

def tibrvMsg_AddI32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI32Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateI32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i32, c_tibrv_u16]
_rv.tibrvMsg_UpdateI32Ex.restype = c_tibrv_status

def tibrvMsg_UpdateI32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI32Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetI32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_i32), c_tibrv_u16]
_rv.tibrvMsg_GetI32Ex.restype = c_tibrv_status

def tibrvMsg_GetI32(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddI32ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddI32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateI32ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateI32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI32ArrayEx.argtypes = [c_tibrvMsg,
                                      _ctypes.c_char_p,
                                      _ctypes.POINTER(c_tibrv_i32_p),
                                      _ctypes.POINTER(c_tibrv_u32),
                                      c_tibrv_u16]
_rv.tibrvMsg_GetI32ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetI32Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i32_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddU32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_AddU32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u32*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u32*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u32**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddU32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU32Ex.restype = c_tibrv_status

def tibrvMsg_AddU32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU32Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateU32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateU32Ex.restype = c_tibrv_status

def tibrvMsg_UpdateU32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU32Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetU32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_u32), c_tibrv_u16]
_rv.tibrvMsg_GetU32Ex.restype = c_tibrv_status

def tibrvMsg_GetU32(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u32()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU32ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddU32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateU32ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateU32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (_ctypes.c_uint32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU32ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_u32_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetU32ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetU32Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u32_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddI64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateI64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i64*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_i64*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetI64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_i64**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddI64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i64, c_tibrv_u16]
_rv.tibrvMsg_AddI64Ex.restype = c_tibrv_status

def tibrvMsg_AddI64(message:tibrvMsg, fieldName: str, value: int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI64Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateI64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i64, c_tibrv_u16]
_rv.tibrvMsg_UpdateI64Ex.restype = c_tibrv_status

def tibrvMsg_UpdateI64(message:tibrvMsg, fieldName: str, value: int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI64Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetI64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_i64), c_tibrv_u16]
_rv.tibrvMsg_GetI64Ex.restype = c_tibrv_status

def tibrvMsg_GetI64(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_i64(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddI64ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddI64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_i64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateI64ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateI64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_i64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI64ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_i64_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetI64ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetI64Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_i64_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetI64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddU64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateU64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u64*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u64*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetU64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_u64**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier);
#
_rv.tibrvMsg_AddU64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u64, c_tibrv_u16]
_rv.tibrvMsg_AddU64Ex.restype = c_tibrv_status

def tibrvMsg_AddU64(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u64, c_tibrv_u16]
_rv.tibrvMsg_UpdateU64Ex.restype = c_tibrv_status

def tibrvMsg_UpdateU64(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU64Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetU64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_u64), c_tibrv_u16]
_rv.tibrvMsg_GetU64Ex.restype = c_tibrv_status

def tibrvMsg_GetU64(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_u64()
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU64ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddU64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_u64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateU64ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateU64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_u64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU64ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_u64_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetU64ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetU64Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_u64_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetU64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddF32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateF32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f32           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateF32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_f32*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetF32Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f32*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetF32ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_f32**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddF32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f32, c_tibrv_u16]
_rv.tibrvMsg_AddF32Ex.restype = c_tibrv_status

def tibrvMsg_AddF32(message:tibrvMsg, fieldName:str, value:float, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateF32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f32, c_tibrv_u16]
_rv.tibrvMsg_UpdateF32Ex.restype = c_tibrv_status

def tibrvMsg_UpdateF32(message:tibrvMsg, fieldName:str, value:float, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f32(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetF32Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_f32), c_tibrv_u16]
_rv.tibrvMsg_GetF32Ex.restype = c_tibrv_status

def tibrvMsg_GetF32(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, float):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_f32(0.0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetF32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret



_rv.tibrvMsg_AddF32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddF32ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddF32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_f32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateF32ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f32_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateF32ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateF32Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_f32 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetF32ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_f32_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetF32ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetF32Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f32_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetF32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddF64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateF64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f64           value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateF64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_f64*    array,
#                tibrv_u32           numElements,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetF64Ex(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_f64*          value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetF64ArrayEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const tibrv_f64**   array,
#                tibrv_u32*          numElements,
#                tibrv_u16           optIdentifier
#              );
#
_rv.tibrvMsg_AddF64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f64, c_tibrv_u16]
_rv.tibrvMsg_AddF64Ex.restype = c_tibrv_status

def tibrvMsg_AddF64(message:tibrvMsg, fieldName:str, value:float, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateF64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f64, c_tibrv_u16]
_rv.tibrvMsg_UpdateF64Ex.restype = c_tibrv_status

def tibrvMsg_UpdateF64(message:tibrvMsg, fieldName:str, value:float, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f64(value)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF64Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetF64Ex.argtypes = [c_tibrvMsg, _ctypes.c_char_p, _ctypes.POINTER(c_tibrv_f64), c_tibrv_u16]
_rv.tibrvMsg_GetF64Ex.restype = c_tibrv_status

def tibrvMsg_GetF64(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, float):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_f64(0.0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetF64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddF64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddU64ArrayEx.restype = c_tibrv_status

def tibrvMsg_AddF64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_f64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateF64ArrayEx.argtypes = [c_tibrvMsg, _ctypes.c_char_p, c_tibrv_f64_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateF64ArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateF64Array(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_f64 * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetF64ArrayEx.argtypes = [c_tibrvMsg,
                                       _ctypes.c_char_p,
                                       _ctypes.POINTER(c_tibrv_f64_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetF64ArrayEx.restype = c_tibrv_status

def tibrvMsg_GetF64Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_f64_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetF64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddStringEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const char*         value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateStringEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const char*         value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateStringArrayEx(
#                tibrvMsg            message,
#                const char*         field_name,
#                const char**        value,
#                tibrv_u32           num_elements,
#                tibrv_u16           opt_identifier
#              );
#
# tibrv_status tibrvMsg_GetStringEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                const char**        value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetStringArrayEx(
#                tibrvMsg            message,
#                const char*         field_name,
#                const char***       ptr_addr,
#                tibrv_u32*          num_elements_addr,
#                tibrv_u16           opt_identifier
#              );
#
_rv.tibrvMsg_AddStringEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_str, c_tibrv_u16]
_rv.tibrvMsg_AddStringEx.restype = c_tibrv_status

def tibrvMsg_AddString(message:tibrvMsg, fieldName:str, value:str, optIdentifier:int = 0, codepage:str = None) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = _cstr(value, codepage)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddStringEx(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateStringEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_str, c_tibrv_u16]
_rv.tibrvMsg_UpdateStringEx.restype = c_tibrv_status

def tibrvMsg_UpdateString(message:tibrvMsg, fieldName:str, value:str, optIdentifier:int = 0, codepage:str=None) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = _cstr(value, codepage)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateStringEx(msg, name, val, id)

    return status

_rv.tibrvMsg_GetStringEx.argtypes = [c_tibrvMsg, c_tibrv_str, _ctypes.POINTER(c_tibrv_str), c_tibrv_u16]
_rv.tibrvMsg_GetStringEx.restype = c_tibrv_status

def tibrvMsg_GetString(message:tibrvMsg, fieldName:str, optIdentifier:int = 0, codepage:str=None) -> (tibrv_status, str):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrv_str(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetStringEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = _pystr(val, codepage)

    return status, ret



_rv.tibrvMsg_AddStringArrayEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_str_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddStringArrayEx.restype = c_tibrv_status

def tibrvMsg_AddStringArray(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0, codepage=None) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_str * n)()
        for x in range(n):
            val[x] = _cstr(value[x], codepage)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddStringArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateStringArrayEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_str_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateStringArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateStringArray(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0, codepage=None) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrv_str * n)()
        for x in range(n):
            val[x] = _cstr(value[x], codepage)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateStringArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetStringArrayEx.argtypes = [c_tibrvMsg,
                                          c_tibrv_str,
                                          _ctypes.POINTER(c_tibrv_str_p),
                                          _ctypes.POINTER(c_tibrv_u32),
                                          c_tibrv_u16]
_rv.tibrvMsg_GetStringArrayEx.restype = c_tibrv_status

def tibrvMsg_GetStringArray(message:tibrvMsg, fieldName:str, optIdentifier:int = 0, codepage = None) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrv_str_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetStringArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(_pystr(val[x], codepage))

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddMsgEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsg            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateMsgEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsg            value,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_UpdateMsgArrayEx(
#                tibrvMsg            message,
#                const char*         field_name,
#                const tibrvMsg*     value,
#                tibrv_u32           num_elements,
#                tibrv_u16           opt_identifier
#              );
#
# tibrv_status tibrvMsg_GetMsgEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsg*           field,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetMsgArrayEx(
#                tibrvMsg            message,
#                const char*         field_name,
#                const tibrvMsg**    ptr_addr,
#                tibrv_u32*          num_elements_addr,
#                tibrv_u16           opt_identifier
#              );
#
_rv.tibrvMsg_AddMsgEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrvMsg, c_tibrv_u16]
_rv.tibrvMsg_AddMsgEx.restype = c_tibrv_status

def tibrvMsg_AddMsg(message:tibrvMsg, fieldName:str, value:tibrvMsg, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        id = c_tibrv_u16(optIdentifier)
        val = c_tibrvMsg(value)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddMsgEx(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateMsgEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrvMsg, c_tibrv_u16]
_rv.tibrvMsg_UpdateMsgEx.restype = c_tibrv_status

def tibrvMsg_UpdateMsg(message:tibrvMsg, fieldName:str, value:tibrvMsg, optIdentifier:int = 0) -> tibrv_status:

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        id = c_tibrv_u16(optIdentifier)
        val = c_tibrvMsg(value)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateMsgEx(msg, name, val, id)

    return status

_rv.tibrvMsg_GetMsgEx.argtypes = [c_tibrvMsg, c_tibrv_str, _ctypes.POINTER(c_tibrvMsg), c_tibrv_u16]
_rv.tibrvMsg_GetMsgEx.restype = c_tibrv_status

def tibrvMsg_GetMsg(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, tibrvMsg):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)
        val = c_tibrvMsg(0)
        id = c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetMsgEx(msg, name, _ctypes.byref(val), id)
    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddMsgArrayEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrvMsg_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_AddMsgArrayEx.restype = c_tibrv_status

def tibrvMsg_AddMsgArray(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrvMsg * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddMsgArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateMsgArrayEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrvMsg_p, c_tibrv_u32, c_tibrv_u16]
_rv.tibrvMsg_UpdateMsgArrayEx.restype = c_tibrv_status

def tibrvMsg_UpdateMsgArray(message:tibrvMsg, fieldName:str, value:list, optIdentifier:int = 0) -> tibrv_status:

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        n = len(value)

        val = (c_tibrvMsg * n)(*value)

        num = c_tibrv_u32(n)

        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateMsgArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetMsgArrayEx.argtypes = [c_tibrvMsg,
                                       c_tibrv_str,
                                       _ctypes.POINTER(c_tibrvMsg_p),
                                       _ctypes.POINTER(c_tibrv_u32),
                                       c_tibrv_u16]
_rv.tibrvMsg_GetMsgArrayEx.restype = c_tibrv_status

def tibrvMsg_GetMsgArray(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    ret = None

    try:
        msg = c_tibrvMsg(message)
        name = _cstr(fieldName)

        val = c_tibrvMsg_p()
        num = c_tibrv_u32(0)
        id = c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetMsgArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
# tibrv/msg.h
# tibrv_status tibrvMsg_AddField(
#                tibrvMsg            message,
#                tibrvMsgField*      field
#              );
#
# tibrv_status tibrvMsg_UpdateField(
#                tibrvMsg                    message,
#                tibrvMsgField*              field
#              );
#
# tibrv_status tibrvMsg_GetFieldEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsgField*      field,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_GetFieldInstance(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrvMsgField*      fieldAddr,
#                tibrv_u32           instance
#              );
#
# tibrv_status tibrvMsg_GetFieldByIndex(
#                tibrvMsg            message,
#                tibrvMsgField*      field,
#                tibrv_u32           fieldIndex
#              );
#
#
_rv.tibrvMsg_AddField.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrvMsgField)]
_rv.tibrvMsg_AddField.restype = c_tibrv_status

def tibrvMsg_AddField(message:tibrvMsg, field:TibrvMsgField) -> tibrv_status:
    if field is None or type(field) is not TibrvMsgField:
        return TIBRV_INVALID_ARG

    msg = c_tibrvMsg(message)
    val = c_tibrvMsgField(field)

    status = _rv.tibrvMsg_AddFieldEx(message, _ctypes.byref(val))

    return status


_rv.tibrvMsg_UpdateField.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrvMsgField)]
_rv.tibrvMsg_UpdateField.restype = c_tibrv_status

def tibrvMsg_UpdateField(message: tibrvMsg, field:TibrvMsgField) -> tibrv_status:
    if field is None or type(field) is not TibrvMsgField:
        return TIBRV_INVALID_ARG

    msg = c_tibrvMsg(message)
    val = c_tibrvMsgField(field)

    status = _rv.tibrvMsg_UpdateFieldEx(msg, _ctypes.byref(val))

    return status


_rv.tibrvMsg_GetFieldEx.argtypes = [c_tibrvMsg, c_tibrv_str, _ctypes.POINTER(c_tibrvMsgField), c_tibrv_u16]
_rv.tibrvMsg_GetFieldEx.restype = c_tibrv_status

def tibrvMsg_GetField(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, TibrvMsgField):

    ret = None
    msg = c_tibrvMsg(message)
    name = _cstr(fieldName)
    val = c_tibrvMsgField()
    id = c_tibrv_u16(int(optIdentifier))

    status = _rv.tibrvMsg_GetFieldEx(msg, name, _ctypes.byref(val), id)
    if status == TIBRV_OK:
        ret = TibrvMsgField()
        val.castTo(ret);

    return status, ret


_rv.tibrvMsg_GetFieldInstance.argtypes = [c_tibrvMsg, c_tibrv_str, _ctypes.POINTER(c_tibrvMsgField), c_tibrv_u32]
_rv.tibrvMsg_GetFieldInstance.restype = c_tibrv_status

def tibrvMsg_GetFieldInstance(message:tibrvMsg, fieldName:str, fieldAddr:TibrvMsgField, instance:int ) -> tibrv_status:
    if fieldAddr is None or type(fieldAddr) is not TibrvMsgField:
        return TIBRV_INVALID_ARG

    msg = c_tibrvMsg(message)
    name = _cstr(fieldName)
    val = c_tibrvMsgField()
    inst = c_tibrv_u32(instance)

    status = _rv.tibrvMsg_GetFieldInstance(msg, name, _ctypes.byref(val), inst)
    if status == TIBRV_OK:
        val.castTo(fieldAddr);

    return status


_rv.tibrvMsg_GetFieldByIndex.argtypes = [c_tibrvMsg, _ctypes.POINTER(c_tibrvMsgField), c_tibrv_u32]
_rv.tibrvMsg_GetFieldByIndex.restype = c_tibrv_status

def tibrvMsg_GetFieldByIndex(message:tibrvMsg, fieldIndex:int ) -> (tibrv_status,TibrvMsgField):

    ret = None
    msg = c_tibrvMsg(message)
    val = c_tibrvMsgField()
    inst = c_tibrv_u32(fieldIndex)

    status = _rv.tibrvMsg_GetFieldByIndex(msg, _ctypes.byref(val), inst)
    if status == TIBRV_OK:
        ret = TibrvMsgField()
        val.castTo(ret);

    return status, ret



##
# tibrv/msg.h
# tibrv_status tibrvMsg_RemoveFieldEx(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u16           optIdentifier
#              );
#
# tibrv_status tibrvMsg_RemoveFieldInstance(
#                tibrvMsg            message,
#                const char*         fieldName,
#                tibrv_u32           instance
#              );
#
_rv.tibrvMsg_RemoveFieldEx.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_u16]
_rv.tibrvMsg_RemoveFieldEx.restype = c_tibrv_status

def tibrvMsg_RemoveField(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> tibrv_status:

    msg = c_tibrvMsg(message)
    name = _cstr(fieldName)
    id = c_tibrv_u16(int(optIdentifier))

    status = _rv.tibrvMsg_RemoveFieldEx(msg, name, id)

    return status


_rv.tibrvMsg_RemoveFieldInstance.argtypes = [c_tibrvMsg, c_tibrv_str, c_tibrv_u32]
_rv.tibrvMsg_RemoveFieldInstance.restype = c_tibrv_status

def tibrvMsg_RemoveFieldInstance(message: tibrvMsg, fieldName: str, instance: int = 0) -> tibrv_status:

    msg = c_tibrvMsg(message)
    name = _cstr(fieldName)
    inst = c_tibrv_u32(int(instance))

    status = _rv.tibrvMsg_RemoveFieldInstance(msg, name, inst)

    return status


class TibrvMsg:

    def id(self):
        return self._msg

    def __init__(self, msg: tibrvMsg = 0):
        self._err = None

        # For exist msg
        if msg != 0:
            self._copied = True
            self._msg = msg
            return

        # Create a new instance
        self._copied = False

        status, ret = tibrvMsg_Create()
        if status == TIBRV_OK:
            self._msg = ret
            return

        raise TibrvError(status)

    def __del__(self):
        if self.id() == 0 or self._copied:
            return

        status = tibrvMsg_Destroy(self.id())

    def __str__(self, codepage=None):
        if self.id() == 0:
            return None

        sz = None
        status, sz = tibrvMsg_ConvertToString(self.id(), codepage)
        self._err = TibrvStatus.error(status)

        return sz


    def detach(self) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_Detach(self.id())

        self._err = TibrvStatus.error(status)

        if status == TIBRV_OK:
            # Let __del__() to call tibrvMsg_Drstroy
            self._copied = False

        return status

    def expend(self, bytes: int ) -> tibrv_status:
        if self.id() == 0 or self._copied:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_Expand(self.id(), bytes)

        self._err = TibrvStatus.error(status)

        return status

    def bytes(self) -> int:
        ret = None
        if self.id() == 0 :
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetByteSize(self.id())

        self._err = TibrvStatus.error(status)

        return ret

    def copy(self):
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, m = tibrvMsg_CreateCopy(self.id())

            if status == TIBRV_OK:
                #msg = type(self.__class__)(n[0])
                ret = TibrvMsg(m)
                ret._copied = False

        self._err = TibrvStatus.error(status)

        return ret

    def count(self) -> int:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetNumFields(self.id())

        self._err = TibrvStatus.error(status)

        return ret

    def reset(self):
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_Reset(self.id())

        self._err = TibrvStatus.error(status)

        return

    @property
    def sendSubject(self):
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetSendSubject(self.id())

        self._err = TibrvStatus.error(status)

        return ret

    @sendSubject.setter
    def sendSubject(self, subj: str):
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_SetSendSubject(self.id(), subj)

        self._err = TibrvStatus.error(status)

    @property
    def replySubject(self):
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetReplySubject(self.id())

        self._err = TibrvStatus.error(status)

        return ret

    @replySubject.setter
    def replySubject(self, subj: str):
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_SetReplySubject(self.id(), subj)

        self._err = TibrvStatus.error(status)

    @staticmethod
    def now() -> TibrvMsgDateTime:
        ret = None
        status, ret = tibrvMsg_GetCurrentTime()

        if status != TIBRV_OK:
            ret = None
            if TibrvStatus.exception():
                raise TibrvError(status)

        return ret

    @staticmethod
    def nowString() -> (str, str):
        lct = None
        gmt = None

        status, lct, gmt = tibrvMsg_GetCurrentTimeString()
        if status != TIBRV_OK:
            if TibrvStatus.exception():
                raise TibrvError(status)

        return lct, gmt

    def addI8(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddI8(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddI8Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addU8(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddU8(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddU8Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addI16(self, name: str, value:int, id:int = 0 ) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddI16(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddI16Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addU16(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddU16(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddU16Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addI32(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddI32(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddI32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addU32(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddU32(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddU32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addI64(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddI64(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddI64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addU64(self, name: str, value:int, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddU64(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddU64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addF32(self, name: str, value:float, id:int = 0 ) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddF32(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddF32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addF64(self, name: str, value:float, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddF64(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddF64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addStr(self, name: str, value:str, id:int = 0, codepage:str=None) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddString(self.id(), name, value, id, codepage)
            else:
                status = tibrvMsg_AddStringArray(self.id(), name, value, id, codepage)

        self._err = TibrvStatus.error(status)
        return status

    def addMsg(self, name: str, value:tibrvMsg, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_AddMsg(self.id(), name, value, id)
            else:
                status = tibrvMsg_AddMsgArray(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addDateTime(self, name: str, value:TibrvMsgDateTime, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_AddDateTime(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def addField(self, field:TibrvMsgField) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_AddField(self.id(), field)

        self._err = TibrvStatus.error(status)
        return status

    def setI8(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateI8(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateI8Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setU8(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateU8(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateU8Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setI16(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateI16(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateI16Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setU16(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateU16(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateU16Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setI32(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateI32(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateI32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setU32(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateU32(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateU32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setI64(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateI64(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateI64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setU64(self, name: str, value:int, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateU64(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateU64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setF32(self, name: str, value:float, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateF32(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateF32Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setF64(self, name: str, value:float, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateF64(self.id(), name, value, id)
            else:
                status = tibrvMsg_UpdateF64Array(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setStr(self, name: str, value:str, id: int = 0,codepage:str=None) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            if type(value) is not list:
                status = tibrvMsg_UpdateString(self.id(), name, value, id, codepage)
            else:
                status = tibrvMsg_UpdateStringArray(self.id(), name, value, id, codepage)

        self._err = TibrvStatus.error(status)
        return status

    def setMsg(self, name: str, value, id: int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        elif value is None:
            status = tibrvMsg_UpdateMsg(self.id(), name, None, id)
        elif type(value) is not list:
            if type(value) is not TibrvMsg:
                status = TIBRV_INVALID_ARG
            else:
                status = tibrvMsg_UpdateMsg(self.id(), name, value.id(), id)
        else:
            msg = []
            for x in value:
                if type(x) is not TibrvMsg:
                    return TIBRV_INVALID_ARG
                msg.append(x.id())

            status = tibrvMsg_UpdateMsgArray(self.id(), name, msg, id)

        self._err = TibrvStatus.error(status)
        return status

    def setDateTime(self, name: str, value:TibrvMsgDateTime, id:int = 0) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_UpdateDateTime(self.id(), name, value, id)

        self._err = TibrvStatus.error(status)
        return status

    def setField(self, field:TibrvMsgField) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status = tibrvMsg_UpdateField(self.id(), field)

        self._err = TibrvStatus.error(status)
        return status

    def __default(self, val, status, kwargs):
        if status == TIBRV_NOT_FOUND:
            if 'default' in kwargs:
                self._err = TibrvError(status)
                return kwargs['default']

        self._err = TibrvStatus.error(status)

        return val

    def getI8(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI8(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def getU8(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU8(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getI16(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI16(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def getU16(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU16(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def getI32(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI32(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def getU32(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU32(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getI64(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI64(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getU64(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU64(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getF32(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0.0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetF32(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getF64(self, name: str, id: int = 0, **kwargs) -> int:

        ret = 0.0

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetF64(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getStr(self, name: str, id: int = 0, codepage:str=None, **kwargs) -> int:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetString(self.id(), name, id, codepage)

        return self.__default(ret, status, kwargs)


    def getMsg(self, name: str, id: int = 0, **kwargs) -> int:

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status,m = tibrvMsg_GetMsg(self.id(), name, id)

            if status == TIBRV_OK:
                #msg = type(self.__class__)(n[0])
                ret = TibrvMsg(m)

        return self.__default(ret, status, kwargs)


    def getDateTime(self, name: str, id: int = 0, **kwargs) -> TibrvMsgDateTime:

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetDateTime(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getField(self, name: str, id: int = 0, **kwargs) -> TibrvMsgField:

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetField(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def getByIndex(self, index: int, **kwargs):

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetFieldByIndex(self.id(), index)

        return self.__default(ret, status, kwargs)

    def getInstance(self, name:str, instance: int, **kwargs):

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetFieldInstance(self.id(), name, instance)

        return self.__default(ret, status, kwargs)


    def listI8(self, name: str, id: int = 0, **kwargs) -> list:

        ret = []

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI8Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def listU8(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU8Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listI16(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI16Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def listU16(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU16Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def listI32(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI32Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)

    def listU32(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU32Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listI64(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetI64Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listU64(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetU64Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listF32(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetF32Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listF64(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None

        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetF64Array(self.id(), name, id)

        return self.__default(ret, status, kwargs)


    def listStr(self, name: str, id: int = 0, codepage:str=None, **kwargs) -> list:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, ret = tibrvMsg_GetStringArray(self.id(), name, id, codepage)

        return self.__default(ret, status, kwargs)


    def listMsg(self, name: str, id: int = 0, **kwargs) -> list:

        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_MSG
        else:
            status, msg = tibrvMsg_GetMsgArray(self.id(), name, id)

            if status == TIBRV_OK:
                ret = []
                for x in msg:
                    ret.append(TibrvMsg(x))

        return self.__default(ret, status, kwargs)


    def add(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
            if TibrvStatus.exception():
                raise self._err
            return None

        if data_type is tibrv_i8:
            return self.addI8(name, id, **kwargs)

        if data_type is tibrv_u8:
            return self.addU8(name, id, **kwargs)

        if data_type is tibrv_i16:
            return self.addI16(name, id, **kwargs)

        if data_type is tibrv_u16:
            return self.addU16(name, id, **kwargs)

        if data_type is tibrv_i32:
            return self.addI32(name, id, **kwargs)

        if data_type is tibrv_u32:
            return self.addU32(name, id, **kwargs)

        if data_type is tibrv_i64:
            return self.addI64(name, id, **kwargs)

        if data_type is tibrv_u64:
            return self.addU64(name, id, **kwargs)

        if data_type is tibrv_f32:
            return self.addF32(name, id, **kwargs)

        if data_type is tibrv_f64:
            return self.addF64(name, id, **kwargs)

        if data_type is tibrv_str:
            return self.addStr(name, id, **kwargs)

        # TibrvMsg
        if data_type is TibrvMsg or TibrvMsg in data_type.__bases__:
            return self.addMsg(name, id, **kwargs)

        # TibrvMsgDateTime
        if data_type is TibrvMsgDateTime or TibrvMsgDateTime in data_type.__bases__:
            return self.addDateTime(name, id, **kwargs)

        # TibrvMsgField
        if data_type is TibrvMsgField or TibrvMsgField in data_type.__bases__:
            return self.addField(name, id, **kwargs)

        self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')
        if TibrvStatus.exception():
            raise self._err

        return None


    def set(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
            if TibrvStatus.exception():
                raise self._err
            return None

        if data_type is tibrv_i8:
            return self.setI8(name, id, **kwargs)

        if data_type is tibrv_u8:
            return self.setU8(name, id, **kwargs)

        if data_type is tibrv_i16:
            return self.setI16(name, id, **kwargs)

        if data_type is tibrv_u16:
            return self.setU16(name, id, **kwargs)

        if data_type is tibrv_i32:
            return self.setI32(name, id, **kwargs)

        if data_type is tibrv_u32:
            return self.setU32(name, id, **kwargs)

        if data_type is tibrv_i64:
            return self.setI64(name, id, **kwargs)

        if data_type is tibrv_u64:
            return self.setU64(name, id, **kwargs)

        if data_type is tibrv_f32:
            return self.setF32(name, id, **kwargs)

        if data_type is tibrv_f64:
            return self.setF64(name, id, **kwargs)

        if data_type is tibrv_str:
            return self.setStr(name, id, **kwargs)

        # TibrvMsg
        if data_type is TibrvMsg or TibrvMsg in data_type.__bases__:
            return self.setMsg(name, id, **kwargs)

        # TibrvMsgDateTime
        if data_type is TibrvMsgDateTime or TibrvMsgDateTime in data_type.__bases__:
            return self.setDateTime(name, id, **kwargs)

        # TibrvMsgField
        if data_type is TibrvMsgField or TibrvMsgField in data_type.__bases__:
            return self.setField(name, id, **kwargs)

        self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')
        if TibrvStatus.exception():
            raise self._err

        return None

    def get(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
            if TibrvStatus.exception():
                raise self._err
            return None

        if data_type is tibrv_i8:
            return self.getI8(name, id, **kwargs)

        if data_type is tibrv_u8:
            return self.getU8(name, id, **kwargs)

        if data_type is tibrv_i16:
            return self.getI16(name, id, **kwargs)

        if data_type is tibrv_u16:
            return self.getU16(name, id, **kwargs)

        if data_type is tibrv_i32:
            return self.getI32(name, id, **kwargs)

        if data_type is tibrv_u32:
            return self.getU32(name, id, **kwargs)

        if data_type is tibrv_i64:
            return self.getI64(name, id, **kwargs)

        if data_type is tibrv_u64:
            return self.getU64(name, id, **kwargs)

        if data_type is tibrv_f32:
            return self.getF32(name, id, **kwargs)

        if data_type is tibrv_f64:
            return self.getF64(name, id, **kwargs)

        if data_type is tibrv_str:
            return self.getStr(name, id, **kwargs)

        # TibrvMsg
        if data_type is TibrvMsg or TibrvMsg in data_type.__bases__:
            return self.getMsg(name, id, **kwargs)

        # TibrvMsgDateTime
        if data_type is TibrvMsgDateTime or TibrvMsgDateTime in data_type.__bases__:
            return self.getDateTime(name, id, **kwargs)

        # TibrvMsgField
        if data_type is TibrvMsgField or TibrvMsgField in data_type.__bases__:
            return self.getField(name, id, **kwargs)

        self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')
        if TibrvStatus.exception():
            raise self._err

        return None


    def list(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
            if TibrvStatus.exception():
                raise self._err
            return None

        if data_type is tibrv_i8:
            return self.listI8(name, id, **kwargs)

        if data_type is tibrv_u8:
            return self.listU8(name, id, **kwargs)

        if data_type is tibrv_i16:
            return self.listI16(name, id, **kwargs)

        if data_type is tibrv_u16:
            return self.listU16(name, id, **kwargs)

        if data_type is tibrv_i32:
            return self.listI32(name, id, **kwargs)

        if data_type is tibrv_u32:
            return self.listU32(name, id, **kwargs)

        if data_type is tibrv_i64:
            return self.listI64(name, id, **kwargs)

        if data_type is tibrv_u64:
            return self.listU64(name, id, **kwargs)

        if data_type is tibrv_f32:
            return self.listF32(name, id, **kwargs)

        if data_type is tibrv_f64:
            return self.listF64(name, id, **kwargs)

        if data_type is tibrv_str:
            return self.listStr(name, id, **kwargs)

        # TibrvMsg
        if data_type is TibrvMsg or TibrvMsg in data_type.__bases__:
            return self.listMsg(name, id, **kwargs)

        # TibrvMsgDateTime, TibrvMsgField
        # array not supported in TIBRV/C

        self._err = TibrvError(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')
        if TibrvStatus.exception():
            raise self._err

        return None


    def __getitem__(self, item):
        # Get By Index
        if type(item) is int:
            if item < 0:
                status = TIBRV_INVALID_ARG
                self._err = TibrvStatus.error(status)
                return None

            ret = None
            status, ret = tibrvMsg_GetFieldByIndex(self.id(), item)

            self._err = TibrvStatus.error(status)

            return ret

        # Get By Name
        if type(item) is str:
            if item is None:
                status = TIBRV_INVALID_ARG
                self._err = TibrvStatus.error(status)
                return None

            ret = None
            status, ret = tibrvMsg_GetField(self.id(), item)

            self._err = TibrvStatus.error(status)

            return ret

        # Unknown
        status = TIBRV_INVALID_ARG
        self._err = TibrvStatus.error(status)
        return None

    def __setitem__(self, key, value):

        if type(value) is int:
            status = tibrvMsg_UpdateI64(self.id(), key, value)
            self._err = TibrvStatus.error(status)
            return

        if type(value) is float:
            status = tibrvMsg_UpdateF64(self.id(), key, value)
            self._err = TibrvStatus.error(status)
            return

        if type(value) is str:
            status = tibrvMsg_UpdateString(self.id(), key, value)
            self._err = TibrvStatus.error(status)
            return

        if isinstance(value, TibrvMsgDateTime):
            status = tibrvMsg_UpdateDateTime(self.id(), key, value)
            self._err = TibrvStatus.error(status)
            return

        if isinstance(value, TibrvMsg):
            status = tibrvMsg_UpdateMsg(self.id(), key, value)
            self._err = TibrvStatus.error(status)
            return

        # TODO more format??
        status = TIBRV_INVALID_ARG
        self._err = TibrvStatus.error(status)
        return

    @property
    def error(self) -> TibrvError:
        return self._err

