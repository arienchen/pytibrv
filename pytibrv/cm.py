##
# pytibrv/cm.py
#   TibrvCmTx               <- tibrvcmTransport_XXX
#   TibrvCmListener         <- tibrvcmEvent_XXX
#   TibrvCmMsg              <- tibrvMsg_XXX
#
# LAST MODIFIED : V1.0 20161226 ARIEN
#
# DESCRIPTIONS
# ------------------------------------------------------
# 1. TibrvCmTx is not a subclass of TibrvTx
#    TibrvCmListener is not a subclass of TibrvListener
#    TibrvCmMsg is derived from TibrvMsg
#
# 2. TibrvCmTx, TibrvCmListener both support OnComplete callback
#    like common callback, the callback pointer would be stored in __callback[]
#    to prevent GC before callback.
#    BUT there is no way to detach from __callback[]
#    I ASSUME the OnComplete callback was assigned at process termination
#
#    Please be NOTICED this would cause memory leak
#    if OnComplete callback in loop and in life of process.
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvcm_Version
#   tibrvcmTransport_Create
#   tibrvcmTransport_Send
#   tibrvcmTransport_SendRequest
#   tibrvcmTransport_SendReply
#   tibrvcmTransport_GetTransport
#   tibrvcmTransport_GetName
#   tibrvcmTransport_GetRelayAgent
#   tibrvcmTransport_GetLedgerName
#   tibrvcmTransport_GetSyncLedger
#   tibrvcmTransport_GetRequestOld
#   tibrvcmTransport_AllowListener
#   tibrvcmTransport_DisallowListener
#   tibrvcmTransport_AddListener
#   tibrvcmTransport_RemoveListener
#   tibrvcmTransport_RemoveSendState
#   tibrvcmTransport_SyncLedger
#   tibrvcmTransport_ConnectToRelayAgent
#   tibrvcmTransport_DisconnectFromRelayAgent
#   tibrvcmTransport_DestroyEx
#   tibrvcmEvent_CreateListener
#   tibrvcmEvent_GetQueue
#   tibrvcmEvent_GetListenerSubject
#   tibrvcmEvent_GetListenerTransport
#   tibrvcmEvent_SetExplicitConfirm
#   tibrvcmEvent_ConfirmMsg
#   tibrvcmEvent_DestroyEx
#   tibrvMsg_GetCMSender
#   tibrvMsg_GetCMSequence
#   tibrvMsg_GetCMTimeLimit
#   tibrvMsg_SetCMTimeLimit
#   tibrvcmTransport_GetDefaultCMTimeLimit
#   tibrvcmTransport_SetDefaultCMTimeLimit
#   tibrvcmTransport_ReviewLedger
#   tibrvcmTransport_ExpireMessages
#
#
# CHANGED LOGS
# ------------------------------------------------------
# 20161226 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
import ctypes as _ctypes
from .types import tibrv_status
from . import _load, _func

from .api import _cstr, _pystr, \
                 _c_tibrv_status, _c_tibrvId,  _c_tibrvTransport, _c_tibrvQueue, _c_tibrvMsg, \
                 _c_tibrv_bool, _c_tibrv_u64, _c_tibrv_f64, _c_tibrv_str, \
                 _c_tibrvEventOnComplete, \
                 tibrvId, tibrvQueue, tibrvTransport, tibrvMsg

from .status import TIBRV_OK, TIBRV_INVALID_TRANSPORT, TIBRV_INVALID_ARG, TIBRV_INVALID_EVENT, \
                    TIBRV_INVALID_MSG, TIBRV_INVALID_QUEUE, TIBRV_INVALID_CALLBACK

# module variable
_rvcm = _load('tibrvcm')

# Data Types
tibrvcmTransport        = tibrvId
tibrvcmEvent            = tibrvId

_c_tibrvcmTransport     = _c_tibrvId
_c_tibrvcmEvent         = _c_tibrvId


# CONSTANTS
TIBRVCM_DEFAULT_TRANSPORT_TIMELIMIT = 0
TIBRVCM_CANCEL                      = True
TIBRVCM_PERSIST                     = False


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

##
# Callback
# typedef void (*tibrvcmTransportOnComplete) (
#                   tibrvcmTransport	destroyedTransport,
#                   void*			    closure
#                  );
#
_c_tibrvcmTransportOnComplete = _func(_ctypes.c_void_p, _c_tibrvcmTransport, _ctypes.c_void_p)

##
# tibrv/cm.h
# typedef void (*tibrvcmEventCallback) (
#                   tibrvcmEvent        event,
#                   tibrvMsg            message,
#                   void*               closure
#                  );
#
_c_tibrvcmEventCallback = _func(_ctypes.c_void_p, _c_tibrvcmEvent, _c_tibrvMsg, _ctypes.c_void_p)

##
# tibrv/cm.h
# typedef void* (*tibrvcmReviewCallback) (
#                   tibrvcmTransport            cmTransport,
#                   const char*                 subject,
#                   tibrvMsg                    message,
#                   void*                       closure);
#
_c_tibrvcmReviewCallback = _func(_ctypes.c_void_p, _c_tibrvcmEvent, _c_tibrv_str, _c_tibrvMsg, _ctypes.c_void_p)


##
# tibrv/cm.h
# const char * tibrvcm_Version(void)
#
_rvcm.tibrvcm_Version.argtypes = []
_rvcm.tibrvcm_Version.restype = _ctypes.c_char_p

def tibrvcm_Version() -> str:
    sz = _rvcm.tibrv_Version()
    return sz.decode()


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_Create(
#                   tibrvcmTransport*           cmTransport,
#                   tibrvTransport              transport,
#                   const char*                 cmName,
#                   tibrv_bool                  requestOld,
#                   const char*                 ledgerName,
#                   tibrv_bool                  syncLedger,
#                   const char*                 relayAgent
#               );
#
_rvcm.tibrvcmTransport_Create.argtypes = [_ctypes.POINTER(_c_tibrvcmTransport),
                                          _c_tibrvTransport,
                                          _c_tibrv_str,
                                          _c_tibrv_bool,
                                          _c_tibrv_str,
                                          _c_tibrv_bool,
                                          _c_tibrv_str]

_rvcm.tibrvcmTransport_Create.restype = _c_tibrv_status

def tibrvcmTransport_Create(tx: tibrvTransport, cmName: str, requestOld: bool = True,
                            ledgerName: str = None, syncLedger: bool = False, relayAgent: str = None) \
                            -> (tibrv_status, tibrvcmTransport):

    if tx == 0 or tx is None:
        return TIBRV_INVALID_TRANSPORT

    cmtx = _c_tibrvcmTransport(0)

    try:
        tx = _c_tibrvTransport(tx)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        # cmName allow None -> auto-generated
        name = _cstr(cmName)
        req_old = _c_tibrv_bool(requestOld)
        ledger = _cstr(ledgerName)
        sync = _c_tibrv_bool(syncLedger)
        agent = _cstr(relayAgent)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_Create(_ctypes.byref(cmtx), tx, name, req_old, ledger, sync, agent)

    return status, cmtx.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_Send(
#                   tibrvcmTransport        cmTransport,
#                   tibrvMsg                message
#               );
#
_rvcm.tibrvcmTransport_Send.argtypes = [_c_tibrvcmTransport, _c_tibrvMsg]
_rvcm.tibrvcmTransport_Send.restype = _c_tibrv_status

def tibrvcmTransport_Send(cmTransport: tibrvcmTransport, message: tibrvMsg) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rvcm.tibrvcmTransport_Send(cmtx, msg)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SendRequest(
#                   tibrvcmTransport            cmTransport,
#                   tibrvMsg                    message,
#                   tibrvMsg*                   reply,
#                   tibrv_f64                   idleTimeout
#               );
_rvcm.tibrvcmTransport_SendRequest.argtypes = [_c_tibrvcmTransport,
                                               _c_tibrvMsg,
                                               _ctypes.POINTER(_c_tibrvMsg),
                                               _c_tibrv_f64]
_rvcm.tibrvcmTransport_SendRequest.restype = _c_tibrv_status

def tibrvcmTransport_SendRequest(cmTransport: tibrvcmTransport, message: tibrvMsg,
                                 idleTimeout: float) -> (tibrv_status, tibrvMsg):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    if idleTimeout is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    ret = _c_tibrvMsg(0)

    try:
        wait_time = _c_tibrv_f64(idleTimeout)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_Send(cmtx, msg, _ctypes.byref(ret), wait_time)

    return status, ret.value

##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SendReply(
#                   tibrvcmTransport            cmTransport,
#                   tibrvMsg                    message,
#                   tibrvMsg                    requestMessage
#               );
#
_rvcm.tibrvcmTransport_SendReply.argtypes = [_c_tibrvcmTransport, _c_tibrvMsg, _c_tibrvMsg]
_rvcm.tibrvTransport_SendReply.restype = _c_tibrv_status

def tibrvcmTransport_SendReply(cmTransport: tibrvcmTransport, message: tibrvMsg, requestMessage: tibrvMsg) \
                              -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    if requestMessage == 0 or requestMessage is None:
        return TIBRV_INVALID_MSG

    try:
        tx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        msg = _c_tibrvMsg(message)
        req = _c_tibrvMsg(requestMessage)
    except:
        return TIBRV_INVALID_MSG

    status = _rvcm.tibrvcmTransport_SendReply(tx, msg, req)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetTransport(
#                   tibrvcmTransport            cmTransport,
#                   tibrvTransport*             transport
#               );
#
_rvcm.tibrvcmTransport_GetTransport.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrvTransport)]
_rvcm.tibrvcmTransport_GetTransport.restype = _c_tibrv_status

def tibrvcmTransport_GetTransport(cmTransport: tibrvcmTransport) -> (tibrv_status, tibrvTransport):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrvTransport()

    status = _rvcm.tibrvcmTransport_GetTransport(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetName(
#                   tibrvcmTransport            cmTransport,
#                   const char**                cmName
#               );
#
_rvcm.tibrvcmTransport_GetName.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_str)]
_rvcm.tibrvcmTransport_GetName.restype = _c_tibrv_status

def tibrvcmTransport_GetName(cmTransport: tibrvcmTransport) -> (tibrv_status, str):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_str(0)

    status = _rvcm.tibrvcmTransport_GetName(cmtx, _ctypes.byref(ret))

    return status, _pystr(ret.value)


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetRelayAgent(
#                   tibrvcmTransport            cmTransport,
#                   const char**                relayAgent
#               );
#
_rvcm.tibrvcmTransport_GetRelayAgent.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_str)]
_rvcm.tibrvcmTransport_GetRelayAgent.restype = _c_tibrv_status

def tibrvcmTransport_GetRelayAgent(cmTransport: tibrvcmTransport) -> (tibrv_status, str):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_str(0)

    status = _rvcm.tibrvcmTransport_GetRelayAgent(cmtx, _ctypes.byref(ret))

    return status, _pystr(ret.value)


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetLedgerName(
#                   tibrvcmTransport            cmTransport,
#                   const char**                ledgerName
#               );
#
_rvcm.tibrvcmTransport_GetLedgerName.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_str)]
_rvcm.tibrvcmTransport_GetLedgerName.restype = _c_tibrv_status

def tibrvcmTransport_GetLedgerName(cmTransport: tibrvcmTransport) -> (tibrv_status, str):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_str(0)

    status = _rvcm.tibrvcmTransport_GetLedgerName(cmtx, _ctypes.byref(ret))

    return status, _pystr(ret.value)


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetSyncLedger(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_bool*                 syncLedger
#               );
#
_rvcm.tibrvcmTransport_GetSyncLedger.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_bool)]
_rvcm.tibrvcmTransport_GetSyncLedger.restype = _c_tibrv_status

def tibrvcmTransport_GetSyncLedger(cmTransport: tibrvcmTransport) -> (tibrv_status, bool):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_bool()

    status = _rvcm.tibrvcmTransport_GetSyncLedger(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetRequestOld(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_bool*                 requestOld
#               );
#
_rvcm.tibrvcmTransport_GetRequestOld.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_bool)]
_rvcm.tibrvcmTransport_GetRequestOld.restype = _c_tibrv_status

def tibrvcmTransport_GetRequestOld(cmTransport: tibrvcmTransport) -> (tibrv_status, bool):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_bool()

    status = _rvcm.tibrvcmTransport_GetRequestOld(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibv/cm.h
# tibrv_status tibrvcmTransport_AllowListener(
#                   tibrvcmTransport            cmTransport,
#                   const char*                 cmName
#               );
#
_rvcm.tibrvcmTransport_AllowListener.argtypes = [_c_tibrvcmTransport, _c_tibrv_str]
_rvcm.tibrvcmTransport_AllowListener.restype = _c_tibrv_status

def tibrvcmTransport_AllowListener(cmTransport: tibrvcmTransport, cmName: str) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if cmName is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        name = _cstr(cmName)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_AllowListener(cmtx, name)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_DisallowListener(
#                   tibrvcmTransport            cmTransport,
#                   const char*                 cmName
#               );
#
_rvcm.tibrvcmTransport_DisallowListener.argtypes = [_c_tibrvcmTransport, _c_tibrv_str]
_rvcm.tibrvcmTransport_DisallowListener.restype = _c_tibrv_status

def tibrvcmTransport_DisallowListener(cmTransport: tibrvcmTransport, cmName: str) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if cmName is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        name = _cstr(cmName)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_DisallowListener(cmtx, name)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_AddListener(
#                   tibrvcmTransport            cmTransport,
#                   const char*                 cmName,
#                   const char*                 subject
#               );
#
_rvcm.tibrvcmTransport_AddListener.argtypes = [_c_tibrvcmTransport, _c_tibrv_str, _c_tibrv_str]
_rvcm.tibrvcmTransport_AddListener.restype = _c_tibrv_status

def tibrvcmTransport_AddListener(cmTransport: tibrvcmTransport, cmName: str, subject: str) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if cmName is None or subject is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        name = _cstr(cmName)
        subj = _cstr(subject)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_AddListener(cmtx, name, subj)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_RemoveListener(
#                   tibrvcmTransport            cmTransport,
#                   const char*                 cmName,
#                   const char*                 subject
#               );
#
_rvcm.tibrvcmTransport_RemoveListener.argtypes = [_c_tibrvcmTransport, _c_tibrv_str, _c_tibrv_str]
_rvcm.tibrvcmTransport_RemoveListener.restype = _c_tibrv_status

def tibrvcmTransport_RemoveListener(cmTransport: tibrvcmTransport, cmName: str, subject: str) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if cmName is None or subject is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        name = _cstr(cmName)
        subj = _cstr(subject)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_RemoveListener(cmtx, name, subj)

    return status



##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_RemoveSendState(
#                   tibrvcmTransport            cmTransport,
#                   const char*                 subject
#               );
#
_rvcm.tibrvcmTransport_RemoveSendState.argtypes = [_c_tibrvcmTransport, _c_tibrv_str]
_rvcm.tibrvcmTransport_RemoveSendState.restype = _c_tibrv_status

def tibrvcmTransport_RemoveSendState(cmTransport: tibrvcmTransport, cmName: str) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if cmName is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        name = _cstr(cmName)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_RemoveSendState(cmtx, name)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SyncLedger(
#                   tibrvcmTransport            cmTransport
#               );
#
_rvcm.tibrvcmTransport_SyncLedger.argtypes = [_c_tibrvcmTransport]
_rvcm.tibrvcmTransport_SyncLedger.restype = _c_tibrv_status

def tibrvcmTransport_SyncLedger(cmTransport: tibrvcmTransport) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    status = _rvcm.tibrvcmTransport_SyncLedger(cmtx)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_ConnectToRelayAgent(
#                   tibrvcmTransport            cmTransport
#               );
#
_rvcm.tibrvcmTransport_ConnectToRelayAgent.argtypes = [_c_tibrvcmTransport]
_rvcm.tibrvcmTransport_ConnectToRelayAgent.restype = _c_tibrv_status

def tibrvcmTransport_ConnectToRelayAgent(cmTransport: tibrvcmTransport) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_ConnectToRelayAgent(cmtx)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_DisconnectFromRelayAgent(
#                   tibrvcmTransport            cmTransport
#               );
#
_rvcm.tibrvcmTransport_DisconnectFromRelayAgent.argtypes = [_c_tibrvcmTransport]
_rvcm.tibrvcmTransport_DisconnectFromRelayAgent.restype = _c_tibrv_status

def tibrvcmTransport_DisconnectFromRelayAgent(cmTransport: tibrvcmTransport) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_DisconnectFromRelayAgent(cmtx)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_Destroy(
#                   tibrvcmTransport            cmTransport
#               );
#
_rvcm.tibrvcmTransport_Destroy.argtypes = [_c_tibrvcmTransport]
_rvcm.tibrvcmTransport_Destroy.restype = _c_tibrv_status

def tibrvcmTransport_Destroy(cmTransport: tibrvcmTransport) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    status = _rvcm.tibrvcmTransport_Destroy(cmtx)

    return status


##
# tibrv/cm.h
# *tibrv_status tibrvcmTransport_DestroyEx(
#                   tibrvcmTransport		    cmTransport,
#                   tibrvcmTransportOnComplete	completionFunction,
#                   void*			            closure
#               );
#


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_CreateListener(
#                   tibrvcmEvent*               cmListener,
#                   tibrvQueue                  queue,
#                   tibrvcmEventCallback        callback,
#                   tibrvcmTransport            cmTransport,
#                   const char*                 subject,
#                   const void*                 closure);
#
_rvcm.tibrvcmEvent_CreateListener.argtypes = [_ctypes.POINTER(_c_tibrvcmEvent),
                                              _c_tibrvQueue,
                                              _c_tibrvcmEventCallback,
                                              _c_tibrvcmTransport,
                                              _c_tibrv_str,
                                              _ctypes.py_object]
_rvcm.tibrvcmEvent_CreateListener.restype = _c_tibrv_status


def tibrvcmEvent_CreateListener(queue: tibrvQueue, callback, cmTransport: tibrvcmTransport,
                                subject: str, closure) -> (tibrv_status, tibrvcmEvent):

    if queue == 0 or queue is None:
        return TIBRV_INVALID_QUEUE

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if subject is None:
        return TIBRV_INVALID_ARG

    if callback is None:
        return TIBRV_INVALID_CALLBACK

    ev = _c_tibrvcmEvent(0)

    try:
        que = _c_tibrvQueue(queue)
    except:
        return TIBRV_INVALID_QUEUE

    try:
        cb = _c_tibrvcmEventCallback(callback)
    except:
        return TIBRV_INVALID_CALLBACK

    try:
        tx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        subj = _cstr(subject)
        cz = _ctypes.py_object(closure)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmEvent_CreateListener(_ctypes.byref(ev), que, cb, tx, subj, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(ev.value, cb, cz)

    return status, ev.value


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_GetQueue(
#                   tibrvcmEvent                event,
#                   tibrvQueue*                 queue
#               );
#
_rvcm.tibrvcmEvent_GetQueue.argtypes = [_c_tibrvcmEvent, _ctypes.POINTER(_c_tibrvQueue)]
_rvcm.tibrvcmEvent_GetQueue.restype = _c_tibrv_status

def tibrvcmEvent_GetQueue(event: tibrvcmEvent) -> (tibrv_status, tibrvQueue):

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    que = _c_tibrvQueue(0)

    status = _rvcm.tibrvcmEvent_GetQueue(ev, _ctypes.byref(que))

    return status, que.value


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_GetListenerSubject(
#                   tibrvcmEvent                event,
#                   const char**                subject
#               );
#
_rvcm.tibrvcmEvent_GetListenerSubject.argtypes = [_c_tibrvcmEvent, _ctypes.POINTER(_c_tibrv_str)]
_rvcm.tibrvcmEvent_GetListenerSubject.restype = _c_tibrv_status

def tibrvcmEvent_GetListenerSubject(event: tibrvcmEvent) -> (tibrv_status, str):

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    ret = _c_tibrv_str(0)

    status = _rvcm.tibrvcmEvent_GetListenerSubject(ev, _ctypes.byref(ret))

    return status, _pystr(ret.value)


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_GetListenerTransport(
#                   tibrvcmEvent                event,
#                   tibrvcmTransport*           transport
#               );
#
_rvcm.tibrvcmEvent_GetListenerTransport.argtypes = [_c_tibrvcmEvent, _ctypes.POINTER(_c_tibrvcmTransport)]
_rvcm.tibrvcmEvent_GetListenerTransport.restype = _c_tibrv_status

def tibrvcmEvent_GetListenerTransport(event: tibrvcmEvent) -> (tibrv_status, tibrvcmTransport):

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    cmtx = _c_tibrvcmTransport(0)

    status = _rvcm.tibrvcmEvent_GetListenerTransport(ev, _ctypes.byref(cmtx))

    return status, cmtx.value


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_SetExplicitConfirm(
#                   tibrvcmEvent                cmListener
#               );
#
_rvcm.tibrvcmEvent_SetExplicitConfirm.argtypes = [_c_tibrvcmEvent]
_rvcm.tibrvcmEvent_SetExplicitConfirm.restype = _c_tibrv_status

def tibrvcmEvent_SetExplicitConfirm(event: tibrvcmEvent) -> tibrv_status:

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    status = _rvcm.tibrvcmEvent_SetExplicitConfirm(ev)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_ConfirmMsg(
#                   tibrvcmEvent                cmListener,
#                   tibrvMsg                    message
#               );
#
_rvcm.tibrvcmEvent_ConfirmMsg.argtypes = [_c_tibrvcmEvent, _c_tibrvMsg]
_rvcm.tibrvcmEvent_ConfirmMsg.restype = _c_tibrv_status

def tibrvcmEvent_ConfirmMsg(event: tibrvcmEvent, message: tibrvMsg) -> tibrv_status:

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rvcm.tibrvcmEvent_ConfirmMsg(ev, msg)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmEvent_DestroyEx(
#                   tibrvcmEvent                cmListener,
#                   tibrv_bool                  cancelAgreements,
#                   tibrvEventOnComplete        completeCallback);
#
_rvcm.tibrvcmEvent_DestroyEx.argtypes = [_c_tibrvcmEvent, _c_tibrv_bool, _c_tibrvEventOnComplete]
_rvcm.tibrvcmEvent_DestroyEx.restype = _c_tibrv_status

def tibrvcmEvent_Destroy(event: tibrvcmEvent, cancelAgreements: bool = False,
                         callback = None) -> tibrv_status:

    if event == 0 or event is None:
        return TIBRV_INVALID_EVENT

    if cancelAgreements is None:
        return TIBRV_INVALID_ARG

    try:
        ev = _c_tibrvcmEvent(event)
    except:
        return TIBRV_INVALID_EVENT

    try:
        cxl = _c_tibrv_bool(cancelAgreements)
    except:
        return TIBRV_INVALID_ARG

    if callback is None:
        cb = _c_tibrvEventOnComplete(0)
    else:
        try:
            cb = _c_tibrvEventOnComplete(callback)
        except:
            return TIBRV_INVALID_CALLBACK

    status = _rvcm.tibrvcmEvent_DestroyEx(ev, cxl, cb)

    # THIS MAY CAUSE MEMORY LEAK
    if status == TIBRV_OK and callback is not None:
        __reg(event, cb)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvMsg_GetCMSender(
#                   tibrvMsg                    message,
#                   const char**                senderName
#               );
#
_rvcm.tibrvMsg_GetCMSender.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_str)]
_rvcm.tibrvMsg_GetCMSender.restype = _c_tibrv_status

def tibrvMsg_GetCMSender(message: tibrvMsg) -> (tibrv_status, str):

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    ret = _c_tibrv_str(0)

    status = _rvcm.tibrvMsg_GetCMSender(msg, _ctypes.byref(ret))

    return status, _pystr(ret.value)


##
# tibrv/cm.h
# tibrv_status tibrvMsg_GetCMSequence(
#                   tibrvMsg                    message,
#                   tibrv_u64*                  sequenceNumber
#               );
#
_rvcm.tibrvMsg_GetCMSequence.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_u64)]
_rvcm.tibrvMsg_GetCMSequence.restype = _c_tibrv_status

def tibrvMsg_GetCMSequence(message: tibrvMsg) -> (tibrv_status, int):

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    ret = _c_tibrv_u64(0)

    status = _rvcm.tibrvMsg_GetCMSequence(msg, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvMsg_GetCMTimeLimit(
#                   tibrvMsg                    message,
#                   tibrv_f64*                  timeLimit
#               );
#
_rvcm.tibrvMsg_GetCMTimeLimit.argtypes = [_c_tibrvMsg, _ctypes.POINTER(_c_tibrv_f64)]
_rvcm.tibrvMsg_GetCMTimeLimit.restype = _c_tibrv_status

def tibrvMsg_GetCMTimeLimit(message: tibrvMsg) -> (tibrv_status, float):

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    ret = _c_tibrv_f64(0)

    status = _rvcm.tibrvMsg_GetCMTimeLimit(msg, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvMsg_SetCMTimeLimit(
#                   tibrvMsg                    message,
#                   tibrv_f64                   timeLimit
#               );
#
_rvcm.tibrvMsg_SetCMTimeLimit.argtypes = [_c_tibrvMsg, _c_tibrv_f64]
_rvcm.tibrvMsg_SetCMTimeLimit.restype = _c_tibrv_status

def tibrvMsg_SetCMTimeLimit(message: tibrvMsg, timeLimit: float) -> tibrv_status:

    if message == 0 or message is None:
        return TIBRV_INVALID_MSG

    if timeLimit is None:
        return TIBRV_INVALID_ARG

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    try:
        tt = _c_tibrv_f64(timeLimit)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvMsg_SetCMTimeLimit(msg, tt)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetDefaultCMTimeLimit(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_f64*                  timeLimit
#               );
#
_rvcm.tibrvcmTransport_GetDefaultCMTimeLimit.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_f64)]
_rvcm.tibrvcmTransport_GetDefaultCMTimeLimit.restype = _c_tibrv_status

def tibrvcmTransport_GetDefaultCMTimeLimit(cmTransport: tibrvcmTransport) -> (tibrv_status, float):

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    ret = _c_tibrv_f64(0)

    status = _rvcm.tibrvcmTransport_GetDefaultCMTimeLimit(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SetDefaultCMTimeLimit(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_f64                   timeLimit
#               );
#
_rvcm.tibrvcmTransport_SetDefaultCMTimeLimit.argtypes = [_c_tibrvcmTransport, _c_tibrv_f64]
_rvcm.tibrvcmTransport_SetDefaultCMTimeLimit.restype = _c_tibrv_status

def tibrvcmTransport_SetDefaultCMTimeLimit(cmTransport: tibrvcmTransport, timeLimit: float) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if timeLimit is None:
        return TIBRV_INVALID_ARG

    try:
        cmtx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        tt = _c_tibrv_f64(timeLimit)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_SetDefaultCMTimeLimit(cmtx, tt)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_ReviewLedger(
#                   tibrvcmTransport            cmTransport,
#                   tibrvcmReviewCallback       callback,
#                   const char*                 subject,
#                   const void*                 closure
#               );
#
_rvcm.tibrvcmTransport_ReviewLedger.argtypes = [_c_tibrvcmTransport,
                                                _c_tibrvcmReviewCallback,
                                                _c_tibrv_str,
                                                _ctypes.py_object]
_rvcm.tibrvcmTransport_ReviewLedger.restype = _c_tibrv_status

def tibrvcmTransport_ReviewLedger(cmTransport: tibrvcmTransport, callback, subject: str, closure) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if callback is None:
        return TIBRV_INVALID_CALLBACK

    if subject is None:
        return TIBRV_INVALID_ARG

    try:
        tx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        cb = _c_tibrvcmReviewCallback(callback)
    except:
        return TIBRV_INVALID_CALLBACK

    try:
        subj = _cstr(subject)
        cz = _ctypes.py_object(closure)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_ReviewLedger(tx, cb, subj, cz)

    # save cb to prevent GC
    if status == TIBRV_OK:
        __reg(tx.value, cb, cz)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_ExpireMessages(
#                   tibrvcmTransport		cmTransport,
#                   const char*			    subject,
#                   tibrv_u64			    sequenceNumber
#               );
#
_rvcm.tibrvcmTransport_ExpireMessages.argtypes = [_c_tibrvcmTransport,
                                                  _c_tibrv_str,
                                                  _c_tibrv_u64]
_rvcm.tibrvcmTransport_ExpireMessages.restype = _c_tibrv_status

def tibrvcmTransport_ExpireMessages(cmTransport: tibrvcmTransport, subject: str,
                                    sequenceNumber: int) -> tibrv_status:

    if cmTransport == 0 or cmTransport is None:
        return TIBRV_INVALID_TRANSPORT

    if subject is None or sequenceNumber is None:
        return TIBRV_INVALID_ARG

    try:
        tx = _c_tibrvcmTransport(cmTransport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        subj = _cstr(subject)
        seq = _c_tibrv_u64(sequenceNumber)
    except:
        return TIBRV_INVALID_ARG

    status = _rvcm.tibrvcmTransport_ExpireMessages(tx, subj, seq)

    return status

