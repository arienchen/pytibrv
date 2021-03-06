##
# pytibrv/queue.py
#   TIBRV Library for PYTHON
#   tibrvQueue_XXX
#
# LAST MODIFIED : V1.1 20170220 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
# 1. DEFAULT QUEUE
#    (1) use TIBRV_DEFAULT_QUEUE in API, like as TIBRV C 
#    (2) TibrvQueue() would be DEFAULT QUEUE by default.
#        You must call TibrvQueue.create() for a new que. 
#        ex:
#        que = TibrvQueue()             -> que is DEFAULT QUE now
#        que.create('MY QUE')           -> que is new, NOT DEFAULT QUE
#
# FEATURES: * = un-implement
# -----------------------------------------------------------------------------
#   tibrvQueue_Create
#   tibrvQueue_Destroy
#   tibrvQueue_Dispatch
#   tibrvQueue_GetCount
#   tibrvQueue_GetLimitPolicy
#   tibrvQueue_GetName
#   tibrvQueue_GetPriority
#   tibrvQueue_Poll
#   tibrvQueue_SetLimitPolicy
#   tibrvQueue_SetName
#   tibrvQueue_SetPriority
#   tibrvQueue_TimedDispatch
#   tibrvQueue_TimedDispatchOneEvent
#
#  *tibrvQueue_SetHook
#  *tibrvQueue_GetHook
#  *tibrvQueue_RemoveHook
#
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20170220 V1.1 ARIEN arien.chen@gmail.com
#   REMOVE TIBRV C Header
#
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
##
import ctypes as _ctypes
from .types import tibrv_status, tibrvQueue, tibrvQueueLimitPolicy, \
                   tibrvQueueOnComplete, \
                   TIBRV_WAIT_FOREVER, TIBRV_NO_WAIT, \
                   TIBRV_DEFAULT_QUEUE

from .status import TIBRV_OK, TIBRV_INVALID_QUEUE, TIBRV_INVALID_ARG, TIBRV_INVALID_CALLBACK

from .api import _rv, _cstr, _pystr, \
                 _c_tibrvQueue, _c_tibrvQueueLimitPolicy, \
                 _c_tibrvQueueOnComplete, _c_tibrvQueueHook, \
                 _c_tibrv_status, _c_tibrv_u32, _c_tibrv_f64


# keep callback/closure object from GC
# key = tibrvEvent
__callback = {}
__closure  = {}

def __reg(key, func, closure):
    __callback[key] = func
    if closure is not None:
        __closure[key] = closure

    return


##-----------------------------------------------------------------------------
# TIBRV API : tibrv/queue.h
##-----------------------------------------------------------------------------

##
_rv.tibrvQueue_Create.argtypes = [_ctypes.POINTER(_c_tibrvQueue)]
_rv.tibrvQueue_Create.restype = _c_tibrv_status

def tibrvQueue_Create() -> (tibrv_status, tibrvQueue):

    que = _c_tibrvQueue(0)

    status = _rv.tibrvQueue_Create(_ctypes.byref(que))

    return status, que.value

##
_rv.tibrvQueue_TimedDispatch.argtypes = [_c_tibrvQueue, _c_tibrv_f64]
_rv.tibrvQueue_TimedDispatch.restype = _c_tibrv_status

def tibrvQueue_TimedDispatch(eventQueue: tibrvQueue, timeout: float) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if timeout is None:
        return TIBRV_INVALID_ARG

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        t = _c_tibrv_f64(timeout)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvQueue_TimedDispatch(que, t)

    return status

def tibrvQueue_Dispatch(eventQueue: tibrvQueue) -> tibrv_status:
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_WAIT_FOREVER)

def tibrvQueue_Poll(eventQueue: tibrvQueue) -> tibrv_status:
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_NO_WAIT)


##
_rv.tibrvQueue_TimedDispatchOneEvent.argtypes = [_c_tibrvQueue, _c_tibrv_f64]
_rv.tibrvQueue_TimedDispatchOneEvent.restype = _c_tibrv_status


def tibrvQueue_TimedDispatchOneEvent(eventQueue: tibrvQueue, waitTime: float) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if waitTime is None:
        return TIBRV_INVALID_ARG

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        t = _c_tibrv_f64(waitTime)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvQueue_TimedDispatchOneEvent(que, t)

    return status


##
_rv.tibrvQueue_DestroyEx.argtypes = [_c_tibrvQueue, _ctypes.c_void_p, _ctypes.c_void_p]
_rv.tibrvQueue_DestroyEx.restype = _c_tibrv_status

def tibrvQueue_Destroy(eventQueue: tibrvQueue, callback : tibrvQueueOnComplete = None,
                       closure = None) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    if callback is None:
        cb = None
        cz = None
    else:
        try:
            cb = _c_tibrvQueueOnComplete(callback)
        except:
            return TIBRV_INVALID_CALLBACK

        cz = _ctypes.py_object(closure)

    status = _rv.tibrvQueue_DestroyEx(que, cb, cz)

    # THIS MAY CAUSE MEMORY LEAK
    if status == TIBRV_OK and callback is not None:
        __reg(eventQueue, cb, closure)

    return status

##
_rv.tibrvQueue_GetCount.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetCount.restype = _c_tibrv_status

def tibrvQueue_GetCount(eventQueue: tibrvQueue) -> (tibrv_status, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE, None

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE, None

    cnt = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetCount(que, _ctypes.byref(cnt))

    return status, cnt.value


##
_rv.tibrvQueue_GetPriority.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetPriority.restype = _c_tibrv_status

def tibrvQueue_GetPriority(eventQueue: tibrvQueue) -> (tibrv_status, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE, None

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE, None

    n = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetPriority(que, _ctypes.byref(n))

    return status, n.value


##
_rv.tibrvQueue_SetPriority.argtypes = [_c_tibrvQueue, _c_tibrv_u32]
_rv.tibrvQueue_SetPriority.restype = _c_tibrv_status

def tibrvQueue_SetPriority(eventQueue: tibrvQueue, priority: int) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if priority is None:
        return TIBRV_INVALID_ARG

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        p = _c_tibrv_u32(priority)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvQueue_SetPriority(que, p)

    return status


##
_rv.tibrvQueue_GetLimitPolicy.argtypes = [_c_tibrvQueue,
                                          _ctypes.POINTER(_c_tibrvQueueLimitPolicy),
                                          _ctypes.POINTER(_c_tibrv_u32),
                                          _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetLimitPolicy.restype = _c_tibrv_status

def tibrvQueue_GetLimitPolicy(eventQueue: tibrvQueue) -> (tibrv_status, int, int, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE, None, None, None

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE, None, None, None

    p = _c_tibrvQueueLimitPolicy(0)
    m = _c_tibrv_u32(0)
    d = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetLimitPolicy(que, _ctypes.byref(p), _ctypes.byref(m), _ctypes.byref(d))

    return status, p.value, m.value, d.value


##
_rv.tibrvQueue_SetLimitPolicy.argtypes = [_c_tibrvQueue,
                                          _c_tibrvQueueLimitPolicy,
                                          _c_tibrv_u32,
                                          _c_tibrv_u32]
_rv.tibrvQueue_SetLimitPolicy.restype = _c_tibrv_status

def tibrvQueue_SetLimitPolicy(eventQueue: tibrvQueue, policy: tibrvQueueLimitPolicy,
                              maxEvents: int,  discardAmount: int) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    if policy is None or maxEvents is None or discardAmount is None:
        return TIBRV_INVALID_ARG

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        p = _c_tibrvQueueLimitPolicy(int(policy))
        m = _c_tibrv_u32(int(maxEvents))
        d = _c_tibrv_u32(int(discardAmount))
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvQueue_SetLimitPolicy(que, p, m, d)
    return status



##
_rv.tibrvQueue_SetName.argtypes = [_c_tibrvQueue, _ctypes.c_char_p]
_rv.tibrvQueue_SetName.restype = _c_tibrv_status

def tibrvQueue_SetName(eventQueue: tibrvQueue, queueName: str) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    if queueName is None:
        return TIBRV_INVALID_ARG

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        sz = _cstr(queueName)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvQueue_SetName(que, sz)
    return status


##
_rv.tibrvQueue_GetName.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvQueue_GetName.restype = _c_tibrv_status

def tibrvQueue_GetName(eventQueue: tibrvQueue) -> (tibrv_status, str):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE, None

    try:
        que = _c_tibrvQueue(eventQueue)
    except:
        return TIBRV_INVALID_QUEUE, None

    sz = _ctypes.c_char_p()

    status = _rv.tibrvQueue_GetName(que, _ctypes.byref(sz))

    return status, _pystr(sz)

