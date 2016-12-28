##
# pytibrv/queue.py
#   TIBRV Library for PYTHON
#   tibrvQueue_XXX
#
# LAST MODIFIED : V1.0 20161211 ARIEN arien.chen@gmail.com 
#
# DESCRIPTIONS
##-----------------------------------------------------------------------------
# 1.TibrvQueue.__del__ will call tibrvQueue_Destory() 
# 
# 2. DEFAULT QUEUE
#    (1) use TIBRV_DEFAULT_QUEUE in API, like as TIBRV C 
#    (2) TibrvQueue() would be DEFAULT QUEUE by default.
#        You must call TibrvQueue.create() for a new que. 
#        ex:
#        que = TibrvQueue()             -> que is DEFAULT QUE now
#        que.create('MY QUE')           -> que is new, NOT DEFAULT QUE
#
# FEATURES: * = un-implement
##-----------------------------------------------------------------------------
#   tibrvQueue_Create
#   tibrvQueue_DestroyEx
#   tibrvQueue_GetCount
#   tibrvQueue_GetLimitPolicy
#   tibrvQueue_GetName
#   tibrvQueue_GetPriority
#   tibrvQueue_SetLimitPolicy
#   tibrvQueue_SetName
#   tibrvQueue_SetPriority
#   tibrvQueue_TimedDispatch
#   tibrvQueue_TimedDispatchOneEvent
##
# CHANGED LOGS
##-----------------------------------------------------------------------------
# 20161211 V1.0 ARIEN arien.chen@gmail.com 
#   CREATED
#
##
import ctypes as _ctypes
from .types import tibrv_status, tibrvQueue, tibrvQueueGroup, tibrvQueueLimitPoliy, \
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


## tibrv/queue.h
# tibrv_status tibrvQueue_Create(
#                tibrvQueue*                 eventQueue
#              );
#
_rv.tibrvQueue_Create.argtypes = [_ctypes.POINTER(_c_tibrvQueue)]
_rv.tibrvQueue_Create.restype = _c_tibrv_status

def tibrvQueue_Create() -> (tibrv_status, tibrvQueue):

    que = _c_tibrvQueue(0)

    status = _rv.tibrvQueue_Create(_ctypes.byref(que))

    return status, que.value

##
# tibrv/queue.h
# tibrv_status tibrvQueue_TimedDispatch(
#                tibrvQueue                  eventQueue,
#                tibrv_f64                   timeout
#              );
#
_rv.tibrvQueue_TimedDispatch.argtypes = [_c_tibrvQueue, _c_tibrv_f64]
_rv.tibrvQueue_TimedDispatch.restype = _c_tibrv_status

def tibrvQueue_TimedDispatch(eventQueue: tibrvQueue, timeout: float) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if timeout is None:
        return TIBRV_INVALID_ARG

    que = _c_tibrvQueue(eventQueue)
    t = _c_tibrv_f64(timeout)

    status = _rv.tibrvQueue_TimedDispatch(que, t)

    return status

def tibrvQueue_Dispatch(eventQueue: tibrvQueue) -> tibrv_status:
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_WAIT_FOREVER)

def tibrvQueue_Poll(eventQueue: tibrvQueue) -> tibrv_status:
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_NO_WAIT)


##
# tibrv/queue.h
# tibrv_status tibrvQueue_TimedDispatchOneEvent(
#                tibrvQueue                  queue,
#                tibrv_f64                   waitTime
#              );
#
_rv.tibrvQueue_TimedDispatchOneEvent.argtypes = [_c_tibrvQueue, _c_tibrv_f64]
_rv.tibrvQueue_TimedDispatchOneEvent.restype = _c_tibrv_status


def tibrvQueue_TimedDispatchOneEvent(eventQueue: tibrvQueue, waitTime: float) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if waitTime is None:
        return TIBRV_INVALID_ARG

    que = _c_tibrvQueue(eventQueue)
    t = _c_tibrv_f64(waitTime)

    status = _rv.tibrvQueue_TimedDispatchOneEvent(que, t)

    return status


##
# tibrv/queue.h
# tibrv_status tibrvQueue_DestroyEx(
#                tibrvQueue                  eventQueue,
#                tibrvQueueOnComplete        completeCallback,
#                const void*                 closure
#              );
#
_rv.tibrvQueue_DestroyEx.argtypes = [_c_tibrvQueue, _ctypes.c_void_p, _ctypes.c_void_p]
_rv.tibrvQueue_DestroyEx.restype = _c_tibrv_status

def tibrvQueue_Destroy(eventQueue: tibrvQueue, callback = None, closure = None) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    que = _c_tibrvQueue(eventQueue)

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
# tibrv/queue.h
# tibrv_status tibrvQueue_GetCount(
#                tibrvQueue                  eventQueue,
#                tibrv_u32*                  numEvents
#              );
#
_rv.tibrvQueue_GetCount.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetCount.restype = _c_tibrv_status

def tibrvQueue_GetCount(eventQueue: tibrvQueue) -> (tibrv_status, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    que = _c_tibrvQueue(eventQueue)
    cnt = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetCount(que, _ctypes.byref(cnt))

    return status, cnt.value


##
# tibrv/queue.h
# tibrv_status tibrvQueue_GetPriority(
#                tibrvQueue                  eventQueue,
#                tibrv_u32*                  priority
#              );
#
_rv.tibrvQueue_GetPriority.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetPriority.restype = _c_tibrv_status

def tibrvQueue_GetPriority(eventQueue: tibrvQueue) -> (tibrv_status, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    que = _c_tibrvQueue(eventQueue)
    n = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetPriority(que, _ctypes.byref(n))

    return status, n.value


##
# tibrv/queue.h
# tibrv_status tibrvQueue_SetPriority(
#                tibrvQueue                  eventQueue,
#                tibrv_u32                   priority
#              );
#
_rv.tibrvQueue_SetPriority.argtypes = [_c_tibrvQueue, _c_tibrv_u32]
_rv.tibrvQueue_SetPriority.restype = _c_tibrv_status

def tibrvQueue_SetPriority(eventQueue: tibrvQueue, priority: int) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if priority is None:
        return TIBRV_INVALID_ARG

    que = _c_tibrvQueue(eventQueue)
    p = _c_tibrv_u32(priority)

    status = _rv.tibrvQueue_SetPriority(que, p)

    return status


##
# tibrv/queue.h
# tibrv_status tibrvQueue_GetLimitPolicy(
#                tibrvQueue                  eventQueue,
#                tibrvQueueLimitPolicy*      policy,
#                tibrv_u32*                  maxEvents,
#                tibrv_u32*                  discardAmount
#              );
#
_rv.tibrvQueue_GetLimitPolicy.argtypes = [_c_tibrvQueue,
                                          _ctypes.POINTER(_c_tibrvQueueLimitPolicy),
                                          _ctypes.POINTER(_c_tibrv_u32),
                                          _ctypes.POINTER(_c_tibrv_u32)]
_rv.tibrvQueue_GetLimitPolicy.restype = _c_tibrv_status

def tibrvQueue_GetLimitPolicy(eventQueue: tibrvQueue) -> (tibrv_status, int, int, int):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    que = _c_tibrvQueue(eventQueue)
    p = _c_tibrvQueueLimitPolicy(0)
    m = _c_tibrv_u32(0)
    d = _c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetLimitPolicy(que, _ctypes.byref(p), _ctypes.byref(m), _ctypes.byref(d))

    return status, p.value, m.value, d.value


##
# tibrv/queue.h
# tibrv_status tibrvQueue_SetLimitPolicy(
#                tibrvQueue                  eventQueue,
#                tibrvQueueLimitPolicy       policy,
#                tibrv_u32                   maxEvents,
#                tibrv_u32                   discardAmount
#              );
#
_rv.tibrvQueue_SetLimitPolicy.argtypes = [_c_tibrvQueue,
                                          _c_tibrvQueueLimitPolicy,
                                          _c_tibrv_u32,
                                          _c_tibrv_u32]
_rv.tibrvQueue_SetLimitPolicy.restype = _c_tibrv_status

def tibrvQueue_SetLimitPolicy(eventQueue: tibrvQueue, policy: int, maxEvents: int,
                              discardAmount: int) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    if policy is None or maxEvents is None or discardAmount is None:
        return TIBRV_INVALID_ARG

    que = _c_tibrvQueue(eventQueue)
    p = _c_tibrvQueueLimitPolicy(int(policy))
    m = _c_tibrv_u32(int(maxEvents))
    d = _c_tibrv_u32(int(discardAmount))

    status = _rv.tibrvQueue_SetLimitPolicy(que, p, m, d)
    return status



##
# tibrv/queue.h
# tibrv_status tibrvQueue_SetName(
#                tibrvQueue                  eventQueue,
#                const char*                 queueName
#              );
#
_rv.tibrvQueue_SetName.argtypes = [_c_tibrvQueue, _ctypes.c_char_p]
_rv.tibrvQueue_SetName.restype = _c_tibrv_status

def tibrvQueue_SetName(eventQueue: tibrvQueue, queueName: str) -> tibrv_status:

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    if queueName is None:
        return TIBRV_INVALID_ARG

    que = _c_tibrvQueue(eventQueue)
    sz = _cstr(queueName)

    status = _rv.tibrvQueue_SetName(que, sz)
    return status


##
# tibrv/queue.h
# tibrv_status tibrvQueue_GetName(
#                tibrvQueue                  eventQueue,
#                const char**                queueName
#              );
#
_rv.tibrvQueue_GetName.argtypes = [_c_tibrvQueue, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvQueue_GetName.restype = _c_tibrv_status

def tibrvQueue_GetName(eventQueue: tibrvQueue) -> (tibrv_status, str):

    if eventQueue is None or eventQueue == 0:
        return TIBRV_INVALID_QUEUE

    que = _c_tibrvQueue(eventQueue)
    sz = _ctypes.c_char_p()

    status = _rv.tibrvQueue_GetName(que, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# UNIMPLEMENTED
# tibrvQueue_SetHook
# tibrvQueue_GetHook
# tibrvQueue_RemoveHook
