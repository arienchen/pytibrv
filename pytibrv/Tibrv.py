##
# pytibrv/Tibrv.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.1 20161227 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
# 1. Naming as capital, TibrvXXXX , for all class
#    TIBRV API methods are all lowercase, tibrvXXXX
#
# 2. TibrvMsgDataTime is tibrvMsgDateTime, not a new class
#
# 3. tibrv_i8, tibrc_u8 ... are declared as 'abstract' class
#    TibrvMsg.get(), TibrvMsg.set(), TibrvMsg.list()
#    use these classes as CONSTANT
#
# 4. TibrvSttus support Exception handling (default is disable)
#    When you set TibrvStatus.exception = True
#    pytibrv.Tibrv would raise TibrvError when API returned tibrv_status != OK
#
# 5. Property getter
#    If TibrvStatus.exception = False (this is default)
#    All property getter function would return None when got ERROR,
#    You could get last error by calling obj.error()
#
# 6. Python destructor __del__
#    DON'T call TIBRV API in __del__()
#
#    __del__() was called by GC,
#    it doest not means it would be called immediately after 'del obj'
#
#    for example of Python Code:
#
#    que = TibrvQueue()
#    ...
#    del que
#    Tibrv.close()
#
#    THERE IS NO GUARANTEE que._del__() would be called immediately.
#    So, it may be called after Tibrv.close()
#
#    It is caller's responsibility to call destroy() after created
#
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20161227 V1.1 ARIEN arien.chen@gmail.com
#   change readonly property to normal function
#   add TibrvMsg.create() as static method
#
# 20161224 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import inspect as _inspect
from .types import *

TibrvMsgDateTime = tibrvMsgDateTime

class TibrvMsgField(tibrvMsgField):

    @property
    def msg(self):
        if self._type == TIBRVMSG_MSG:
            return TibrvMsg(self._data)

        raise TypeError('can not convert to TibrvMsg')

    @msg.setter
    def msg(self, m):
        if not isinstance(m, TibrvMsg):
            raise TypeError('data is not TibrvMsg')

        self._type = TIBRVMSG_MSG
        self._size = 0
        self._data = m.id()

    @property
    def data(self):
        if self._type == TIBRVMSG_MSG:
            return self.msg

        return self._data

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


##-----------------------------------------------------------------------------
# Tibrv
##-----------------------------------------------------------------------------
from .api import tibrv_Open, tibrv_Close, tibrv_Version

class Tibrv:

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

##-----------------------------------------------------------------------------
# TibrvStatus
##-----------------------------------------------------------------------------
from .status import *
class TibrvError(Exception):
    def __init__(self, code: tibrv_status, text=None):
        self._err = code
        self._text = text

    def __str__(self):
        return self.text()

    def code(self) -> tibrv_status:
        return self._err

    def text(self) -> str:
        if self._text is None:
            return tibrvStatus_GetText(self._err)
        else:
            return self._text

    def isOK(self) -> bool:
        if self._err == TIBRV_OK:
            return True
        else:
            return False

class TibrvStatus:

    _exception = False

    @staticmethod
    def exception(*args):
        if len(args) == 0:
            return TibrvStatus._exception
        if args[0]:
            TibrvStatus._exception = True
        else:
            TibrvStatus._exception = False

    @staticmethod
    def text(code: tibrv_status) -> str:
        return tibrvStatus_GetText(code)

    @staticmethod
    def error(code: tibrv_status, text=None) -> TibrvError:
        if code == TIBRV_OK:
            return None

        ex = TibrvError(code, text)

        if TibrvStatus._exception:
            raise ex

        return ex


##-----------------------------------------------------------------------------
#  TibrvMsg
##-----------------------------------------------------------------------------
from .msg import tibrvMsg, tibrvMsgDateTime, tibrvMsgField, \
                 tibrvMsg_Create, tibrvMsg_Destroy, tibrvMsg_Detach, \
                 tibrvMsg_Reset, tibrvMsg_ConvertToString, \
                 tibrvMsg_CreateCopy, tibrvMsg_Expand, \
                 tibrvMsg_AddDateTime, tibrvMsg_AddBool, tibrvMsg_AddI8, tibrvMsg_AddU8, \
                 tibrvMsg_AddI16, tibrvMsg_AddU16, tibrvMsg_AddI32, tibrvMsg_AddU32, \
                 tibrvMsg_AddI64, tibrvMsg_AddU64, tibrvMsg_AddF32, tibrvMsg_AddF64, \
                 tibrvMsg_AddString, tibrvMsg_AddMsg, tibrvMsg_AddField,\
                 tibrvMsg_AddI8Array, tibrvMsg_AddU8Array, tibrvMsg_AddI16Array, \
                 tibrvMsg_AddU16Array, tibrvMsg_AddI32Array, tibrvMsg_AddU32Array, \
                 tibrvMsg_AddI64Array, tibrvMsg_AddU64Array, tibrvMsg_AddF32Array, \
                 tibrvMsg_AddF64Array, tibrvMsg_AddStringArray, tibrvMsg_AddMsgArray, \
                 tibrvMsg_GetBool, tibrvMsg_GetString, tibrvMsg_GetSendSubject, \
                 tibrvMsg_GetByteSize, tibrvMsg_GetClosure, tibrvMsg_GetCurrentTime, \
                 tibrvMsg_GetCurrentTimeString, tibrvMsg_GetDateTime, tibrvMsg_GetEvent, \
                 tibrvMsg_GetF32, tibrvMsg_GetF32Array, tibrvMsg_GetF64, tibrvMsg_GetF64Array, \
                 tibrvMsg_GetField, tibrvMsg_GetFieldByIndex, tibrvMsg_GetFieldInstance, \
                 tibrvMsg_GetI8, tibrvMsg_GetI8Array, tibrvMsg_GetI16, tibrvMsg_GetI16Array, \
                 tibrvMsg_GetI32, tibrvMsg_GetI32Array, tibrvMsg_GetI64, tibrvMsg_GetI64Array, \
                 tibrvMsg_GetMsg, tibrvMsg_GetMsgArray, tibrvMsg_GetNumFields, \
                 tibrvMsg_GetReplySubject, tibrvMsg_GetStringArray, tibrvMsg_GetU8, \
                 tibrvMsg_GetU8Array, tibrvMsg_GetU16, tibrvMsg_GetU16Array, \
                 tibrvMsg_GetU32, tibrvMsg_GetU32Array, tibrvMsg_GetU64, tibrvMsg_GetU64Array, \
                 tibrvMsg_RemoveField, tibrvMsg_RemoveFieldInstance, tibrvMsg_SetReplySubject, \
                 tibrvMsg_SetSendSubject, tibrvMsg_UpdateBool, tibrvMsg_UpdateDateTime, \
                 tibrvMsg_UpdateF32, tibrvMsg_UpdateF32Array, tibrvMsg_UpdateF64, \
                 tibrvMsg_UpdateF64Array, tibrvMsg_UpdateField, tibrvMsg_UpdateI8, \
                 tibrvMsg_UpdateI8Array, tibrvMsg_UpdateI16, tibrvMsg_UpdateI16Array, \
                 tibrvMsg_UpdateI32, tibrvMsg_UpdateI32Array, tibrvMsg_UpdateI64, \
                 tibrvMsg_UpdateI64Array, tibrvMsg_UpdateMsg, tibrvMsg_UpdateMsgArray, \
                 tibrvMsg_UpdateString, tibrvMsg_UpdateStringArray, tibrvMsg_UpdateU8, \
                 tibrvMsg_UpdateU8Array, tibrvMsg_UpdateU16, tibrvMsg_UpdateU16Array, \
                 tibrvMsg_UpdateU32, tibrvMsg_UpdateU32Array, tibrvMsg_UpdateU64, \
                 tibrvMsg_UpdateU64Array

class TibrvMsg:

    def id(self):
        return self._msg

    def __init__(self, msg: tibrvMsg = 0):
        self._err = None
        self._msg = 0

        # For exist msg
        if msg is not None and msg != 0:
            self._copied = True
            self._msg = tibrvMsg(msg)

        return

    @staticmethod
    def create(initBytes: int = 0):

        status, ret = tibrvMsg_Create(initBytes)
        if status == TIBRV_OK:
            return TibrvMsg(ret), None

        return None, TibrvError(status)

    def destroy(self) -> tibrv_status:

        if self.id() == 0 or self._copied:
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvMsg_Destroy(self.id())
        self._msg = 0
        self._err = TibrvStatus.error(status)

        return status;

    def __str__(self, codepage: str = None):
        if self.id() == 0:
            return None

        status, sz = tibrvMsg_ConvertToString(self.id(), codepage)
        self._err = TibrvStatus.error(status)

        return sz


    def detach(self) -> tibrv_status:

        status = tibrvMsg_Detach(self.id())
        self._err = TibrvStatus.error(status)

        if status == TIBRV_OK:
            # Let destroy()  to call tibrvMsg_Drstroy
            self._copied = False

        return status

    def expend(self, bytes: int ) -> tibrv_status:

        status = tibrvMsg_Expand(self.id(), bytes)
        self._err = TibrvStatus.error(status)

        return status

    def bytes(self) -> int:

        status, ret = tibrvMsg_GetByteSize(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def copy(self):

        status, m = tibrvMsg_CreateCopy(self.id())

        if status == TIBRV_OK:
            ret = TibrvMsg(m)
            ret._copied = False

        self._err = TibrvStatus.error(status)

        return ret

    def count(self) -> int:

        status, ret = tibrvMsg_GetNumFields(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def reset(self):

        status = tibrvMsg_Reset(self.id())
        self._err = TibrvStatus.error(status)

        return

    @property
    def sendSubject(self):

        status, ret = tibrvMsg_GetSendSubject(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @sendSubject.setter
    def sendSubject(self, subj: str):

        status = tibrvMsg_SetSendSubject(self.id(), subj)
        self._err = TibrvStatus.error(status)

    @property
    def replySubject(self):

        status, ret = tibrvMsg_GetReplySubject(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @replySubject.setter
    def replySubject(self, subj: str):

        status = tibrvMsg_SetReplySubject(self.id(), subj)

        self._err = TibrvStatus.error(status)

    @staticmethod
    def now() -> TibrvMsgDateTime:

        status, ret = tibrvMsg_GetCurrentTime()
        TibrvStatus.error(status)

        return ret

    @staticmethod
    def nowString() -> (str, str):

        status, lct, gmt = tibrvMsg_GetCurrentTimeString()
        TibrvStatus.error(status)

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
            self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
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

        self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')

        return None


    def set(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
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

        self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')

        return None

    def get(self,  data_type, name:str, id: int = 0, **kwargs):

        if not _inspect.isclass(data_type):
            self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not a class')
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

        self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')

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

        self._err = TibrvStatus.error(TIBRV_INVALID_ARG, data_type.__name__ + ' is not supported')

        return None


    def __getitem__(self, item):
        # Get By Index
        if type(item) is int:
            if item < 0:
                status = TIBRV_INVALID_ARG
                self._err = TibrvStatus.error(status)
                return None

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

    def error(self) -> TibrvError:
        return self._err


##-----------------------------------------------------------------------------
# TibrvQueue
##-----------------------------------------------------------------------------
from .queue import tibrvQueue, tibrvQueueGroup, tibrvQueueLimitPoliy, \
                   tibrvQueue_Create, tibrvQueue_Destroy, \
                   tibrvQueue_Dispatch, tibrvQueue_GetCount, tibrvQueue_GetName, \
                   tibrvQueue_GetLimitPolicy, tibrvQueue_GetPriority, \
                   tibrvQueue_Poll, tibrvQueue_SetLimitPolicy, tibrvQueue_SetName, \
                   tibrvQueue_SetPriority, tibrvQueue_TimedDispatch, \
                   tibrvQueue_TimedDispatchOneEvent


class TibrvQueue:

    DISCARD_NONE    = TIBRVQUEUE_DISCARD_NONE
    DISCARD_FIRST   = TIBRVQUEUE_DISCARD_FIRST
    DISCARD_LAST    = TIBRVQUEUE_DISCARD_LAST
    DISCARD_NEW     = TIBRVQUEUE_DISCARD_NEW

    def __init__(self, que: tibrvQueue = TIBRV_DEFAULT_QUEUE):
        self._que = 0
        self._err = None
        self._policy = 0
        self._maxEvents = 0
        self._discard = 0

        if que is not None:
            self._que = tibrvQueue(que)

    def id(self):
        return self._que

    def create(self, name: str = None) -> tibrv_status:

        if self._que != 0 and self._que != TIBRV_DEFAULT_QUEUE:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        status, que = tibrvQueue_Create()
        if status == TIBRV_OK:
            self._que = que

            s,p,m,d = tibrvQueue_GetLimitPolicy(que)
            if s == TIBRV_OK:
                self._policy = p
                self._maxEvents = m
                self._discard = d

            if name is not None:
                tibrvQueue_SetName(que, name)

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:

        if self._que == 0 or self._que == TIBRV_DEFAULT_QUEUE:
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvQueue_Destroy(self._que)
        self._que = 0
        self._err = TibrvStatus.error(status)

        return status


    @property
    def name(self) -> str:

        status, ret = tibrvQueue_GetName(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @name.setter
    def name(self, sz: str) -> None:
        status = tibrvQueue_SetName(self.id(), sz)
        self._err = TibrvStatus.error(status)

    def dispatch(self) -> int:

        status = tibrvQueue_Dispatch(self.id())
        self._err = TibrvStatus.error(status)

        return status

    @property
    def count(self) -> int:

        status, ret = tibrvQueue_GetCount(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def setPolicy(self, policy: int, maxEvents: int, discardAmount: int) -> tibrv_status:

        status = tibrvQueue_SetLimitPolicy(self.id(), policy, maxEvents, discardAmount)
        self._err = TibrvStatus.error(status)

        if status == TIBRV_OK:
            self._policy = int(policy)
            self._maxEvents = int(maxEvents)
            self._discard = int(discardAmount)

        return status

    def policy(self) -> str:
        return self._policy

    def maxEvents(self) -> str:
        return self._maxEvents

    def discardAmount(self) -> str:
        return self._discard

    @property
    def priority(self) -> str:

        status, ret = tibrvQueue_GetPriority(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @priority.setter
    def priority(self, val: int) -> None:

        status = tibrvQueue_SetPriority(self.id(), val)
        self._err = TibrvStatus.error(status)

    def poll(self) -> tibrv_status:

        status = tibrvQueue_Poll(self.id())
        self._err = TibrvStatus.error(status)

        return status


    def timedDispatch(self, timeout: float) -> tibrv_status:

        status = tibrvQueue_TimedDispatch(self.id(), timeout)
        self._err = TibrvStatus.error(status)

        return status

    def error(self) -> TibrvError :
        return self._err


##-----------------------------------------------------------------------------
## TibrvTx
##-----------------------------------------------------------------------------
from .tport import tibrvTransport, tibrvTransport_Create, tibrvTransport_Destroy, \
                   tibrvTransport_CreateInbox, tibrvTransport_GetService, \
                   tibrvTransport_GetDaemon, tibrvTransport_GetNetwork, tibrvTransport_GetDescription, \
                   tibrvTransport_RequestReliability, tibrvTransport_SetDescription, \
                   tibrvTransport_Send, tibrvTransport_SendRequest, tibrvTransport_SendReply

class TibrvTx :
    def __init__(self, tx: tibrvTransport = 0):
        self._tx = 0
        self._err = None
        if tx is not None:
            self._tx = tibrvTransport(tx)

    def id(self):
        return self._tx

    def create(self, service: str, network: str, daemon: str) -> int:
        if self._tx != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        status, self._tx = tibrvTransport_Create(service, network, daemon)
        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> int:
        status = tibrvTransport_Destroy(self._tx)
        self._tx = 0

        self._err = TibrvStatus.error(status)

        return status

    @property
    def description(self) -> str:

        status, ret = tibrvTransport_GetDescription(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @description.setter
    def description(self, sz: str):

        status = tibrvTransport_SetDescription(self.id(), sz)
        self._err = TibrvStatus.error(status)

    @property
    def service(self) -> str:

        status, ret = tibrvTransport_GetService(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def network(self) -> str:

        status, ret = tibrvTransport_GetNetwork(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def daemon(self) -> str:

        status, ret = tibrvTransport_GetDaemon(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def inbox(self) -> str:

        status, ret = tibrvTransport_CreateInbox(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def reliability(self, reliability: float) -> int:

        status = tibrvTransport_RequestReliability(self.id(), reliability)
        self._err = TibrvStatus.error(status)

        return status

    def error(self) -> TibrvError :
        return self._err

    def send(self, msg: TibrvMsg, subj: str = None) -> tibrv_status:

        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status, None

        if subj is not None:
            status = tibrvMsg_SetSendSubject(msg.id(), subj)
            if status != TIBRV_OK:
                self._err = TibrvStatus.error(status)
                return status

        status = tibrvTransport_Send(self.id(), msg.id())

        self._err = TibrvStatus.error(status)

        return status

    def sendRequest(self, msg: TibrvMsg, timeout: float, subj: str = None) -> (tibrv_status, TibrvMsg):

        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status, None

        if subj is not None:
            status = tibrvMsg_SetSendSubject(msg.id(), subj)
            if status != TIBRV_OK:
                self._err = TibrvStatus.error(status)
                return status, None

        reply = None
        status, m = tibrvTransport_SendRequest(self.id(), msg.id(), timeout)
        if status == TIBRV_OK:
            reply = TibrvMsg(m)

        self._err = TibrvStatus.error(status)

        return status, reply

    def sendReply(self, msg: TibrvMsg, request: TibrvMsg) -> tibrv_status:
        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        if request is None or not isinstance(request, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvTransport_SendReply(self.id(), msg.id(), request.id())

        self._err = TibrvStatus.error(status)

        return status


##-----------------------------------------------------------------------------
## TibrvEvent, TibrvTimer, TibrvListener
##-----------------------------------------------------------------------------
from .events import tibrvEvent, tibrvClosure,  \
                    tibrvEvent_CreateTimer, tibrvEvent_CreateListener, \
                    tibrvEvent_CreateVectorListener, tibrvEvent_Destroy, \
                    tibrvEvent_GetType, tibrvEvent_ResetTimerInterval, \
                    tibrvEvent_GetTimerInterval, tibrvEvent_GetQueue, \
                    tibrvEvent_GetListenerSubject, tibrvEvent_GetListenerTransport

class TibrvTimerCallback:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, event, msg, closure):
        pass

    def _register(self):
        def _cb(event, msg, closure):
            if event != 0:
                ev = TibrvTimer(event)
            else:
                ev = None

            cz = tibrvClosure(closure)

            self.callback(ev, None, cz)

        return _cb


class TibrvMsgCallback:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, event, msg: TibrvMsg, closure):
        pass

    def _register(self):
        def _cb(event, msg, closure):
            if event != 0:
                ev = TibrvListener(event)
            else:
                ev = None

            if msg != 0:
                m = TibrvMsg(msg)
            else:
                m = None

            cz = tibrvClosure(closure)

            self.callback(ev, m, cz)

        return _cb


class TibrvEvent:

    def __init__(self, event: tibrvEvent = 0):
        self._err = None
        self._event = 0
        if event is not None:
            self._event = event

    def id(self):
        return self._event

    def destroy(self):

        status = tibrvEvent_Destroy(self._event)
        self._event = 0

        return status

    def error(self) -> TibrvError:
        return self._err

    def eventType(self):

        status, ret = tibrvEvent_GetType(self.id())
        self._err = TibrvStatus.error(status)

        return ret


class TibrvTimer(TibrvEvent):

    def __init__(self, event: tibrvEvent = 0):
        super().__init__(event)

    def create(self, que: TibrvQueue, callback: TibrvTimerCallback,
               interval: float, closure = None) -> tibrv_status:

        if self._event != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)

        if que is None or not isinstance(que, TibrvQueue):
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        if callback is None or not isinstance(callback, TibrvTimerCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status, ret = tibrvEvent_CreateTimer(que.id(), callback._register(), interval, closure)

        if status == TIBRV_OK:
            self._event = ret

        self._err = TibrvStatus.error(status)
        return status

    @property
    def interval(self):
        status, ret = tibrvEvent_GetTimerInterval(self.id())

        self._err = TibrvStatus.error(status)

        return ret

    @interval.setter
    def interval(self, sec: float):

        status = tibrvEvent_ResetTimerInterval(self.id(), sec)
        self._err = TibrvStatus.error(status)


class TibrvListener(TibrvEvent):

    def __init__(self, event: tibrvEvent = 0):
        super().__init__(event)

    def create(self, que: TibrvQueue, callback: TibrvMsgCallback, tx: TibrvTx,
               subject: str, closure = None) -> tibrv_status:

        if self._event != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)

        if que is None or not isinstance(que, TibrvQueue):
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        if tx is None or not isinstance(tx, TibrvTx):
            status = TIBRV_INVALID_TRANSPORT
            self._err = TibrvStatus.error(status)
            return status

        if callback is None or not isinstance(callback, TibrvMsgCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status, self._event = tibrvEvent_CreateListener(que.id(), callback._register(),
                                                        tx.id(), subject, closure)

        self._err = TibrvStatus.error(status)

        return status

    def subject(self) -> str:

        status, ret = tibrvEvent_GetListenerSubject(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def queue(self) -> TibrvQueue:
        ret = None

        status, q = tibrvEvent_GetQueue(self.id())
        if status == TIBRV_OK:
            ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret


##-----------------------------------------------------------------------------
## TibrvDispatcher
##-----------------------------------------------------------------------------
from .disp import tibrvDispatcher, \
                  tibrvDispatcher_Create, tibrvDispatcher_Destroy, tibrvDispatcher_Join, \
                  tibrvDispatcher_GetName, tibrvDispatcher_SetName

class TibrvDispatcher :
    def __init__(self):
        self._disp = tibrvDispatcher(0)
        self._err = None
        self._timeout = TIBRV_WAIT_FOREVER

    def id(self):
        return self._disp

    def create(self, que: TibrvQueue, timeout: float = TIBRV_WAIT_FOREVER) -> tibrv_status:

        if self._disp != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)

            return status

        if que is None or not isinstance(que, TibrvQueue):
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)

            return status

        if timeout is None:
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)

            return status

        self._timeout = timeout
        status, self._disp = tibrvDispatcher_Create(que.id(), self._timeout)

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> int:

        status = tibrvDispatcher_Destroy(self._disp)
        self._disp = 0
        self._err = TibrvStatus.error(status)

        return status

    @property
    def name(self) -> str:

        status, sz = tibrvDispatcher_GetName(self.id())

        self._err = TibrvStatus.error(status)

        return sz

    @name.setter
    def name(self, sz: str):

        status = tibrvDispatcher_SetName(self.id(), sz)
        self._err = TibrvStatus.error(status)

    def join(self) -> tibrv_status:

        status = tibrvDispatcher_Join(self.id())
        self._err = TibrvStatus.error(status)

        return status

    def timeout(self) -> float:
        return self._timeout

    def error(self) -> TibrvError:
        return self._err

