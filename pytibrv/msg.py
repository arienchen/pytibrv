##
# pytibrv/msg.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.1 20170220 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
# 1. Data Type
#    API NOT SUPPORT
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
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------
# 20170220 V1.1 ARIEN arien.chen@gmail.com
#   REMOVE TIBRV C Header
#
# 20161211 ARIEN V1.0
#   CREATED
#

import ctypes as _ctypes

from .types import tibrv_status, tibrvMsg, tibrvMsgDateTime, tibrvMsgField, tibrvEvent,\
                   TIBRVMSG_I8, TIBRVMSG_U8, TIBRVMSG_I16, TIBRVMSG_U16, \
                   TIBRVMSG_I32, TIBRVMSG_U32, TIBRVMSG_I64, TIBRVMSG_U64, \
                   TIBRVMSG_F32, TIBRVMSG_F64, TIBRVMSG_STRING, TIBRVMSG_MSG, \
                   TIBRVMSG_DATETIME, \
                   TIBRVMSG_DATETIME_STRING_SIZE

from .status import TIBRV_OK, TIBRV_INVALID_ARG, TIBRV_INVALID_MSG

from .api import _rv, _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvMsg, _c_tibrvEvent, _c_tibrv_bool, \
                 _c_tibrv_i8, _c_tibrv_u8, _c_tibrv_i16, _c_tibrv_u16, \
                 _c_tibrv_i32, _c_tibrv_u32, _c_tibrv_i64, _c_tibrv_u64, \
                 _c_tibrv_f32, _c_tibrv_f64, _c_tibrv_str,\
                 _c_tibrv_ipport16, _c_tibrv_ipaddr32, \
                 _c_tibrv_i8_p, _c_tibrv_u8_p, _c_tibrv_i16_p, _c_tibrv_u16_p, \
                 _c_tibrv_i32_p, _c_tibrv_u32_p, _c_tibrv_i64_p, _c_tibrv_u64_p, \
                 _c_tibrv_f32_p, _c_tibrv_f64_p, _c_tibrv_str_p, _c_tibrvMsg_p


class _c_tibrvMsgDateTime(_ctypes.Structure):
    _fields_ = [("sec", _c_tibrv_i64),
                ("nsec", _c_tibrv_u32)]

    def __init__(self, dt: tibrvMsgDateTime = None):
        if dt is None:
            return

        self.sec = dt.sec
        self.nsec = dt.nsec

    def castTo(self, dt: tibrvMsgDateTime):
        if dt is None:
            return
        dt.sec = self.sec
        dt.nsec = self.nsec


class _c_tibrvLocalData(_ctypes.Union):
    _fields_ = [("msg", _c_tibrvMsg),
                ("str", _c_tibrv_str),
                ("buf", _ctypes.c_void_p),
                ("array", _ctypes.c_void_p),
                ("boolean", _c_tibrv_bool),
                ("i8", _c_tibrv_i8),
                ("u8", _c_tibrv_u8),
                ("i16", _c_tibrv_i16),
                ("u16", _c_tibrv_u16),
                ("i32", _c_tibrv_i32),
                ("u32", _c_tibrv_u32),
                ("i64", _c_tibrv_i64),
                ("u64", _c_tibrv_u64),
                ("f32", _c_tibrv_f32),
                ("f64", _c_tibrv_f64),
                ("ipport16", _c_tibrv_ipport16),
                ("ipaddr32", _c_tibrv_ipaddr32),
                ("date", _c_tibrvMsgDateTime)]


class _c_tibrvMsgField(_ctypes.Structure):
    _fields_ = [("name", _c_tibrv_str),
                ("size", _c_tibrv_u32),
                ("count", _c_tibrv_u32),
                ("data", _c_tibrvLocalData),
                ("id", _c_tibrv_u16),
                ("type", _c_tibrv_u8)]

    def __init__(self, fld: tibrvMsgField = None):

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

    def castTo(self, obj: tibrvMsgField, codepage= None):

        obj._name = _pystr(self.name)
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
            # obj.str/setter will assign obj._size = len()
            # it is str length, not bytes
            # len('ABC中文') -> 5 UTF char, bytes = 10
            obj.str = _pystr(self.data.str, codepage)
            return

        if obj.type == TIBRVMSG_MSG:
            # NOW return tibrvMsg = int
            obj.msg = self.data.msg
            return

        if obj.type == TIBRVMSG_DATETIME:
            dt = tibrvMsgDateTime()
            dt.sec = self.data.date.sec.value
            dt.nsec = self.date.date.nsec.value
            obj.data = dt
            return

        # TODO array


##-----------------------------------------------------------------------------
# TIBRV API : tibrv/msg.h
##-----------------------------------------------------------------------------

##
_rv.tibrvMsg_Create.argtypes = [_ctypes.POINTER(_c_tibrvMsg)]
_rv.tibrvMsg_Create.restype = _c_tibrv_status

_rv.tibrvMsg_CreateEx.argtypes = [_ctypes.POINTER(_c_tibrvMsg), _c_tibrv_u32]
_rv.tibrvMsg_CreateEx.restype = _c_tibrv_status

def tibrvMsg_Create(initialStorage: int=0) -> (tibrv_status, tibrvMsg):

    msg = _c_tibrvMsg(0)

    if initialStorage == 0:
        status = _rv.tibrvMsg_Create(_ctypes.byref(msg))
    else:
        try:
            n = _c_tibrv_u32(initialStorage)
        except:
            return TIBRV_INVALID_ARG, None

        status = _rv.tibrvMsg_CreateEx(_ctypes.byref(msg), n)

    return status, msg.value


##
_rv.tibrvMsg_Destroy.argtypes = [_c_tibrvMsg]
_rv.tibrvMsg_Destroy.restype = _c_tibrv_status

def tibrvMsg_Destroy(message: tibrvMsg) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rv.tibrvMsg_Destroy(msg)

    return status


##
_rv.tibrvMsg_Detach.argtypes = [_c_tibrvMsg]
_rv.tibrvMsg_Detach.restype = _c_tibrv_status

def tibrvMsg_Detach(message: tibrvMsg) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rv.tibrvMsg_Detach(msg)

    return status


##
_rv.tibrvMsg_CreateCopy.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrvMsg)]
_rv.tibrvMsg_CreateCopy.restype = _c_tibrv_status

def tibrvMsg_CreateCopy(message: tibrvMsg) -> (tibrv_status, tibrvMsg):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    cc  = _c_tibrvMsg(0)

    status = _rv.tibrvMsg_CreateCopy(msg, _ctypes.byref(cc))

    return status, cc.value


##
_rv.tibrvMsg_Reset.argtypes = [_c_tibrvMsg]
_rv.tibrvMsg_Reset.restype = _c_tibrv_status

def tibrvMsg_Reset(message: tibrvMsg) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rv.tibrvMsg_Reset(msg)

    return status


##
_rv.tibrvMsg_Expand.argtypes = [_c_tibrvMsg, _c_tibrv_i32]
_rv.tibrvMsg_Expand.restype = _c_tibrv_status

def tibrvMsg_Expand(message: tibrvMsg, additionalStorage: int) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if additionalStorage is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        n = _c_tibrv_u32(additionalStorage)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_Expand(msg, n)

    return status


##
_rv.tibrvMsg_SetSendSubject.argtypes = [_c_tibrvMsg, _c_tibrv_str]
_rv.tibrvMsg_SetSendSubject.restype = _c_tibrv_status

def tibrvMsg_SetSendSubject(message:tibrvMsg, subject: str) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        sz = _cstr(subject)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_SetSendSubject(msg, sz)

    return status


##
_rv.tibrvMsg_GetSendSubject.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_str)]
_rv.tibrvMsg_GetSendSubject.restype = _c_tibrv_status

def tibrvMsg_GetSendSubject(message: tibrvMsg) -> (tibrv_status, str):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    sz = _c_tibrv_str(0)
    status = _rv.tibrvMsg_GetSendSubject(msg, _ctypes.byref(sz))

    return status, _pystr(sz)


##
_rv.tibrvMsg_SetReplySubject.argtypes = [_c_tibrvMsg, _c_tibrv_str]
_rv.tibrvMsg_SetReplySubject.restype = _c_tibrv_status

def tibrvMsg_SetReplySubject(message: tibrvMsg, subject: str) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if subject is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        sz = _cstr(subject)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_SetReplySubject(msg, sz)

    return status

##
_rv.tibrvMsg_GetReplySubject.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_str)]
_rv.tibrvMsg_GetReplySubject.restype = _c_tibrv_status

def tibrvMsg_GetReplySubject(message: tibrvMsg) -> (tibrv_status, str):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    sz = _c_tibrv_str()
    status = _rv.tibrvMsg_GetReplySubject(msg, _ctypes.byref(sz))

    return status, _pystr(sz)


##
_rv.tibrvMsg_GetEvent.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrvEvent)]
_rv.tibrvMsg_GetEvent.restype = _c_tibrv_status

def tibrvMsg_GetEvent(message: tibrvMsg) -> (tibrv_status, tibrvEvent):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    n = _c_tibrvEvent(0)

    status = _rv.tibrvMsg_GetEvent(msg, _ctypes.byref(n))

    return status, n.value


##
_rv.tibrvMsg_GetClosure.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_ctypes.py_object)]
_rv.tibrvMsg_GetClosure.restype = _c_tibrv_status

def tibrvMsg_GetClosure(message: tibrvMsg) -> (tibrv_status, object):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None
    cz = _ctypes.py_object
    status = _rv.tibrvMsg_GetClosure(msg, _ctypes.byref(cz))

    # cast to Python Object
    if status == TIBRV_OK:
        ret = _ctypes.cast(cz, _ctypes.py_object).value

    return status, ret

##
_rv.tibrvMsg_GetNumFields.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvMsg_GetNumFields.restype = _c_tibrv_status

def tibrvMsg_GetNumFields(message: tibrvMsg) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    n = _c_tibrv_u32(0)
    status = _rv.tibrvMsg_GetNumFields(msg, _ctypes.byref(n))

    return status, n.value


##
_rv.tibrvMsg_GetByteSize.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvMsg_GetByteSize.restype = _c_tibrv_status

def tibrvMsg_GetByteSize(message: tibrvMsg) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    n = _c_tibrv_u32(0)
    status = _rv.tibrvMsg_GetByteSize(msg, _ctypes.byref(n))

    return status, n.value


##
_rv.tibrvMsg_ConvertToString.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_str)]
_rv.tibrvMsg_ConvertToString.restype = _c_tibrv_status

def tibrvMsg_ConvertToString(message: tibrvMsg, codepage: str=None) -> (tibrv_status, str):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    sz = _c_tibrv_str()
    status = _rv.tibrvMsg_ConvertToString(msg, _ctypes.byref(sz))

    return status, _pystr(sz, codepage)


##
_rv.tibrvMsg_GetCurrentTime.argtypes = [_ctypes.POINTER(_c_tibrvMsgDateTime)]
_rv.tibrvMsg_GetCurrentTime.restype = _c_tibrv_status

def tibrvMsg_GetCurrentTime() -> (tibrv_status, tibrvMsgDateTime):

    ret = None

    dt = _c_tibrvMsgDateTime()
    status = _rv.tibrvMsg_GetCurrentTime(_ctypes.byref(dt))

    if status == TIBRV_OK:
        ret = tibrvMsgDateTime()
        dt.castTo(ret)

    return status, ret


_rv.tibrvMsg_GetCurrentTimeString.argtypes = [_c_tibrv_str, _c_tibrv_str]
_rv.tibrvMsg_GetCurrentTimeString.restype = _c_tibrv_status

def tibrvMsg_GetCurrentTimeString() -> (tibrv_status, str, str):

    local_time = _ctypes.create_string_buffer(TIBRVMSG_DATETIME_STRING_SIZE)
    gmt_time = _ctypes.create_string_buffer(TIBRVMSG_DATETIME_STRING_SIZE)

    status = _rv.tibrvMsg_GetCurrentTimeString(local_time, gmt_time)

    if status != TIBRV_OK:
        return status, None, None

    return TIBRV_OK, _pystr(local_time), _pystr(gmt_time)


##
_rv.tibrvMsg_AddDateTimeEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrvMsgDateTime),
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddDateTimeEx.restype = _c_tibrv_status

def tibrvMsg_AddDateTime(message: tibrvMsg, fieldName: str, value: tibrvMsgDateTime,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    if value is not None and type(value) is not tibrvMsgDateTime:
        return TIBRV_INVALID_ARG

    try:
        name = _cstr(fieldName)
        dt = _c_tibrvMsgDateTime(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddDateTimeEx(msg, name, _ctypes.byref(dt), id)

    return status


_rv.tibrvMsg_UpdateDateTimeEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _ctypes.POINTER(_c_tibrvMsgDateTime),
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateDateTimeEx.restype = _c_tibrv_status

def tibrvMsg_UpdateDateTime(message: tibrvMsg, fieldName: str, value: tibrvMsgDateTime,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    if value is not None and type(value) is not tibrvMsgDateTime:
        return TIBRV_INVALID_ARG

    try:
        name = _cstr(fieldName)
        dt = _c_tibrvMsgDateTime(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateDateTimeEx(msg, name, _ctypes.byref(dt), id)

    return status


_rv.tibrvMsg_GetDateTimeEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrvMsgDateTime),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetDateTimeEx.restype = _c_tibrv_status

def tibrvMsg_GetDateTime(message: tibrvMsg, fieldName: str,
                         optIdentifier: int = 0) -> (tibrv_status, tibrvMsgDateTime):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrvMsgDateTime()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetDateTimeEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = tibrvMsgDateTime()
        val.castTo(ret)

    return status, ret


##
_rv.tibrvMsg_AddBoolEx.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_bool, _c_tibrv_u16]
_rv.tibrvMsg_AddBoolEx.restype = _c_tibrv_status

def tibrvMsg_AddBool(message: tibrvMsg, fieldName: str, value: bool, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_bool(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddBoolEx(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateBoolEx.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_bool, _c_tibrv_u16]
_rv.tibrvMsg_UpdateBoolEx.restype = _c_tibrv_status

def tibrvMsg_UpdateBool(message: tibrvMsg, fieldName: str, value: bool, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_bool(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateBoolEx(msg, name, val, id)

    return status


_rv.tibrvMsg_GetBoolEx.argtypes = [_c_tibrvMsg,
                                   _c_tibrv_str,
                                   _ctypes.POINTER(_c_tibrv_bool),
                                   _c_tibrv_u16]

_rv.tibrvMsg_GetBoolEx.restype = _c_tibrv_status

def tibrvMsg_GetBool(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, bool):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_bool()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetBoolEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


##
_rv.tibrvMsg_AddI8Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i8, _c_tibrv_u16]
_rv.tibrvMsg_AddI8Ex.restype = _c_tibrv_status

def tibrvMsg_AddI8(message: tibrvMsg, fieldName: str, value: int, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i8(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI8Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateI8Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i8, _c_tibrv_u16]
_rv.tibrvMsg_UpdateI8Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateI8(message: tibrvMsg, fieldName: str, value: int, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i8(int(value))
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI8Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetI8Ex.argtypes = [_c_tibrvMsg,
                                 _c_tibrv_str,
                                 _ctypes.POINTER(_c_tibrv_i8),
                                 _c_tibrv_u16]

_rv.tibrvMsg_GetI8Ex.restype = _c_tibrv_status

def tibrvMsg_GetI8(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i8()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI8Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI8ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _c_tibrv_i8_p,
                                      _c_tibrv_u32,
                                      _c_tibrv_u16]

_rv.tibrvMsg_AddI8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddI8Array(message: tibrvMsg, fieldName: str, value: list,
                        optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddI8ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i8 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI8ArrayEx.argtypes = [_c_tibrvMsg,
                                         _c_tibrv_str,
                                         _c_tibrv_i8_p,
                                         _c_tibrv_u32,
                                         _c_tibrv_u16]

_rv.tibrvMsg_UpdateI8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateI8Array(message: tibrvMsg, fieldName: str, value: list,
                           optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateI8ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i8 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI8ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _ctypes.POINTER(_c_tibrv_i8_p),
                                      _ctypes.POINTER(_c_tibrv_u32),
                                      _c_tibrv_u16]

_rv.tibrvMsg_GetI8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetI8Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i8_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI8ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddU8Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u8, _c_tibrv_u16]
_rv.tibrvMsg_AddU8Ex.restype = _c_tibrv_status

def tibrvMsg_AddU8(message: tibrvMsg, fieldName: str, value: int,
                   optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u8(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU8Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU8Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u8, _c_tibrv_u16]
_rv.tibrvMsg_UpdateU8Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateU8(message: tibrvMsg, fieldName: str, value: int,
                      optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u8(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU8Ex(msg, name, val, id)

    return status

_rv.tibrvMsg_GetU8Ex.argtypes = [_c_tibrvMsg,
                                 _c_tibrv_str,
                                 _ctypes.POINTER(_c_tibrv_u8),
                                 _c_tibrv_u16]

_rv.tibrvMsg_GetU8Ex.restype = _c_tibrv_status

def tibrvMsg_GetU8(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u8()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU8Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU8ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _c_tibrv_u8_p,
                                      _c_tibrv_u32,
                                      _c_tibrv_u16]

_rv.tibrvMsg_AddU8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddU8Array(message: tibrvMsg, fieldName: str, value: list,
                        optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddU8ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u8 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU8ArrayEx.argtypes = [_c_tibrvMsg,
                                         _c_tibrv_str,
                                         _c_tibrv_u8_p,
                                         _c_tibrv_u32,
                                         _c_tibrv_u16]

_rv.tibrvMsg_UpdateU8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateU8Array(message:tibrvMsg, fieldName: str, value: list,
                           optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateU8ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u8 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU8ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU8ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _ctypes.POINTER(_c_tibrv_u8_p),
                                      _ctypes.POINTER(_c_tibrv_u32),
                                      _c_tibrv_u16]

_rv.tibrvMsg_GetU8ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetU8Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u8_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU8ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddI16Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i16, _c_tibrv_u16]
_rv.tibrvMsg_AddI16Ex.restype = _c_tibrv_status

def tibrvMsg_AddI16(message: tibrvMsg, fieldName: str, value: int, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i16(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateI16Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i16, _c_tibrv_u16]
_rv.tibrvMsg_UpdateI16Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateI16(message: tibrvMsg, fieldName: str, value: int, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i16(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetI16Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_i16),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetI16Ex.restype = _c_tibrv_status

def tibrvMsg_GetI16(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i16(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI16Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI16ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_i16_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddI16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddI16Array(message: tibrvMsg, fieldName: str, value: list, optIdentifier: int = 0) \
                        -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddI16ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i16 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI16ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_i16_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateI16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateI16Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateI16ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i16 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI16ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _ctypes.POINTER(_c_tibrv_i16_p),
                                      _ctypes.POINTER(_c_tibrv_u32),
                                      _c_tibrv_u16]

_rv.tibrvMsg_GetI16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetI16Array(message: tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):


    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i16_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI16ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddU16Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u16, _c_tibrv_u16]
_rv.tibrvMsg_AddU16Ex.restype = _c_tibrv_status

def tibrvMsg_AddU16(message: tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u16(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU16Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u16, _c_tibrv_u16]
_rv.tibrvMsg_UpdateU16Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateU16(message: tibrvMsg, fieldName: str, value: int,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u16(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU16Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetU16Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_u16),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetU16Ex.restype = _c_tibrv_status

def tibrvMsg_GetU16(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u16(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU16Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU16ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_u16_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddU16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddU16Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddU16ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u16 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU16ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_u16_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateU16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateU16Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0)  -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateU16ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u16 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU16ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU16ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_u16_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetU16ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetU16Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u16_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU16ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddI32Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i32, _c_tibrv_u16]
_rv.tibrvMsg_AddI32Ex.restype = _c_tibrv_status

def tibrvMsg_AddI32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i32(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateI32Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_i32, _c_tibrv_u16]
_rv.tibrvMsg_UpdateI32Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateI32(message:tibrvMsg, fieldName:str, value:int, optIdentifier:int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i32(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetI32Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_i32),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetI32Ex.restype = _c_tibrv_status

def tibrvMsg_GetI32(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI32ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_i32_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddI32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddI32Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:


    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddI32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI32ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_i32_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateI32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateI32Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateI32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI32ArrayEx.argtypes = [_c_tibrvMsg,
                                      _c_tibrv_str,
                                      _ctypes.POINTER(_c_tibrv_i32_p),
                                      _ctypes.POINTER(_c_tibrv_u32),
                                      _c_tibrv_u16]

_rv.tibrvMsg_GetI32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetI32Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i32_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddU32Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u32, _c_tibrv_u16]
_rv.tibrvMsg_AddU32Ex.restype = _c_tibrv_status

def tibrvMsg_AddU32(message: tibrvMsg, fieldName: str, value: int,
                    optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u32(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU32Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u32, _c_tibrv_u16]
_rv.tibrvMsg_UpdateU32Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateU32(message: tibrvMsg, fieldName: str, value: int,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u32(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetU32Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_u32),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetU32Ex.restype = _c_tibrv_status

def tibrvMsg_GetU32(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u32()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU32ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_u32_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddU32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddU32Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddU32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_ctypes.c_uint32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU32ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_u32_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateU32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateU32Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateU32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_ctypes.c_uint32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU32ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_u32_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetU32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetU32Array(message:tibrvMsg, fieldName:str, optIdentifier:int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u32_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddI64Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _c_tibrv_i64,
                                  _c_tibrv_u16]

_rv.tibrvMsg_AddI64Ex.restype = _c_tibrv_status

def tibrvMsg_AddI64(message:tibrvMsg, fieldName: str, value: int, optIdentifier:int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateI64Ex.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _c_tibrv_i64,
                                     _c_tibrv_u16]

_rv.tibrvMsg_UpdateI64Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateI64(message: tibrvMsg, fieldName: str, value: int,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetI64Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_i64),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetI64Ex.restype = _c_tibrv_status

def tibrvMsg_GetI64(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i64(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddI64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_i64_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddI64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddI64Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddI64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddI64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateI64ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_i64_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateI64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateI64Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateI64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_i64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateI64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetI64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_i64_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetI64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetI64Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_i64_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetI64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddU64Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u64, _c_tibrv_u16]
_rv.tibrvMsg_AddU64Ex.restype = _c_tibrv_status

def tibrvMsg_AddU64(message: tibrvMsg, fieldName: str, value: int, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateU64Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u64, _c_tibrv_u16]
_rv.tibrvMsg_UpdateU64Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateU64(message: tibrvMsg, fieldName: str, value: int,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetU64Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_u64),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetU64Ex.restype = _c_tibrv_status

def tibrvMsg_GetU64(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, int):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u64()
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddU64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_u64_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddU64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddU64Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddU64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddU64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateU64ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_u64_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateU64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateU64Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateU64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_u64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateU64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetU64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_u64_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetU64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetU64Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_u64_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetU64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddF32Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _c_tibrv_f32,
                                  _c_tibrv_u16]

_rv.tibrvMsg_AddF32Ex.restype = _c_tibrv_status

def tibrvMsg_AddF32(message: tibrvMsg, fieldName: str, value: float,
                    optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f32(value)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateF32Ex.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _c_tibrv_f32,
                                     _c_tibrv_u16]

_rv.tibrvMsg_UpdateF32Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateF32(message: tibrvMsg, fieldName: str, value: float,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f32(value)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF32Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetF32Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_f32),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetF32Ex.restype = _c_tibrv_status

def tibrvMsg_GetF32(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, float):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f32(0.0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetF32Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddF32ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_f32_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddF32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddF32Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddF32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_f32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateF32ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_f32_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateF32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateF32Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateF32ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_f32 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF32ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetF32ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_f32_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetF32ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetF32Array(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f32_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetF32ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddF64Ex.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_f64, _c_tibrv_u16]
_rv.tibrvMsg_AddF64Ex.restype = _c_tibrv_status

def tibrvMsg_AddF64(message: tibrvMsg, fieldName: str, value: float,
                    optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateF64Ex.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _c_tibrv_f64,
                                     _c_tibrv_u16]

_rv.tibrvMsg_UpdateF64Ex.restype = _c_tibrv_status

def tibrvMsg_UpdateF64(message: tibrvMsg, fieldName: str, value: float,
                       optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f64(value)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF64Ex(msg, name, val, id)

    return status


_rv.tibrvMsg_GetF64Ex.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrv_f64),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetF64Ex.restype = _c_tibrv_status

def tibrvMsg_GetF64(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, float):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f64(0.0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetF64Ex(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddF64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrv_f64_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddU64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddF64Array(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddF64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_f64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddF64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateF64ArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_f64_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateF64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateF64Array(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateF64ArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_f64 * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateF64ArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetF64ArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrv_f64_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetF64ArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetF64Array(message: tibrvMsg, fieldName: str,
                         optIdentifier: int = 0)  -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_f64_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetF64ArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddStringEx.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _c_tibrv_str,
                                     _c_tibrv_u16]

_rv.tibrvMsg_AddStringEx.restype = _c_tibrv_status

def tibrvMsg_AddString(message: tibrvMsg, fieldName: str, value: str,
                       optIdentifier: int = 0, codepage: str = None) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _cstr(value, codepage)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddStringEx(msg, name, val, id)

    return status


_rv.tibrvMsg_UpdateStringEx.argtypes = [_c_tibrvMsg,
                                        _c_tibrv_str,
                                        _c_tibrv_str,
                                        _c_tibrv_u16]

_rv.tibrvMsg_UpdateStringEx.restype = _c_tibrv_status

def tibrvMsg_UpdateString(message: tibrvMsg, fieldName: str, value: str,
                          optIdentifier: int = 0, codepage: str = None) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        val = _cstr(value, codepage)
        id = _c_tibrv_u16(optIdentifier)

    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateStringEx(msg, name, val, id)

    return status


_rv.tibrvMsg_GetStringEx.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _ctypes.POINTER(_c_tibrv_str),
                                     _c_tibrv_u16]

_rv.tibrvMsg_GetStringEx.restype = _c_tibrv_status

def tibrvMsg_GetString(message: tibrvMsg, fieldName: str, optIdentifier: int = 0,
                       codepage: str = None) -> (tibrv_status, str):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_str(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetStringEx(msg, name, _ctypes.byref(val), id)

    if status == TIBRV_OK:
        ret = _pystr(val, codepage)

    return status, ret


_rv.tibrvMsg_AddStringArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrv_str_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_AddStringArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddStringArray(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0, codepage: str = None) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddStringArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_str * n)()
        for x in range(n):
            val[x] = _cstr(value[x], codepage)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddStringArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateStringArrayEx.argtypes = [_c_tibrvMsg,
                                             _c_tibrv_str,
                                             _c_tibrv_str_p,
                                             _c_tibrv_u32,
                                             _c_tibrv_u16]

_rv.tibrvMsg_UpdateStringArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateStringArray(message: tibrvMsg, fieldName: str, value: list,
                               optIdentifier: int = 0, codepage: str = None) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateStringArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrv_str * n)()
        for x in range(n):
            val[x] = _cstr(value[x], codepage)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateStringArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetStringArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _ctypes.POINTER(_c_tibrv_str_p),
                                          _ctypes.POINTER(_c_tibrv_u32),
                                          _c_tibrv_u16]

_rv.tibrvMsg_GetStringArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetStringArray(message: tibrvMsg, fieldName: str, optIdentifier: int = 0,
                            codepage: str = None) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrv_str_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetStringArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(_pystr(val[x], codepage))

    return status, ret


##
_rv.tibrvMsg_AddMsgEx.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _c_tibrvMsg,
                                  _c_tibrv_u16]

_rv.tibrvMsg_AddMsgEx.restype = _c_tibrv_status

def tibrvMsg_AddMsg(message: tibrvMsg, fieldName: str, value: tibrvMsg,
                    optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
        val = _c_tibrvMsg(value)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddMsgEx(msg, name, val, id)

    return status

_rv.tibrvMsg_UpdateMsgEx.argtypes = [_c_tibrvMsg,
                                     _c_tibrv_str,
                                     _c_tibrvMsg,
                                     _c_tibrv_u16]
_rv.tibrvMsg_UpdateMsgEx.restype = _c_tibrv_status

def tibrvMsg_UpdateMsg(message: tibrvMsg, fieldName: str, value: tibrvMsg,
                       optIdentifier: int = 0)  -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
        val = _c_tibrvMsg(value)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateMsgEx(msg, name, val, id)

    return status

_rv.tibrvMsg_GetMsgEx.argtypes = [_c_tibrvMsg,
                                  _c_tibrv_str,
                                  _ctypes.POINTER(_c_tibrvMsg),
                                  _c_tibrv_u16]

_rv.tibrvMsg_GetMsgEx.restype = _c_tibrv_status

def tibrvMsg_GetMsg(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, tibrvMsg):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    ret = None

    try:
        name = _cstr(fieldName)
        val = _c_tibrvMsg(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_GetMsgEx(msg, name, _ctypes.byref(val), id)
    if status == TIBRV_OK:
        ret = val.value

    return status, ret


_rv.tibrvMsg_AddMsgArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _c_tibrvMsg_p,
                                       _c_tibrv_u32,
                                       _c_tibrv_u16]

_rv.tibrvMsg_AddMsgArrayEx.restype = _c_tibrv_status

def tibrvMsg_AddMsgArray(message: tibrvMsg, fieldName: str, value: list,
                         optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_AddMsgArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrvMsg * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_AddMsgArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_UpdateMsgArrayEx.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _c_tibrvMsg_p,
                                          _c_tibrv_u32,
                                          _c_tibrv_u16]

_rv.tibrvMsg_UpdateMsgArrayEx.restype = _c_tibrv_status

def tibrvMsg_UpdateMsgArray(message: tibrvMsg, fieldName: str, value: list,
                            optIdentifier: int = 0)  -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        name = _cstr(fieldName)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG

    if value is None:
        status = _rv.tibrvMsg_UpdateMsgArrayEx(msg, name, None, 0, id)
        return status

    if type(value) is not list:
        return TIBRV_INVALID_ARG

    try:
        n = len(value)
        val = (_c_tibrvMsg * n)(*value)
        num = _c_tibrv_u32(n)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvMsg_UpdateMsgArrayEx(msg, name, val, num, id)

    return status


_rv.tibrvMsg_GetMsgArrayEx.argtypes = [_c_tibrvMsg,
                                       _c_tibrv_str,
                                       _ctypes.POINTER(_c_tibrvMsg_p),
                                       _ctypes.POINTER(_c_tibrv_u32),
                                       _c_tibrv_u16]

_rv.tibrvMsg_GetMsgArrayEx.restype = _c_tibrv_status

def tibrvMsg_GetMsgArray(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> (tibrv_status, list):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None or optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    ret = None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    try:
        name = _cstr(fieldName)
        val = _c_tibrvMsg_p()
        num = _c_tibrv_u32(0)
        id = _c_tibrv_u16(optIdentifier)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvMsg_GetMsgArrayEx(msg, name, _ctypes.byref(val), _ctypes.byref(num), id)

    if status == TIBRV_OK:
        ret = []
        for x in range(num.value):
            ret.append(val[x])

    return status, ret


##
_rv.tibrvMsg_AddField.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrvMsgField)]
_rv.tibrvMsg_AddField.restype = _c_tibrv_status

def tibrvMsg_AddField(message: tibrvMsg, field: tibrvMsgField) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if field is None or type(field) is not tibrvMsgField:
        return TIBRV_INVALID_ARG

    msg = _c_tibrvMsg(message)
    val = _c_tibrvMsgField(field)

    status = _rv.tibrvMsg_AddFieldEx(msg, _ctypes.byref(val))

    return status


_rv.tibrvMsg_UpdateField.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrvMsgField)]
_rv.tibrvMsg_UpdateField.restype = _c_tibrv_status

def tibrvMsg_UpdateField(message: tibrvMsg, field: tibrvMsgField) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if field is None or type(field) is not tibrvMsgField:
        return TIBRV_INVALID_ARG

    msg = _c_tibrvMsg(message)
    val = _c_tibrvMsgField(field)

    status = _rv.tibrvMsg_UpdateFieldEx(msg, _ctypes.byref(val))

    return status


_rv.tibrvMsg_GetFieldEx.argtypes = [_c_tibrvMsg,
                                    _c_tibrv_str,
                                    _ctypes.POINTER(_c_tibrvMsgField),
                                    _c_tibrv_u16]

_rv.tibrvMsg_GetFieldEx.restype = _c_tibrv_status

def tibrvMsg_GetField(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) \
                     -> (tibrv_status, tibrvMsgField):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldName is None:
        return TIBRV_INVALID_ARG, None

    if optIdentifier is None:
        return TIBRV_INVALID_ARG, None

    ret = None
    msg = _c_tibrvMsg(message)
    name = _cstr(fieldName)
    val = _c_tibrvMsgField()
    id = _c_tibrv_u16(optIdentifier)

    status = _rv.tibrvMsg_GetFieldEx(msg, name, _ctypes.byref(val), id)
    if status == TIBRV_OK:
        ret = tibrvMsgField()
        val.castTo(ret)

    return status, ret


_rv.tibrvMsg_GetFieldInstance.argtypes = [_c_tibrvMsg,
                                          _c_tibrv_str,
                                          _ctypes.POINTER(_c_tibrvMsgField),
                                          _c_tibrv_u32]

_rv.tibrvMsg_GetFieldInstance.restype = _c_tibrv_status

def tibrvMsg_GetFieldInstance(message: tibrvMsg, fieldName: str, fieldAddr: tibrvMsgField,
                              instance: int) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None:
        return TIBRV_INVALID_ARG

    if fieldAddr is None or type(fieldAddr) is not tibrvMsgField:
        return TIBRV_INVALID_ARG

    if instance is None:
        return TIBRV_INVALID_ARG

    msg = _c_tibrvMsg(message)
    name = _cstr(fieldName)
    val = _c_tibrvMsgField()
    inst = _c_tibrv_u32(instance)

    status = _rv.tibrvMsg_GetFieldInstance(msg, name, _ctypes.byref(val), inst)
    if status == TIBRV_OK:
        val.castTo(fieldAddr)

    return status


_rv.tibrvMsg_GetFieldByIndex.argtypes = [_c_tibrvMsg,
                                         _ctypes.POINTER(_c_tibrvMsgField),
                                         _c_tibrv_u32]

_rv.tibrvMsg_GetFieldByIndex.restype = _c_tibrv_status

def tibrvMsg_GetFieldByIndex(message: tibrvMsg, fieldIndex: int ) -> (tibrv_status, tibrvMsgField):

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if fieldIndex is None:
        return TIBRV_INVALID_ARG, None

    ret = None
    msg = _c_tibrvMsg(message)
    val = _c_tibrvMsgField()
    inst = _c_tibrv_u32(fieldIndex)

    status = _rv.tibrvMsg_GetFieldByIndex(msg, _ctypes.byref(val), inst)
    if status == TIBRV_OK:
        ret = tibrvMsgField()
        val.castTo(ret)

    return status, ret


##
_rv.tibrvMsg_RemoveFieldEx.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u16]
_rv.tibrvMsg_RemoveFieldEx.restype = _c_tibrv_status

def tibrvMsg_RemoveField(message: tibrvMsg, fieldName: str, optIdentifier: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None:
        return TIBRV_INVALID_ARG

    if optIdentifier is None:
        return TIBRV_INVALID_ARG

    msg = _c_tibrvMsg(message)
    name = _cstr(fieldName)
    id = _c_tibrv_u16(int(optIdentifier))

    status = _rv.tibrvMsg_RemoveFieldEx(msg, name, id)

    return status


_rv.tibrvMsg_RemoveFieldInstance.argtypes = [_c_tibrvMsg, _c_tibrv_str, _c_tibrv_u32]
_rv.tibrvMsg_RemoveFieldInstance.restype = _c_tibrv_status

def tibrvMsg_RemoveFieldInstance(message: tibrvMsg, fieldName: str, instance: int = 0) -> tibrv_status:

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if fieldName is None:
        return TIBRV_INVALID_ARG

    if instance is None:
        return TIBRV_INVALID_ARG

    msg = _c_tibrvMsg(message)
    name = _cstr(fieldName)
    inst = _c_tibrv_u32(instance)

    status = _rv.tibrvMsg_RemoveFieldInstance(msg, name, inst)

    return status

