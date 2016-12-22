##
# pytibrv/disp.py
#   TIBRV Library for PYTHON
#   tibrvDispacher_XXX
# 
# LAST MODIFIED : V1.0 20161211 ARIEN
#
# DESCRIPTIONS
# ---------------------------------------------------
# 1. TibrvDispatcher.__del__() will call tibrvDispatcher_Destroy() 
# 
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvDispatcher_Create
#   tibrvDispatcher_Destroy
#   tibrvDispatcher_GetName
#   tibrvDispatcher_SetName
#
# Python Class
# ------------------------------------------------------
#   TibrvDispacher 
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes
from .queue import *
from .api import _rv, _cstr, _pystr

##-----------------------------------------------------------------------------
## TibrvDispatcher
##-----------------------------------------------------------------------------

##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_CreateEx(
#                tibrvDispatcher*            dispatcher,
#                tibrvDispatchable           dispatchable,
#                tibrv_f64                   idleTimeout
#              );
#
_rv.tibrvDispatcher_CreateEx.argtypes = [_ctypes.POINTER(c_tibrvDispatcher), c_tibrvDispatchable, c_tibrv_f64]
_rv.tibrvDispatcher_CreateEx.restype = c_tibrv_status

def tibrvDispatcher_Create(dispatchable: tibrvDispatchable, idleTimeout: float = TIBRV_WAIT_FOREVER) -> tibrv_status:

    disp = c_tibrvDispatcher(0)
    que  = c_tibrvDispatchable(dispatchable)
    t = c_tibrv_f64(idleTimeout)
    status = _rv.tibrvDispatcher_CreateEx(_ctypes.byref(disp), que, t)

    return status, disp.value

##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_Join(
#    tibrvDispatcher             dispatcher);
#
_rv.tibrvDispatcher_Join.argtypes = [c_tibrvDispatcher]
_rv.tibrvDispatcher_Join.restype = c_tibrv_status


def tibrvDispatcher_Join(dispatcher:tibrvDispatcher) -> tibrv_status :

    disp = c_tibrvDispatcher(dispatcher)
    status = _rv.tibrvDispatcher_Join(disp)
    return status


##
# tibrv/disp.h
# tibrv_status  tibrvDispatcher_Destroy(
#                 ibrvDispatcher             dispatcher
#               );
#
_rv.tibrvDispatcher_Destroy.argtypes = [c_tibrvDispatcher]
_rv.tibrvDispatcher_Destroy.restype = c_tibrv_status

def tibrvDispatcher_Destroy(dispatcher:tibrvDispatcher) -> tibrv_status :

    disp = c_tibrvDispatcher(dispatcher)
    status = _rv.tibrvDispatcher_Destroy(disp)

    return status


##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_SetName(
#                tibrvDispatcher             dispatcher,
#                const char*                 dispatchName
#              );
#
_rv.tibrvDispatcher_SetName.argtypes = [c_tibrvDispatcher, _ctypes.c_char_p]
_rv.tibrvDispatcher_SetName.restype = c_tibrv_status

def tibrvDispatcher_SetName(dispatcher:tibrvDispatcher, dispatchName:str) -> tibrv_status :

    disp = c_tibrvDispatcher(dispatcher)
    sz = _cstr(dispatchName)
    status = _rv.tibrvDispatcher_SetName(disp, sz)

    return status

##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_GetName(
#                tibrvDispatcher             dispatcher,
#                const char**                dispatchName
#              );
_rv.tibrvDispatcher_GetName.argtypes = [c_tibrvDispatcher, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvDispatcher_GetName.restype = c_tibrv_status

def tibrvDispatcher_GetName(dispatcher:tibrvDispatcher) -> tibrv_status :

    disp = c_tibrvDispatcher(dispatcher)
    sz = _ctypes.c_char_p()
    status = _rv.tibrvDispatcher_GetName(disp, _ctypes.byref(sz))

    return status, _pystr(sz)

class TibrvDispatcher :
    def __init__(self):
        self._disp = 0
        self._err = None
        self._timeout = TIBRV_WAIT_FOREVER

    def __del__(self):
        try :
            self.destroy()
        except:
            pass

    def id(self):
        return self._disp

    def create(self, que : TibrvQueue, timeout : float = TIBRV_WAIT_FOREVER) -> tibrv_status :

        if self._disp != 0:
            status = TIBRV_ID_IN_USE
        else:
            self._timeout = float(timeout)
            status,ret = tibrvDispatcher_Create(que.id(), self._timeout);
            if status == TIBRV_OK:
                self._disp = ret

        self._err = TibrvStatus.error(status)

        return status;

    def destroy(self) -> int:
        if self._disp == 0:
            status =  TIBRV_INVALID_DISPATCHER
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvDispatcher_Destroy(self._disp)
        self._disp = 0
        self._err = TibrvStatus.error(status)

        return status

    @property
    def name(self) -> str:
        sz = None

        if self.id() == 0:
            status = TIBRV_INVALID_DISPATCHER
        else:
            status, sz = tibrvDispatcher_GetName(self.id())

        self._err = TibrvStatus.error(status)

        return sz

    @name.setter
    def name(self, sz: str) -> None:
        if self.id() == 0:
            status = TIBRV_INVALID_DISPATCHER
        else:
            status = tibrvDispatcher_SetName(self._disp, sz)

        self._err = TibrvStatus.error(status)

    def join(self) -> tibrv_status:
        if self.id() == 0:
            status = TIBRV_INVALID_DISPATCHER
        else:
            status = tibrvDispatcher_Join(self._que)

        self._err = TibrvStatus.error(status)
        return status

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def error(self) -> TibrvError:
        return self._err
