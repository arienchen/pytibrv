##
# tibrv/queue.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.0 20161211 ARIEN
#
# DESCRIPTIONS
# ---------------------------------------------------
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
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
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161211 ARIEN V1.0
#   CREATED
#
##
import ctypes as _ctypes
from .status import *
from .api import _rv, _cstr, _pystr

##-----------------------------------------------------------------------------
## TibrvQueue
##-----------------------------------------------------------------------------

## tibrv/queue.h
# tibrv_status tibrvQueue_Create(
#                tibrvQueue*                 eventQueue
#              );
#
_rv.tibrvQueue_Create.argtypes = [_ctypes.POINTER(c_tibrvQueue)]
_rv.tibrvQueue_Create.restype = c_tibrv_status


def tibrvQueue_Create() -> (tibrv_status, tibrvQueue):

    que = c_tibrvQueue(0)

    status = _rv.tibrvQueue_Create(_ctypes.byref(que))

    return status, que.value

##
# tibrv/queue.h
# tibrv_status tibrvQueue_TimedDispatch(
#                tibrvQueue                  eventQueue,
#                tibrv_f64                   timeout
#              );
#
_rv.tibrvQueue_TimedDispatch.argtypes = [c_tibrvQueue, c_tibrv_f64]
_rv.tibrvQueue_TimedDispatch.restype = c_tibrv_status

def tibrvQueue_TimedDispatch(eventQueue:tibrvQueue, timeout: float) -> tibrv_status :

    que = c_tibrvQueue(eventQueue)
    t = c_tibrv_f64(timeout)

    status = _rv.tibrvQueue_TimedDispatch(que, t)

    return status

def tibrvQueue_Dispatch(eventQueue:tibrvQueue) -> tibrv_status :
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_WAIT_FOREVER)

def tibrvQueue_Poll(eventQueue:tibrvQueue) -> tibrv_status :
    return tibrvQueue_TimedDispatch(eventQueue, TIBRV_NO_WAIT)


##
# tibrv/queue.h
# tibrv_status tibrvQueue_TimedDispatchOneEvent(
#                tibrvQueue                  queue,
#                tibrv_f64                   waitTime
#              );
#
_rv.tibrvQueue_TimedDispatchOneEvent.argtypes = [c_tibrvQueue, c_tibrv_f64]
_rv.tibrvQueue_TimedDispatchOneEvent.restype = c_tibrv_status


def tibrvQueue_TimedDispatchOneEvent(eventQueue: tibrvQueue, waitTime: float) -> tibrv_status:

    que = c_tibrvQueue(eventQueue)
    t = c_tibrv_f64(waitTime)

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
_rv.tibrvQueue_DestroyEx.argtypes = [c_tibrvQueue, _ctypes.c_void_p, _ctypes.c_void_p]
_rv.tibrvQueue_DestroyEx.restype = c_tibrv_status

def tibrvQueue_DestroyEx(eventQueue:tibrvQueue, completeCallback :c_tibrvQueueOnComplete,  closure) -> tibrv_status :

    que = c_tibrvQueue(eventQueue)

    # TODO
    cb = None
    cz = None

    status = _rv.tibrvQueue_DestroyEx(que, cb, cz)

    return status


def tibrvQueue_Destroy(eventQueue:tibrvQueue) -> tibrv_status :

    status = tibrvQueue_DestroyEx(eventQueue, None, None)

    return status

##
# tibrv/queue.h
# tibrv_status tibrvQueue_GetCount(
#                tibrvQueue                  eventQueue,
#                tibrv_u32*                  numEvents
#              );
#
_rv.tibrvQueue_GetCount.argtypes = [c_tibrvQueue, _ctypes.POINTER(c_tibrv_u32)]
_rv.tibrvQueue_GetCount.restype = c_tibrv_status


def tibrvQueue_GetCount(eventQueue:tibrvQueue) -> (tibrv_status, int):

    que = c_tibrvQueue(eventQueue)
    cnt = c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetCount(que, _ctypes.byref(cnt))

    return status, cnt.value


##
# tibrv/queue.h
# tibrv_status tibrvQueue_GetPriority(
#                tibrvQueue                  eventQueue,
#                tibrv_u32*                  priority
#              );
#
_rv.tibrvQueue_GetPriority.argtypes = [c_tibrvQueue, _ctypes.POINTER(c_tibrv_u32)]
_rv.tibrvQueue_GetPriority.restype = c_tibrv_status

def tibrvQueue_GetPriority(eventQueue:tibrvQueue) -> (tibrv_status, int):

    que = c_tibrvQueue(eventQueue)
    n = c_tibrv_u32(0)

    status = _rv.tibrvQueue_GetPriority(que, _ctypes.byref(n))

    return status, n.value


##
# tibrv/queue.h
# tibrv_status tibrvQueue_SetPriority(
#                tibrvQueue                  eventQueue,
#                tibrv_u32                   priority
#              );
#
_rv.tibrvQueue_SetPriority.argtypes = [c_tibrvQueue, c_tibrv_u32]
_rv.tibrvQueue_SetPriority.restype = c_tibrv_status

def tibrvQueue_SetPriority(eventQueue:c_tibrvQueue, priority: int) -> tibrv_status:

    que = c_tibrvQueue(eventQueue)
    p = c_tibrv_u32(int(priority))

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
_rv.tibrvQueue_GetLimitPolicy.argtypes = [c_tibrvQueue,
                                          _ctypes.POINTER(c_tibrvQueueLimitPolicy),
                                          _ctypes.POINTER(c_tibrv_u32),
                                          _ctypes.POINTER(c_tibrv_u32)]
_rv.tibrvQueue_GetLimitPolicy.restype = c_tibrv_status

def tibrvQueue_GetLimitPolicy(eventQueue:tibrvQueue) -> (tibrv_status,int,int,int) :

    que = c_tibrvQueue(eventQueue)
    p = c_tibrvQueueLimitPolicy(0)
    m = c_tibrv_u32(0)
    d = c_tibrv_u32(0)

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
_rv.tibrvQueue_SetLimitPolicy.argtypes = [c_tibrvQueue,c_tibrvQueueLimitPolicy, c_tibrv_u32, c_tibrv_u32]
_rv.tibrvQueue_SetLimitPolicy.restype = c_tibrv_status

def tibrvQueue_SetLimitPolicy(eventQueue:tibrvQueue, policy:int, maxEvents:int, discardAmount:int) -> tibrv_status :

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    que = c_tibrvQueue(eventQueue)
    p = c_tibrvQueueLimitPolicy(int(policy))
    m = c_tibrv_u32(int(maxEvents))
    d = c_tibrv_u32(int(discardAmount))

    status = _rv.tibrvQueue_SetLimitPolicy(que, p, m, d)
    return status



##
# tibrv/queue.h
# tibrv_status tibrvQueue_SetName(
#                tibrvQueue                  eventQueue,
#                const char*                 queueName
#              );
#
_rv.tibrvQueue_SetName.argtypes = [c_tibrvQueue, _ctypes.c_char_p]
_rv.tibrvQueue_SetName.restype = c_tibrv_status

def tibrvQueue_SetName(eventQueue:tibrvQueue, queueName:str) -> tibrv_status :

    if eventQueue == TIBRV_DEFAULT_QUEUE:
        return TIBRV_INVALID_QUEUE

    que = c_tibrvQueue(eventQueue)
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
_rv.tibrvQueue_GetName.argtypes = [c_tibrvQueue, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvQueue_GetName.restype = c_tibrv_status

def tibrvQueue_GetName(eventQueue:tibrvQueue) -> (tibrv_status, str):

    que = c_tibrvQueue(eventQueue)
    sz = _ctypes.c_char_p()

    status = _rv.tibrvQueue_GetName(que, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# UNIMPLEMENTED
# tibrvQueue_SetHook
# tibrvQueue_GetHook
# tibrvQueue_RemoveHook

class TibrvQueue :
    DISCARD_NONE    = TIBRVQUEUE_DISCARD_NONE
    DISCARD_FIRST   = TIBRVQUEUE_DISCARD_FIRST
    DISCARD_LAST    = TIBRVQUEUE_DISCARD_LAST
    DISCARD_NEW     = TIBRVQUEUE_DISCARD_NEW

    def __init__(self):
        self._que = TIBRV_DEFAULT_QUEUE
        self._err = None
        self._policy = 0
        self._maxEvents = 0
        self._discard = 0

    def __del__(self):
        self.destroy()

    def id(self):
        return self._que

    def create(self, name : str = None) -> tibrv_status:
        if self._que != 0 and self._que != TIBRV_DEFAULT_QUEUE:
            self.destroy()

        status, que = tibrvQueue_Create();
        self._err = TibrvStatus.error(status)
        if status == TIBRV_OK:
            self._que = que

            s,p,m,d = tibrvQueue_GetLimitPolicy(que)
            if s == TIBRV_OK:
                self._policy = p
                self._maxEvents = m
                self._discard = d

            if name is not None :
                tibrvQueue_SetName(que, name)

        return status;

    def destroy(self) -> tibrv_status :
        if self._que == 0 or self._que == TIBRV_DEFAULT_QUEUE:
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvQueue_Destroy(self._que)
        self._err = TibrvStatus.error(status)

        self._que = 0

        return status


    @property
    def name(self) -> str:
        ret = None
        status, ret = tibrvQueue_GetName(self._que)
        self._err = TibrvStatus.error(status)

        return ret

    @name.setter
    def name(self, sz : str) -> None:
        status = tibrvQueue_SetName(self._que, sz)
        self._err = TibrvStatus.error(status)

    def dispatch(self) -> int:
        status = tibrvQueue_Dispatch(self._que)
        self._err = TibrvStatus.error(status)
        return status

    @property
    def count(self) -> int:
        ret = None
        status, ret = tibrvQueue_GetCount(self._que)
        self._err = TibrvStatus.error(status)

        return ret

    def setPolicy(self, policy : int , maxEvents : int , discardAmount : int ) -> tibrv_status :
        status = tibrvQueue_SetLimitPolicy(self._que, policy, maxEvents, discardAmount)
        self._err = TibrvStatus.error(status)
        if status == TIBRV_OK:
            self._policy = int(policy)
            self._maxEvents = int(maxEvents)
            self._discard = int(discardAmount)

        return status

    @property
    def policy(self) -> str:
        return self._policy

    @property
    def maxEvents(self) -> str:
        return self._maxEvents

    @property
    def discardAmount(self) -> str:
        return self._discard

    @property
    def priority(self) -> str:
        ret = None
        status, ret = tibrvQueue_GetPriority(self._que)
        self._err = TibrvStatus.error(status)

        return ret

    @priority.setter
    def priority(self, val: int) -> None:
        status = tibrvQueue_SetPriority(self._que, val)
        self._err = TibrvStatus.error(status)

    def poll(self) -> tibrv_status:
        status = tibrvQueue_Poll(self._que)
        self._err = TibrvStatus.error(status)
        return status


    def timedDispatch(self, timeout : float) -> tibrv_status:
        status = tibrvQueue_TimedDispatch(self._que, timeout)
        self._err = TibrvStatus.error(status)
        return status

    @property
    def error(self) -> TibrvError :
        return self._err

