##
# pytibrv/tport.py
#   TIBRV Library for PYTHON
#   tibrvTransport_XXX
#
# LAST MODIFIED : V1.0 20161211 ARIEN arien.chen@gmail.com 
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
#
#
# FEATURES: * = un-implement
# -----------------------------------------------------------------------------
#   tibrvTransport_Create
#   tibrvTransport_CreateInbox
#   tibrvTransport_Destroy
#   tibrvTransport_GetDaemon
#   tibrvTransport_GetNetwork
#   tibrvTransport_GetService
#   tibrvTransport_GetDescription
#   tibrvTransport_RequestReliability
#   tibrvTransport_Send
#   tibrvTransport_SendRequest
#   tibrvTransport_SendReply
#   tibrvTransport_SetDescription
#
#  *tibrvTransport_CreateAcceptVc
#  *tibrvTransport_CreateConnectVc
#  *tibrvTransport_WaitForVcConnection
#  *tibrvTransport_Sendv
#  *tibrvTransport_SetSendingWaitLimit
#  *tibrvTransport_GetSendingWaitLimit
#  *tibrvTransport_SetBatchMode
#  *tibrvTransport_SetBatchSize
#  *tibrvTransport_CreateLicensed
#
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20161211 V1.0 ARIEN arien.chen@gmail.com
#   CREATED
#
##

import ctypes as _ctypes
from .types import tibrv_status, tibrvTransport, tibrvMsg, \
                   TIBRV_SUBJECT_MAX

from .api import _rv, _cstr, _pystr, \
                 _c_tibrvTransport, _c_tibrvMsg, \
                 _c_tibrv_status, _c_tibrv_u32, _c_tibrv_f64

from .status import TIBRV_INVALID_MSG, TIBRV_INVALID_ARG, TIBRV_INVALID_TRANSPORT

# tibrv/tport.h
# tibrv_status tibrvTransport_Create(
#                tibrvTransport*     transport,
#                const char*         service,
#                const char*         network,
#                const char*         daemonStr
#              );
_rv.tibrvTransport_Create.argtypes = [_ctypes.POINTER(_c_tibrvTransport),
                                      _ctypes.c_char_p,
                                      _ctypes.c_char_p,
                                      _ctypes.c_char_p]
_rv.tibrvTransport_Create.restype = _c_tibrv_status

def tibrvTransport_Create(service: str, network: str, daemon: str) -> (tibrv_status, tibrvTransport):

    tx = _c_tibrvTransport(0)

    status = _rv.tibrvTransport_Create(_ctypes.byref(tx), _cstr(service), _cstr(network), _cstr(daemon))

    return status, tx.value


##
# tibrv/tport.h
# tibrv_status tibrvTransport_Send(
#                tibrvTransport      transport,
#                tibrvMsg            message
#              );
#
_rv.tibrvTransport_Send.argtypes = [_c_tibrvTransport, _c_tibrvMsg]
_rv.tibrvTransport_Send.restype = _c_tibrv_status

def tibrvTransport_Send(transport: tibrvTransport, message: tibrvMsg) -> tibrv_status:

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG

    status = _rv.tibrvTransport_Send(tx, msg)

    return status

##
# tibrv/tport.h
# tibrv_status tibrvTransport_SendRequest(
#                tibrvTransport      transport,
#                tibrvMsg            message,
#                tibrvMsg*           reply,
#                tibrv_f64           idleTimeout
#              );
#
_rv.tibrvTransport_SendRequest.argtypes = [_c_tibrvTransport,
                                           _c_tibrvMsg,
                                           _ctypes.POINTER(_c_tibrvMsg),
                                           _c_tibrv_f64]
_rv.tibrvTransport_SendRequest.restype = _c_tibrv_status


def tibrvTransport_SendRequest(transport: tibrvTransport, message: tibrvMsg,
                               idleTimeout: float) -> (tibrv_status, tibrvMsg):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    if message is None or message == 0:
        return TIBRV_INVALID_MSG, None

    if idleTimeout is None:
        return TIBRV_INVALID_ARG, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        msg = _c_tibrvMsg(message)
    except:
        return TIBRV_INVALID_MSG, None

    r = _c_tibrvMsg(0)

    try:
        t = _c_tibrv_f64(idleTimeout)
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvTransport_SendRequest(tx, msg, _ctypes.byref(r), t)

    return status, r.value


##
# tibrv/tport.h
# tibrv_status tibrvTransport_SendReply(
#                tibrvTransport      transport,
#                tibrvMsg            message,
#                tibrvMsg            requestMessage
#              );
#
_rv.tibrvTransport_SendReply.argtypes = [_c_tibrvTransport, _c_tibrvMsg, _c_tibrvMsg]
_rv.tibrvTransport_SendReply.restype = _c_tibrv_status

def tibrvTransport_SendReply(transport: tibrvTransport, message: tibrvMsg, requestMessage: tibrvMsg) \
                            -> tibrv_status:

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT

    if message is None or message == 0:
        return TIBRV_INVALID_MSG

    if requestMessage is None or requestMessage == 0:
        return TIBRV_INVALID_MSG

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        msg = _c_tibrvMsg(message)
        req = _c_tibrvMsg(requestMessage)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvTransport_SendReply(tx, msg, req)

    return status


##
# tibrv/tport.h
# tibrv_status tibrvTransport_Destroy(
#                tibrvTransport      transport
#              );
#
_rv.tibrvTransport_Destroy.argtypes = [_c_tibrvTransport]
_rv.tibrvTransport_Destroy.restype = _c_tibrv_status

def tibrvTransport_Destroy(transport: tibrvTransport) -> tibrv_status:

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT

    status = _rv.tibrvTransport_Destroy(tx)

    return status

##
# tibrv/tport.h
# tibrv_status tibrvTransport_CreateInbox(
#                tibrvTransport      transport,
#                char*               subjectString,
#                tibrv_u32           subjectLimit
#              );
#
_rv.tibrvTransport_CreateInbox.argtypes = [_c_tibrvTransport, _ctypes.c_char_p, _c_tibrv_u32]
_rv.tibrvTransport_CreateInbox.restype = _c_tibrv_status

def tibrvTransport_CreateInbox(transport: tibrvTransport) -> (tibrv_status, str):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    subj = _ctypes.create_string_buffer(TIBRV_SUBJECT_MAX)

    status = _rv.tibrvTransport_CreateInbox(tx, subj, _ctypes.sizeof(subj))

    return status, _pystr(subj)


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetService(
#                tibrvTransport      transport,
#                const char**        serviceString
#              );
#
_rv.tibrvTransport_GetService.argtypes = [_c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetService.restype = _c_tibrv_status

def tibrvTransport_GetService(transport: tibrvTransport) -> (tibrv_status, str):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    sz = _ctypes.c_char_p()
    status = _rv.tibrvTransport_GetService(tx, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetNetwork(
#                tibrvTransport      transport,
#                const char**        networkString
#              );
#
_rv.tibrvTransport_GetNetwork.argtypes = [_c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetNetwork.restype = _c_tibrv_status

def tibrvTransport_GetNetwork(transport: tibrvTransport) -> (tibrv_status, str):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    sz = _ctypes.c_char_p()

    status = _rv.tibrvTransport_GetNetwork(tx, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetDaemon(
#                tibrvTransport      transport,
#                const char**        daemonString
#              );
#
_rv.tibrvTransport_GetDaemon.argtypes = [_c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetDaemon.restype = _c_tibrv_status

def tibrvTransport_GetDaemon(transport: tibrvTransport) -> (tibrv_status, str):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        sz = _ctypes.c_char_p()
    except:
        return TIBRV_INVALID_ARG, None

    status = _rv.tibrvTransport_GetDaemon(tx, _ctypes.byref(sz))

    return status, _pystr(sz)

##
# tibrv/tport.h
# tibrv_status tibrvTransport_SetDescription(
#                tibrvTransport      transport,
#                const char*         description
#              );
#
_rv.tibrvTransport_SetDescription.argtypes = [_c_tibrvTransport, _ctypes.c_char_p]
_rv.tibrvTransport_SetDescription.restype = _c_tibrv_status

def tibrvTransport_SetDescription(transport: tibrvTransport, description: str) -> tibrv_status:

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT

    if description is None:
        return TIBRV_INVALID_ARG

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        sz = _cstr(description)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvTransport_SetDescription(tx, sz)

    return status


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetDescription(
#                tibrvTransport      transport,
#                const char**        description
#              );
#
_rv.tibrvTransport_GetDescription.argtypes = [_c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetDescription.restype = _c_tibrv_status

def tibrvTransport_GetDescription(transport: tibrvTransport) -> (tibrv_status, str):

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT, None

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT, None

    sz = _ctypes.c_char_p()
    status = _rv.tibrvTransport_GetDescription(tx, _ctypes.byref(sz))

    return status, _pystr(sz)

##
# tibrv/tport.h
# tibrv_status tibrvTransport_RequestReliability(
#                tibrvTransport      transport,
#                tibrv_f64           reliability
#              );
#
_rv.tibrvTransport_RequestReliability.argtypes = [_c_tibrvTransport, _c_tibrv_f64]
_rv.tibrvTransport_RequestReliability.restype = _c_tibrv_status

def tibrvTransport_RequestReliability(transport: tibrvTransport, reliability: float) -> tibrv_status:

    if transport is None or transport == 0:
        return TIBRV_INVALID_TRANSPORT

    if reliability is None:
        return TIBRV_INVALID_ARG

    try:
        tx = _c_tibrvTransport(transport)
    except:
        return TIBRV_INVALID_TRANSPORT

    try:
        n = _c_tibrv_f64(reliability)
    except:
        return TIBRV_INVALID_ARG

    status = _rv.tibrvTransport_RequestReliability(tx, n)

    return status


