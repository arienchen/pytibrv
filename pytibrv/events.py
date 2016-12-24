##
# pytibrv/events.py
#   TIBRV Library for PYTHON
#   tibrvEvent_XXX
# 
# LAST MODIFIED : V1.0 20161211 ARIEN arien.chen@gmail.com 
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
#    IT WOULD SEGMENT FAULT WHEN my_callback was triggered.
#    The local variable:cb would store the callback function pointer
#    and it would be garbage collected when reg_callback() was returned,
#    
#    Callback is async. When C try to 'callback' the Python Function,
#    it would access a destroy object in Python.
#    then it cause SEGFAULT.
#
#    I found this issue only in OSX, Linux seems OK.
#
#    BUGFIX:
#       create a dict variable to store the CFUNCTYPE objects
#       rather than a local variable inner a function
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
#    (3) Call C API to pass Python my_obj
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
#       cnt = int(1)
#       ...
#       reg_func(cb, py_object(cnt))
#       ...
#       cnt = cnt + 1           -> cnt would refer to a new int object, not 1
#                               -> my_func would always get the original object (=1)
#                               -> Python pass object reference BY VALUE.   
#
#   (6) GC Issue
#       like as GC issue of CFUNCTYPE()/Callback
#       if closure object was create inner a function,
#       this local object would be GC and destroyed when when function returned
#       it cause Segment Fault either.
#
# 3. callback function inner class 
#    DONT pass class function into API
#    All class function predefine 1'st parameter as 'self'. 
#    
#    If you prefer calling wrapper API, then declare callback as module function.
#    If you use class function for callback, please user pytibrv Python Object Model
#    ex: TibrvListener, TibrvMsgCallback  
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
# -------------------------------------------------------
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
##

import ctypes as _ctypes
from .types import tibrv_status, tibrvTransport, tibrvQueue, tibrvEvent, tibrvEventType

from .status import TIBRV_OK
from .api import _rv, _cstr, _pystr, \
                 _c_tibrvTransport, _c_tibrvQueue, _c_tibrvEvent, _c_tibrvEventType, \
                 _c_tibrvEventOnComplete, _c_tibrvEventCallback, _c_tibrvEventVectorCallback, \
                 _c_tibrv_status, _c_tibrv_f64


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
_rv.tibrvEvent_CreateListener.argtypes = [_ctypes.POINTER(_c_tibrvEvent),
                                          _c_tibrvQueue,
                                          _c_tibrvEventCallback,
                                          _c_tibrvTransport,
                                          _ctypes.c_char_p,
                                          _ctypes.py_object]
_rv.tibrvEvent_CreateListener.restype = _c_tibrv_status

def tibrvEvent_CreateListener(queue:tibrvQueue, callback, transport:tibrvTransport, subject:str, closure=None) \
                             -> (tibrv_status, tibrvEvent):

    ev = _c_tibrvEvent(0)
    que = _c_tibrvQueue(queue)
    cb = _c_tibrvEventCallback(callback)
    tx = _c_tibrvTransport(transport)
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
_rv.tibrvEvent_CreateVectorListener.argtypes = [_ctypes.POINTER(_c_tibrvEvent),
                                                _c_tibrvQueue,
                                                _c_tibrvEventVectorCallback,
                                                _c_tibrvTransport,
                                                _ctypes.c_char_p,
                                                _ctypes.py_object]
_rv.tibrvEvent_CreateVectorListener.restype = _c_tibrv_status

def tibrvEvent_CreateVectorListener(queue:tibrvQueue, callback, transport:tibrvTransport, subject:str, closure)\
                                   -> (tibrv_status, tibrvEvent):

    ev = _c_tibrvEvent(0)
    que = _c_tibrvQueue(queue)
    cb = _c_tibrvEventVectorCallback(callback)
    tx = _c_tibrvTransport(transport)
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
_rv.tibrvEvent_CreateTimer.argtypes = [_ctypes.POINTER(_c_tibrvEvent),
                                       _c_tibrvQueue,
                                       _c_tibrvEventCallback,
                                       _c_tibrv_f64,
                                       _ctypes.py_object]
_rv.tibrvEvent_CreateTimer.restype = _c_tibrv_status

def tibrvEvent_CreateTimer(queue: tibrvQueue, callback, interval: float, closure=None) \
                           -> (tibrv_status, tibrvEvent):

    ev = _c_tibrvEvent(0)
    que = _c_tibrvQueue(queue)
    cb = _c_tibrvEventCallback(callback)
    n = _c_tibrv_f64(interval)

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
_rv.tibrvEvent_DestroyEx.argtypes = [_c_tibrvEvent, _c_tibrvEventOnComplete]
_rv.tibrvEvent_DestroyEx.restype = _c_tibrv_status

def tibrvEvent_Destroy(event:tibrvEvent) -> tibrv_status:

    ev = _c_tibrvEvent(event)

    # tibrvEventOnComplete IS NOT SUPPORTED
    # plz refer the GC issue of callback
    cb = _c_tibrvEventOnComplete(0)

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
_rv.tibrvEvent_GetType.argtypes = [_c_tibrvEvent, _ctypes.POINTER(_c_tibrvEventType)]
_rv.tibrvEvent_GetType.restype = _c_tibrv_status

def tibrvEvent_GetType(event:tibrvEvent) -> (tibrv_status, tibrvEventType):

    ev = _c_tibrvEvent(event)
    ty = _c_tibrvEventType(0)

    status = _rv.tibrvEvent_GetType(ev, _ctypes.byref(ty))

    return status, ty.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetQueue(
#                tibrvEvent                  event,
#                tibrvQueue*                 queue
#              );
#
_rv.tibrvEvent_GetQueue.argtypes = [_c_tibrvEvent, _ctypes.POINTER(_c_tibrvQueue)]
_rv.tibrvEvent_GetQueue.restype = _c_tibrv_status

def tibrvEvent_GetQueue(event:tibrvEvent) -> (tibrv_status, tibrvQueue):

    ev = _c_tibrvEvent(event)
    que = _c_tibrvQueue()

    status = _rv.tibrvEvent_GetQueue(ev, _ctypes.byref(que))

    return status, que.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetListenerSubject(
#                tibrvEvent                  event,
#                const char**                subject
#              );
#
_rv.tibrvEvent_GetListenerSubject.argtypes = [_c_tibrvEvent, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvEvent_GetListenerSubject.restype = _c_tibrv_status

def tibrvEvent_GetListenerSubject(event: tibrvEvent) -> (tibrv_status, str):

    ev = _c_tibrvEvent(event)
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
_rv.tibrvEvent_GetListenerTransport.argtypes = [_c_tibrvEvent, _ctypes.POINTER(_c_tibrvTransport)]
_rv.tibrvEvent_GetListenerTransport.restype = _c_tibrv_status

def tibrvEvent_GetListenerTransport(event: tibrvEvent) -> (tibrv_status, tibrvTransport):

    ev = _c_tibrvEvent(event)
    tx = _c_tibrvTransport(0)

    status = _rv.tibrvEvent_GetListenerTransport(ev, _ctypes.byref(tx))

    return status, tx.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_GetTimerInterval(
#                tibrvEvent                  event,
#                tibrv_f64*                  interval
#              );
#
_rv.tibrvEvent_GetTimerInterval.argtypes = [_c_tibrvEvent, _ctypes.POINTER(_c_tibrv_f64)]
_rv.tibrvEvent_GetTimerInterval.restype = _c_tibrv_status

def tibrvEvent_GetTimerInterval(event: tibrvEvent) -> (tibrv_status, float):

    ev = _c_tibrvEvent(event)
    n = _c_tibrv_f64(0)

    status = _rv.tibrvEvent_GetTimerInterval(ev, _ctypes.byref(n))

    return status, n.value


##
# tibrv/events.h
# tibrv_status tibrvEvent_ResetTimerInterval(
#                tibrvEvent                  event,
#                tibrv_f64                   newInterval
#              );
#
_rv.tibrvEvent_ResetTimerInterval.argtypes = [_c_tibrvEvent, _c_tibrv_f64]
_rv.tibrvEvent_ResetTimerInterval.restype = _c_tibrv_status

def tibrvEvent_ResetTimerInterval(event: tibrvEvent, newInterval:float) -> tibrv_status:

    ev = _c_tibrvEvent(event)
    n = _c_tibrv_f64(newInterval)

    status = _rv.tibrvEvent_ResetTimerInterval(ev, n)

    return status

