##
# pytibrv/ft.py
#   tibrvft_XXX
#
# LAST MODIFIED : V1.0 20161225 ARIEN
#
# DESCRIPTIONS
# ------------------------------------------------------
# 1.
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvft_Version
#   tibrvftMember_Create
#   tibrvftMember_Destroy
#   tibrvftMember_GetGroupName
#   tibrvftMember_GetQueue
#   tibrvftMember_GetTransport
#   tibrvftMember_GetWeight
#   tibrvftMember_SetWeight
#   tibrvftMonitor_Create
#   tibrvftMonitor_DestroyEx
#   tibrvftMonitor_GetGroupName
#   tibrvftMonitor_GetQueue
#   tibrvftMonitor_GetTransport
#
#
# CHANGED LOGS
# ------------------------------------------------------
# 20161225 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes
from .types import tibrv_status
from . import _load, _func

from .api import _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvId, _c_tibrv_str, _c_tibrvTransport, _c_tibrvQueue, \
                 _c_tibrv_u16, _c_tibrv_u32, _c_tibrv_f64, \
                 tibrvId, tibrvQueue, tibrvTransport

from .status import TIBRV_OK, TIBRV_INVALID_ARG, TIBRV_INVALID_CALLBACK, \
                    TIBRV_INVALID_QUEUE, TIBRV_INVALID_TRANSPORT

# module variable
_rvft = _load('tibrvft')

# Data Types
tibrvftMember           = tibrvId
tibrvftMonitor          = tibrvId
tibrvftAction           = int           # enum

_c_tibrvftAction        = _ctypes.c_int
_c_tibrvftMember        = _c_tibrvId
_c_tibrvftMonitor       = _c_tibrvId

# CONSTANTS
TIBRVFT_PREPARE_TO_ACTIVATE         = 1
TIBRVFT_ACTIVATE                    = 2
TIBRVFT_DEACTIVATE                  = 3
TIBRVFT_PREPARE_AND_ACTIVATE        = 4


# keep callback/closure object from GC
# key = tibrvEvent
__callback = {}
__closure  = {}

def __reg(ft, func, closure):
    __callback[ft] = func
    if closure is not None:
        __closure[ft] = closure

    return

def __unreg(ft):
    if ft in __callback:
        del __callback[ft]

    if ft in __closure:
        del __closure[ft]

    return

##
# Callback
# typedef void (*tibrvftMemberCallback) (
#                 tibrvftMember               member,
#                 const char*                 groupName,
#                 tibrvftAction               action,
#                 void*                       closure);
#
_c_tibrvftMemberCallback  = _func(_ctypes.c_void_p, _c_tibrvftMember, _c_tibrv_str,  \
                                  _c_tibrvftAction, _ctypes.c_void_p)

##
#  typedef void (*tibrvftMemberOnComplete) (
#                   tibrvftMember               member,
#                   void*                       closure);
#
_c_tibrvftMemberOnComplete = _func(_ctypes.c_void_p, _c_tibrvftMember, _ctypes.c_void_p)

##
# typedef void (*tibrvftMonitorCallback) (
#                   tibrvftMonitor              monitor,
#                   const char*                 groupName,
#                   tibrv_u32                   numActiveMembers,
#                   void*                       closure);
#
_c_tibrvftMonitorCallback = _func(_ctypes.c_void_p, _c_tibrvftMonitor, _c_tibrv_str, \
                                  _c_tibrv_u32, _ctypes.c_void_p)

##
# typedef void (*tibrvftMonitorOnComplete) (
#                   tibrvftMonitor              monitor,
#                   void*                       closure);
_c_tibrvftMonitorOnComplete = _func(_ctypes.c_void_p, _c_tibrvftMonitor, _ctypes.c_void_p)

##
# tibrv/ft.h
# const char * tibrvft_Version(void)
#
_rvft.tibrvft_Version.argtypes = []
_rvft.tibrvft_Version.restype = _ctypes.c_char_p

def tibrvft_Version() -> str:
    sz = _rvft.tibrv_Version()
    return sz.decode()

##
# tibrv/ft.h
# tibrv_status tibrvftMember_Create(
#                   tibrvftMember*              member,
#                   tibrvQueue                  queue,
#                   tibrvftMemberCallback       callback,
#                   tibrvTransport              transport,
#                   const char*                 groupName,
#                   tibrv_u16                   weight,
#                   tibrv_u16                   activeGoal,
#                   tibrv_f64                   heartbeatInterval,
#                   tibrv_f64                   preparationInterval,
#                   tibrv_f64                   activationInterval,
#                   const void*                 closure
#               );
#
_rvft.tibrvftMember_Create.argtypes = [_ctypes.POINTER(_c_tibrvftMember),
                                       _c_tibrvQueue,
                                       _c_tibrvftMemberCallback,
                                       _c_tibrvTransport,
                                       _c_tibrv_str,
                                       _c_tibrv_u16,
                                       _c_tibrv_u16,
                                       _c_tibrv_f64,
                                       _c_tibrv_f64,
                                       _c_tibrv_f64,
                                       _ctypes.py_object]
_rvft.tibrvftMember_Create.restype = _c_tibrv_status

def tibrvftMember_Create(queue: tibrvQueue, callback, transport: tibrvTransport, groupName: str, \
                         weight: int, activeGoal: int, heartbeatInterval: float, \
                         preparationInterval: float, activationInterval: float, closure = None) \
                        -> (tibrv_status, tibrvftMember):

    if queue == 0 or queue is None:
        return TIBRV_INVALID_QUEUE, None

    if transport == 0 or transport is None:
        return TIBRV_INVALID_TRANSPORT, None

    if groupName is None or weight is None \
       or activeGoal is None or heartbeatInterval is None \
       or preparationInterval is None or activationInterval is None :
        return TIBRV_INVALID_ARG

    if callback is None:
        return TIBRV_INVALID_CALLBACK, None

    ft = _c_tibrvftMember(0)

    try:
        que = _c_tibrvQueue(queue)
    except:
        return TIBRV_INVALID_QUEUE, None

    try:
        cb = _c_tibrvftMemberCallback(callback)
    except:
        return TIBRV_INVALID_CALLBACK, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        grp = _cstr(groupName)
        wt = _c_tibrv_u16(weight)
        goal = _c_tibrv_u16(activeGoal)
        hbt = _c_tibrv_f64(heartbeatInterval)
        pre = _c_tibrv_f64(preparationInterval)
        act = _c_tibrv_f64(activationInterval)

        cz = _ctypes.py_object(closure)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMember_Create(_ctypes.byref(ft), que, cb, tx, grp, wt, goal, hbt, pre, act, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ft.value, cb, cz)

    return status, ft.value


##
# tibrv/ft.h
# tibrv_status tibrvftMember_Destroy(
#                   tibrvftMember               member
#               );
#
#
# tibrv_status tibrvftMember_DestroyEx(
#                   tibrvftMember               member,
#                   tibrvftMemberOnComplete     completeCallback
#               );
#
#
_rvft.tibrvftMember_Destroy.argtypes = [_c_tibrvftMember]
_rvft.tibrvftMember_Destroy.restype = _c_tibrv_status

def tibrvftMember_Destroy(member: tibrvftMember, callback = None) -> tibrv_status:

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG
    try:
        ft = _c_tibrvftMember(member)
    except:
        return TIBRV_INVALID_ARG

    if callback is None:
        cb = _c_tibrvftMemberOnComplete(0)
    else:
        try:
            cb = _c_tibrvftMemberOnComplete(callback)
        except:
            return TIBRV_INVALID_CALLBACK

    status = _rvft.tibrvftMember_Destroy(ft)

    if status == TIBRV_OK:
        __unreg(member)

        # THIS MAY CAUSE MEMORY LEAK
        if callback is not None:
            __reg(member, cb)

    return status


##
# tibrv_status tibrvftMember_GetQueue(
#    tibrvftMember               member,
#    tibrvQueue*                 queue);
#
_rvft.tibrvftMember_GetQueue.argtypes = [_c_tibrvftMember, _ctypes.POINTER(_c_tibrvQueue)]
_rvft.tibrvftMember_GetQueue.restype = _c_tibrv_status

def tibrvftMember_GetQueue(member: tibrvftMember) -> (tibrv_status, tibrvQueue):

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMember(member)
        que = _c_tibrvQueue()
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMember_GetQueue(ft, _ctypes.byref(que))

    return status, que.value


##
# tibrv_status tibrvftMember_GetTransport(
#                   tibrvftMember               member,
#                   tibrvTransport*             transport
#               );
#
_rvft.tibrvftMember_GetTransport.argtypes = [_c_tibrvftMember, _ctypes.POINTER(_c_tibrvTransport)]
_rvft.tibrvftMember_GetTransport.restype = _c_tibrv_status

def tibrvftMember_GetTransport(member: tibrvftMember) -> (tibrv_status, tibrvTransport):

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMember(member)
        tx = _c_tibrvTransport()
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMember_GetTransport(ft, _ctypes.byref(tx))

    return status, tx.value

##
# tibrv_status tibrvftMember_GetGroupName(
#                   tibrvftMember               member,
#                   const char**                groupName
#               );
#
_rvft.tibrvftMember_GetGroupName.argtypes = [_c_tibrvftMember, _ctypes.POINTER(_c_tibrv_str)]
_rvft.tibrvftMember_GetGroupName.restype = _c_tibrv_status

def tibrvftMember_GetGroupName(member: tibrvftMember) -> (tibrv_status, str):

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMember(member)
        sz = _ctypes.c_char_p(0)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMember_GetGroupName(ft, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv_status tibrvftMember_GetWeight(
#                   tibrvftMember               member,
#                   tibrv_u16*                  weight
#               );
#
_rvft.tibrvftMember_GetWeight.argtypes = [_c_tibrvftMember, _ctypes.POINTER(_c_tibrv_u16)]
_rvft.tibrvftMember_GetWeight.restype = _c_tibrv_status

def tibrvftMember_GetWeight(member: tibrvftMember) -> (tibrv_status, int):

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMember(member)
        n = _c_tibrv_u16(0)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMember_GetWeight(ft, _ctypes.byref(n))

    return status, n.value


##
# tibrv_status tibrvftMember_SetWeight(
#                   tibrvftMember               member,
#                   tibrv_u16                   weight
#               );
#
_rvft.tibrvftMember_SetWeight.argtypes = [_c_tibrvftMember, _c_tibrv_u16]
_rvft.tibrvftMember_SetWeight.restype = _c_tibrv_status

def tibrvftMember_SetWeight(member: tibrvftMember, weight: int) -> tibrv_status:

    if member == 0 or member is None:
        return TIBRV_INVALID_ARG

    if weight is None:
        return TIBRV_INVALID_ARG

    try:
        ft = _c_tibrvftMember(member)
        n = _c_tibrv_u16(weight)
    except:
        return TIBRV_INVALID_ARG

    status = _rvft.tibrvftMember_SetWeight(ft, n)

    return status


##
# tibrv_status tibrvftMonitor_Create(
#                   tibrvftMonitor*             monitor,
#                   tibrvQueue                  queue,
#                   tibrvftMonitorCallback      callback,
#                   tibrvTransport              transport,
#                   const char*                 groupName,
#                   tibrv_f64                   lostInterval,
#                   const void*                 closure
#               );
#
_rvft.tibrvftMonitor_Create.argtypes = [_ctypes.POINTER(_c_tibrvftMonitor),
                                       _c_tibrvQueue,
                                       _c_tibrvftMonitorCallback,
                                       _c_tibrvTransport,
                                       _c_tibrv_str,
                                       _c_tibrv_f64,
                                       _ctypes.py_object]
_rvft.tibrvftMonitor_Create.restype = _c_tibrv_status

def tibrvftMonitor_Create(queue: tibrvQueue, callback, transport: tibrvTransport, groupName: str,
                          lostInterval: float, closure = None) -> (tibrv_status, tibrvftMonitor):

    if queue == 0 or queue is None:
        return TIBRV_INVALID_QUEUE, None

    if transport == 0 or transport is None:
        return TIBRV_INVALID_TRANSPORT, None

    if groupName is None or lostInterval is None:
        return TIBRV_INVALID_ARG, None

    if callback is None:
        return TIBRV_INVALID_CALLBACK, None

    try:
        ft = _c_tibrvftMonitor(0)
    except:
        return TIBRV_INVALID_ARG, None

    try:
        que = _c_tibrvQueue(queue)
    except:
        return TIBRV_INVALID_QUEUE, None

    try:
        cb = _c_tibrvftMonitorCallback(callback)
    except:
        return TIBRV_INVALID_CALLBACK, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        grp = _cstr(groupName)
        hbt = _c_tibrv_f64(lostInterval)

        cz = _ctypes.py_object(closure)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMonitor_Create(_ctypes.byref(ft), que, cb, tx, grp, hbt, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ft.value, cb, cz)

    return status, ft.value


##
# tibrv_status tibrvftMonitor_Destroy(
#                   tibrvftMonitor              monitor
#               );
#
# tibrv_status tibrvftMonitor_DestroyEx(
#                   tibrvftMonitor              monitor,
#                   tibrvftMonitorOnComplete    completeCallback
#               );
#
_rvft.tibrvftMonitor_DestroyEx.argtypes = [_c_tibrvftMonitor]
_rvft.tibrvftMonitor_DestroyEx.restype = _c_tibrv_status

def tibrvftMonitor_Destroy(monitor: tibrvftMember, callback = None) -> tibrv_status:

    if monitor == 0 or monitor is None:
        return TIBRV_INVALID_ARG

    try:
        ft = _c_tibrvftMonitor(monitor)
    except:
        return TIBRV_INVALID_ARG

    if callback is None:
        cb = _c_tibrvftMonitorOnComplete(0)
    else:
        try:
            cb = _c_tibrvftMonitorOnComplete(callback)
        except:
            return TIBRV_INVALID_CALLBACK

    status = _rvft.tibrvftMonitor_DestroyEx(ft, cb)

    if status == TIBRV_OK:
        __unreg(monitor)

        # THIS MAY CAUSE MEMORY LEAK
        if callback is not None:
            __reg(monitor, cb)

    return status


##
# tibrv_status tibrvftMonitor_GetQueue(
#                   tibrvftMonitor              monitor,
#                   tibrvQueue*                 queue
#               );
#
_rvft.tibrvftMonitor_GetQueue.argtypes = [_c_tibrvftMonitor, _ctypes.POINTER(_c_tibrvQueue)]
_rvft.tibrvftMonitor_GetQueue.restype = _c_tibrv_status

def tibrvftMonitor_GetQueue(monitor: tibrvftMonitor) -> (tibrv_status, tibrvQueue):

    if monitor == 0 or monitor is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMonitor(monitor)
        que = _c_tibrvQueue()
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMonitor_GetQueue(ft, _ctypes.byref(que))

    return status, que.value


##
# tibrv_status tibrvftMonitor_GetTransport(
#                   tibrvftMonitor              monitor,
#                   tibrvTransport*             transport
#               );
#
_rvft.tibrvftMonitor_GetTransport.argtypes = [_c_tibrvftMonitor, _ctypes.POINTER(_c_tibrvTransport)]
_rvft.tibrvftMonitor_GetTransport.restype = _c_tibrv_status

def tibrvftMonitor_GetTransport(monitor: tibrvftMonitor) -> (tibrv_status, tibrvTransport):

    if monitor == 0 or monitor is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMonitor(monitor)
        tx = _c_tibrvTransport()
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMonitor_GetTransport(ft, _ctypes.byref(tx))

    return status, tx.value


##
# tibrv_status tibrvftMonitor_GetGroupName(
#                   tibrvftMonitor              monitor,
#                   const char**                groupName
#               );
#
_rvft.tibrvftMonitor_GetGroupName.argtypes = [_c_tibrvftMonitor, _ctypes.POINTER(_c_tibrv_str)]
_rvft.tibrvftMonitor_GetGroupName.restype = _c_tibrv_status

def tibrvftMonitor_GetGroupName(monitor: tibrvftMonitor) -> (tibrv_status, str):

    if monitor == 0 or monitor is None:
        return TIBRV_INVALID_ARG, None

    try:
        ft = _c_tibrvftMonitor(monitor)
        sz = _ctypes.c_char_p(0)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rvft.tibrvftMonitor_GetGroupName(ft, _ctypes.byref(sz))

    return status, _pystr(sz)

