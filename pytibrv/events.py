##
# pytibrv/events.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.0 20161211 ARIEN
#
# DESCRIPTIONS
# ---------------------------------------------------
# 1. Callback cause Segment Fault in OSX
#    for detail: http://osdir.com/ml/python.ctypes/2008-05/msg00010.html
#
#    sample code as below:
#
#    _clib = ctypes.cdll.LoadLibrary()
#    _callback = CFUNCTYPE(...)
#    ...
#    def my_callback() :
#       ...
#
#    def reg_callback() :
#       ...
#       cb = _callback(my_calback)
#       # Call C Lib to register
#       _clib.register(cb)
#       ...
#
#    IT WOULD SEGMENT FAULT WHEN my_callback was triggered
#    object cb would store the callback function pointer
#    when reg_callback() was returned,
#    cb would be garbage collected
#    when C try to 'callback' the Python Function,
#    it would access a destroy object in Python.
#
#    I found this issue only in OSX, Linux seems OK.
#
#    BUGFIX:
#       create a dict variable to store the CFUNCTYPE objects
#
#
# 2. Callback Closure as Python Object
#    plz refer : http://stackoverflow.com/questions/3245859/back-casting-a-ctypes-py-object-in-a-callback
#
#    Hints:
#    (1) Declare Callback prototype as c_void_p
#           callback = CFUNCTYPE( , c_void_p, ...)
#
#    (2) Declare C API as py_object
#           reg_func.argtypes = [ , py_object, ...]
#
#
#    (3) Call C API to pass Pythoon my_obj
#           cb = callback(my_func)
#           reg_func( cb, py_object(my_obj), ...)
#
#    (4) Cast in Callback
#        def my_func(,closure,...):
#           obj = cast(closure, py_object).value
#           # obj is my_obj
#
#   (5) Beware for immutable object, such as Python native data type: bool, int, float, str
#       for example:
#
#       cnt = 1
#       ...
#       reg_func(cb, py_object(cnt))
#       ...
#       cnt = cnt + 1           -> cnt would refer to a new object, not 1
#                               -> my_func would get the original object (=1) always
#
#   (6) GC Issue
#       like as GC issue of CFUNCTYPE()
#       if closure object was create inner a function,
#       when function returned the closure object would be GC and destroyed.
#       it cause Segment Fault either.
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvEvent_CreateListener
#   tibrvEvent_CreateTimer
#   tibrvEvent_CreateVectorListener
#   tibrvEvent_DestroyEx
#   tibrvEvent_GetListenerSubject
#   tibrvEvent_GetListenerTransport
#   tibrvEvent_GetTimerInterval
#   tibrvEvent_GetType
#   tibrvEvent_GetQueue
#   tibrvEvent_ResetTimerInterval
#
#  *tibrvEventOnComplete
#  *tibrvEvent_CreateGroupVectorListener
#  *tibrvEvent_CreateIO
#  *tibrvEvent_GetIOSource
#  *tibrvEvent_GetIOType
#
# CHANGED LOGS
# ---------------------------------------------------
# 20161211 ARIEN V1.0
#   CREATED
#

import ctypes as _ctypes
from .queue import *
from .tport import *
from .api import _rv, _cstr, _pystr

# keep callback/closure object from GC
# key = tibrvEvent
__callback = {}
__closure  = {}

def __reg(event, func, closure):
    __callback[event] = func
    if closure is not None:
        __closure[event] = closure

    return

def __unreg(event):
    if event in __callback:
        del __callback[event]

    if event in __closure:
        del __closure[event]

    return

# Helper function to cast closure to Python Object
def tibrvClosure(closure) -> object:
    return _ctypes.cast(closure, _ctypes.py_object).value

##-----------------------------------------------------------------------------
## TibrvListener
##-----------------------------------------------------------------------------
##
# tibrv/events.h
# tibrv_status tibrvEvent_CreateListener(
#                tibrvEvent*                 event,
#                tibrvQueue                  queue,
#                tibrvEventCallback          callback,
#                tibrvTransport              transport,
#                const char*                 subject,
#                const void*                 closure
#              );
#
_rv.tibrvEvent_CreateListener.argtypes = [_ctypes.POINTER(c_tibrvEvent),
                                          c_tibrvQueue,
                                          c_tibrvEventCallback,
                                          c_tibrvTransport,
                                          _ctypes.c_char_p,
                                          _ctypes.py_object]
_rv.tibrvEvent_CreateListener.restype = c_tibrv_status

def tibrvEvent_CreateListener(queue:tibrvQueue, callback, transport:tibrvTransport, subject:str, closure) -> tibrv_status:

    ev = c_tibrvEvent(0)
    que = c_tibrvQueue(queue)
    cb = c_tibrvEventCallback(callback)
    tx = c_tibrvTransport(transport)
    subj = _cstr(subject)

    cz = _ctypes.py_object(closure)

    status = _rv.tibrvEvent_CreateListener(_ctypes.byref(ev), que, cb, tx, subj, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ev.value, cb, cz)

    return status, ev.value

##
# tibrv/events.h
# tibrv_status tibrvEvent_CreateVectorListener(
#                tibrvEvent*                 event,
#                tibrvQueue                  queue,
#                tibrvEventVectorCallback    callback,
#                tibrvTransport              transport,
#                const char*                 subject,
#                const void*                 closure
#              );
#
_rv.tibrvEvent_CreateVectorListener.argtypes = [_ctypes.POINTER(c_tibrvEvent),
                                                c_tibrvQueue,
                                                c_tibrvEventVectorCallback,
                                                c_tibrvTransport,
                                                _ctypes.c_char_p,
                                                _ctypes.py_object]
_rv.tibrvEvent_CreateVectorListener.restype = c_tibrv_status

def tibrvEvent_CreateVectorListener(queue:tibrvQueue, callback, transport:tibrvTransport, subject:str, closure) -> tibrv_status :

    ev = c_tibrvEvent(0)
    que = c_tibrvQueue(queue)
    cb = c_tibrvEventVectorCallback(callback)
    tx = c_tibrvTransport(transport)
    subj = _cstr(subject)
    cz = _ctypes.py_object(closure)

    status = _rv.tibrvEvent_CreateVectorListener(_ctypes.byref(ev), que, cb, tx, subj, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ev.value, cb, cz)

    return status, ev.value


# tibrv_status tibrvEvent_CreateGroupVectorListener(
#                tibrvEvent*                     event,
#                tibrvQueue                      queue,
#                tibrvEventVectorCallback        cb,
#                tibrvTransport                  tport,
#                const char*                     subject,
#                const void*                     arg,
#                const void*                     msgGroupId
#              );
#


# tibrv_status tibrvEvent_CreateTimer(
#                tibrvEvent*                 event,
#                tibrvQueue                  queue,
#                tibrvEventCallback          callback,
#                tibrv_f64                   interval,
#                const void*                 closure
#              );
#
_rv.tibrvEvent_CreateTimer.argtypes = [_ctypes.POINTER(c_tibrvEvent),
                                       c_tibrvQueue,
                                       c_tibrvEventCallback,
                                       c_tibrv_f64,
                                       _ctypes.py_object]
_rv.tibrvEvent_CreateTimer.restype = c_tibrv_status

def tibrvEvent_CreateTimer(queue: tibrvQueue, callback, interval: float, closure=None) -> tibrv_status:

    ev = c_tibrvEvent(0)
    que = c_tibrvQueue(queue)
    cb = c_tibrvEventCallback(callback)
    n = c_tibrv_f64(interval)

    cz = _ctypes.py_object(closure)

    status = _rv.tibrvEvent_CreateTimer(_ctypes.byref(ev), que, cb, n, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ev.value, cb, cz)

    return status, ev.value



##
# tibrv/events.h
# tibrv_status tibrvEvent_DestroyEx(
#                tibrvEvent                  event,
#                tibrvEventOnComplete        completeCallback
#              );
#
_rv.tibrvEvent_DestroyEx.argtypes = [c_tibrvEvent, c_tibrvEventOnComplete]
_rv.tibrvEvent_DestroyEx.restype = c_tibrv_status

def tibrvEvent_DestroyEx(event:tibrvEvent) -> tibrv_status :

    ev = c_tibrvEvent(event)

    # tibrvEventOnComplete IS NOT SUPPORTED
    # plz refer the GC issue of callback
    cb = c_tibrvEventOnComplete(0)

    status = _rv.tibrvEvent_DestroyEx(ev, cb)

    if status == TIBRV_OK:
        __unreg(event)

    return status


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetType(
#                tibrvEvent                  event,
#                tibrvEventType*             type
#              );
#
_rv.tibrvEvent_GetType.argtypes = [c_tibrvEvent, _ctypes.POINTER(c_tibrvEventType)]
_rv.tibrvEvent_GetType.restype = c_tibrv_status

def tibrvEvent_GetType(event:tibrvEvent) -> tibrv_status :

    ev = c_tibrvEvent(event)
    ty = c_tibrvEventType(0)

    status = _rv.tibrvEvent_GetType(ev, _ctypes.byref(ty))

    return status, ty.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetQueue(
#                tibrvEvent                  event,
#                tibrvQueue*                 queue
#              );
#
_rv.tibrvEvent_GetQueue.argtypes = [c_tibrvEvent, _ctypes.POINTER(c_tibrvQueue)]
_rv.tibrvEvent_GetQueue.restype = c_tibrv_status

def tibrvEvent_GetQueue(event:tibrvEvent) -> tibrv_status :

    ev = c_tibrvEvent(event)
    que = c_tibrvQueue()

    status = _rv.tibrvEvent_GetQueue(ev, _ctypes.byref(que))

    return status, que.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetListenerSubject(
#                tibrvEvent                  event,
#                const char**                subject
#              );
#
_rv.tibrvEvent_GetListenerSubject.argtypes = [c_tibrvEvent, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvEvent_GetListenerSubject.restype = c_tibrv_status

def tibrvEvent_GetListenerSubject(event: tibrvEvent) -> tibrv_status:

    ev = c_tibrvEvent(event)
    sz = _ctypes.c_char_p(0)

    status = _rv.tibrvEvent_GetListenerSubject(ev, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetListenerTransport(
#                tibrvEvent                  event,
#                tibrvTransport*             transport
#              );
#
_rv.tibrvEvent_GetListenerTransport.argtypes = [c_tibrvEvent, _ctypes.POINTER(c_tibrvTransport)]
_rv.tibrvEvent_GetListenerTransport.restype = c_tibrv_status

def tibrvEvent_GetListenerTransport(event: tibrvEvent) -> tibrv_status:

    ev = c_tibrvEvent(event)
    tx = c_tibrvTransport(0)

    status = _rv.tibrvEvent_GetListenerTransport(ev, _ctypes.byref(tx))

    return status, tx.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetTimerInterval(
#                tibrvEvent                  event,
#                tibrv_f64*                  interval
#              );
#
_rv.tibrvEvent_GetTimerInterval.argtypes = [c_tibrvEvent, _ctypes.POINTER(c_tibrv_f64)]
_rv.tibrvEvent_GetTimerInterval.restype = c_tibrv_status

def tibrvEvent_GetTimerInterval(event: tibrvEvent) -> tibrv_status:

    ev = c_tibrvEvent(event)
    n = c_tibrv_f64(0)

    status = _rv.tibrvEvent_GetTimerInterval(ev, _ctypes.byref(n))

    return status, n.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_ResetTimerInterval(
#                tibrvEvent                  event,
#                tibrv_f64                   newInterval
#              );
#
_rv.tibrvEvent_ResetTimerInterval.argtypes = [c_tibrvEvent, c_tibrv_f64]
_rv.tibrvEvent_ResetTimerInterval.restype = c_tibrv_status

def tibrvEvent_ResetTimerInterval(event: tibrvEvent, newInterval:float) -> tibrv_status:

    ev = c_tibrvEvent(event)
    n = c_tibrv_f64(newInterval)

    status = _rv.tibrvEvent_ResetTimerInterval(ev, n)

    return status


class TibrvTimerCallback:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, event, closure):
        pass

    def _register(self):
        def _cb(event, msg, closure):
            if event != 0:
                ev = TibrvTimer(event)
            else:
                ev = None

            cz = tibrvClosure(closure)

            self.callback(ev, cz)

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

    def __init__(self, event : tibrvEvent = 0):
        self._err = None
        self._event = event

        if event != 0 :
            self._copied = True
        else:
            self._copied = False

    def id(self):
        return self._event

    def destroy(self):
        if self.id() == 0:
            return TIBRV_INVALID_EVENT

        status = tibrvEvent_DestroyEx(self._event)
        self._event = 0
        return status

    @property
    def error(self) -> TibrvError:
        return self._err

    def eventType(self):
        ret = None

        if self.id() == 0 :
            status = TIBRV_INVALID_EVENT
        else:
            status, ret = tibrvEvent_GetType(self.id())

        self._err = TibrvStatus.error(status)

        return ret


class TibrvTimer(TibrvEvent):

    def __init__(self, event:tibrvEvent = 0):
        super().__init__(event)


    def create(self, que:TibrvQueue, callback: TibrvTimerCallback, interval:float, closure = None) -> tibrv_status :
        if self._copied == True or self.id() != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if not isinstance(callback, TibrvTimerCallback):
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)
            return status

        ret = 0
        status, ret = tibrvEvent_CreateTimer(que.id(), callback._register(), interval, closure)

        if status == TIBRV_OK:
            self._event = ret

        self._err = TibrvStatus.error(status)
        return status

    @property
    def interval(self):
        ret = 0
        if self._event == 0:
            status = TIBRV_INVALID_EVENT
        else:
            status, ret = tibrvEvent_GetTimerInterval(self._event)

        self._err = TibrvStatus.error(status)

        return ret

    @interval.setter
    def interval(self, sec: float):
        if self._event == 0:
            status = TIBRV_INVALID_EVENT
        else:
            status = tibrvEvent_ResetTimerInterval(self._event, sec)

        self._err = TibrvStatus.error(status)



class TibrvListener(TibrvEvent):

    def __init__(self, event:tibrvEvent = 0):
        super().__init__(event)

    def create(self, que: TibrvQueue, callback: TibrvMsgCallback, tx: TibrvTx, subject: str, closure = None) -> tibrv_status :
        if self._copied == True :
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if not isinstance(callback, TibrvMsgCallback):
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)
            return status

        ret = 0
        status, ret = tibrvEvent_CreateListener(que.id(), callback._register(), tx.id(), subject, closure)

        if status == TIBRV_OK :
            self._event = ret

        self._err = TibrvStatus.error(status)
        return status

    def subject(self) -> str :
        ret = None
        if self._event == 0 :
            status = TIBRV_INVALID_EVENT
        else:
            status, ret = tibrvEvent_GetListenerSubject(self._event)

        self._err = TibrvStatus.error(status)

        return ret

    def queue(self) -> TibrvQueue :
        ret = None
        if self._event == 0 :
            status = TIBRV_INVALID_EVENT
        else:
            status, q = tibrvEvent_GetListenerSubject(self._event)
            if status == TIBRV_OK :
                ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret
