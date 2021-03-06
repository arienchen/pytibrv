##
# pytibrv/disp.py
#   tibrvDispacher_XXX
# 
# LAST MODIFIED : V1.1 20170220 ARIEN
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
# 20170220 V1.1 ARIEN arien.chen@gmail.com
#   REMOVE TIBRV C Header
#
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes

from .types import tibrvDispatcher, tibrvDispatchable, tibrv_status, \
                   TIBRV_WAIT_FOREVER

from .api import _rv, _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvDispatcher, _c_tibrvDispatchable, \
                 _c_tibrv_f64

from .status import TIBRV_INVALID_DISPATCHER, TIBRV_INVALID_ARG, TIBRV_INVALID_DISPATCHABLE

##-----------------------------------------------------------------------------
# TIBRV API : tibrv/disp.h
##-----------------------------------------------------------------------------

_rv.tibrvDispatcher_CreateEx.argtypes = [_ctypes.POINTER(_c_tibrvDispatcher),
                                         _c_tibrvDispatchable,
                                         _c_tibrv_f64]
_rv.tibrvDispatcher_CreateEx.restype = _c_tibrv_status

def tibrvDispatcher_Create(dispatchable: tibrvDispatchable,
                           idleTimeout: float = TIBRV_WAIT_FOREVER) -> (tibrv_status, tibrvDispatcher):

    if dispatchable is None or dispatchable == 0:
        return TIBRV_INVALID_DISPATCHABLE, None

    if idleTimeout is None:
        return TIBRV_INVALID_ARG, None

    disp = _c_tibrvDispatcher(0)

    try:
        que  = _c_tibrvDispatchable(dispatchable)
    except:
        return TIBRV_INVALID_DISPATCHABLE, None

    try:
        t = _c_tibrv_f64(idleTimeout)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvDispatcher_CreateEx(_ctypes.byref(disp), que, t)

    return status, disp.value

##
_rv.tibrvDispatcher_Join.argtypes = [_c_tibrvDispatcher]
_rv.tibrvDispatcher_Join.restype = _c_tibrv_status

def tibrvDispatcher_Join(dispatcher: tibrvDispatcher) -> tibrv_status:

    if dispatcher is None or dispatcher == 0:
        return TIBRV_INVALID_DISPATCHER

    try:
        disp = _c_tibrvDispatcher(dispatcher)
    except:
        return TIBRV_INVALID_DISPATCHER

    status = _rv.tibrvDispatcher_Join(disp)
    return status


##
_rv.tibrvDispatcher_Destroy.argtypes = [_c_tibrvDispatcher]
_rv.tibrvDispatcher_Destroy.restype = _c_tibrv_status

def tibrvDispatcher_Destroy(dispatcher: tibrvDispatcher) -> tibrv_status:

    if dispatcher is None or dispatcher == 0:
        return TIBRV_INVALID_DISPATCHER

    try:
        disp = _c_tibrvDispatcher(dispatcher)
    except:
        return TIBRV_INVALID_DISPATCHER

    status = _rv.tibrvDispatcher_Destroy(disp)

    return status


##
_rv.tibrvDispatcher_SetName.argtypes = [_c_tibrvDispatcher, _ctypes.c_char_p]
_rv.tibrvDispatcher_SetName.restype = _c_tibrv_status

def tibrvDispatcher_SetName(dispatcher: tibrvDispatcher, dispatchName: str) -> tibrv_status:

    if dispatcher is None or dispatcher == 0:
        return TIBRV_INVALID_DISPATCHER

    try:
        disp = _c_tibrvDispatcher(dispatcher)
    except:
        return TIBRV_INVALID_DISPATCHER

    try:
        sz = _cstr(dispatchName)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvDispatcher_SetName(disp, sz)

    return status

##
_rv.tibrvDispatcher_GetName.argtypes = [_c_tibrvDispatcher, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvDispatcher_GetName.restype = _c_tibrv_status

def tibrvDispatcher_GetName(dispatcher: tibrvDispatcher) -> (tibrv_status, str):

    if dispatcher is None or dispatcher == 0:
        return TIBRV_INVALID_DISPATCHER, None

    try:
        disp = _c_tibrvDispatcher(dispatcher)
    except:
        return TIBRV_INVALID_DISPATCHER, None

    sz = _ctypes.c_char_p()
    status = _rv.tibrvDispatcher_GetName(disp, _ctypes.byref(sz))

    return status, _pystr(sz)
