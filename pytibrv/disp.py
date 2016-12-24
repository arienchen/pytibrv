##
# pytibrv/disp.py
#   tibrvDispacher_XXX
# 
# LAST MODIFIED : V1.0 20161211 ARIEN
#
# DESCRIPTIONS
# ------------------------------------------------------
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvDispatcher_Create
#   tibrvDispatcher_Destroy
#   tibrvDispatcher_GetName
#   tibrvDispatcher_SetName
#
# CHANGED LOGS
# ------------------------------------------------------
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes
from .types import tibrvDispatcher, tibrvDispatchable, tibrv_status, \
                   TIBRV_WAIT_FOREVER, TIBRV_NO_WAIT

from .api import _rv, _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvDispatcher, _c_tibrvDispatchable, \
                 _c_tibrv_f64


##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_CreateEx(
#                tibrvDispatcher*            dispatcher,
#                tibrvDispatchable           dispatchable,
#                tibrv_f64                   idleTimeout
#              );
#
_rv.tibrvDispatcher_CreateEx.argtypes = [_ctypes.POINTER(_c_tibrvDispatcher),
                                         _c_tibrvDispatchable,
                                         _c_tibrv_f64]
_rv.tibrvDispatcher_CreateEx.restype = _c_tibrv_status

def tibrvDispatcher_Create(dispatchable: tibrvDispatchable, idleTimeout: float = TIBRV_WAIT_FOREVER) \
                          -> (tibrv_status, tibrvDispatcher):

    disp = _c_tibrvDispatcher(0)
    que  = _c_tibrvDispatchable(dispatchable)
    t = _c_tibrv_f64(idleTimeout)
    status = _rv.tibrvDispatcher_CreateEx(_ctypes.byref(disp), que, t)

    return status, disp.value

##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_Join(
#    tibrvDispatcher             dispatcher);
#
_rv.tibrvDispatcher_Join.argtypes = [_c_tibrvDispatcher]
_rv.tibrvDispatcher_Join.restype = _c_tibrv_status


def tibrvDispatcher_Join(dispatcher:tibrvDispatcher) -> tibrv_status:

    disp = _c_tibrvDispatcher(dispatcher)
    status = _rv.tibrvDispatcher_Join(disp)
    return status


##
# tibrv/disp.h
# tibrv_status  tibrvDispatcher_Destroy(
#                 ibrvDispatcher             dispatcher
#               );
#
_rv.tibrvDispatcher_Destroy.argtypes = [_c_tibrvDispatcher]
_rv.tibrvDispatcher_Destroy.restype = _c_tibrv_status

def tibrvDispatcher_Destroy(dispatcher:tibrvDispatcher) -> tibrv_status:

    disp = _c_tibrvDispatcher(dispatcher)
    status = _rv.tibrvDispatcher_Destroy(disp)

    return status


##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_SetName(
#                tibrvDispatcher             dispatcher,
#                const char*                 dispatchName
#              );
#
_rv.tibrvDispatcher_SetName.argtypes = [_c_tibrvDispatcher, _ctypes.c_char_p]
_rv.tibrvDispatcher_SetName.restype = _c_tibrv_status

def tibrvDispatcher_SetName(dispatcher:tibrvDispatcher, dispatchName:str) -> tibrv_status:

    disp = _c_tibrvDispatcher(dispatcher)
    sz = _cstr(dispatchName)
    status = _rv.tibrvDispatcher_SetName(disp, sz)

    return status

##
# tibrv/disp.h
# tibrv_status tibrvDispatcher_GetName(
#                tibrvDispatcher             dispatcher,
#                const char**                dispatchName
#              );
_rv.tibrvDispatcher_GetName.argtypes = [_c_tibrvDispatcher, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvDispatcher_GetName.restype = _c_tibrv_status

def tibrvDispatcher_GetName(dispatcher:tibrvDispatcher) -> (tibrv_status, str):

    disp = _c_tibrvDispatcher(dispatcher)
    sz = _ctypes.c_char_p()
    status = _rv.tibrvDispatcher_GetName(disp, _ctypes.byref(sz))

    return status, _pystr(sz)
