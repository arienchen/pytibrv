##
# pytibrv/tport.py
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
# CHANGED LOGS
# ---------------------------------------------------
# 20161211 ARIEN V1.0
#   CREATED
#
##

import ctypes as _ctypes
from .msg import *
from .api import _rv, _cstr, _pystr

##-----------------------------------------------------------------------------
## tibrvTransport
##-----------------------------------------------------------------------------

# tibrv/tport.h
# tibrv_status tibrvTransport_Create(
#                tibrvTransport*     transport,
#                const char*         service,
#                const char*         network,
#                const char*         daemonStr
#              );
_rv.tibrvTransport_Create.argtypes = [_ctypes.POINTER(c_tibrvTransport),
                                      _ctypes.c_char_p,
                                      _ctypes.c_char_p,
                                      _ctypes.c_char_p]
_rv.tibrvTransport_Create.restype = c_tibrv_status

def tibrvTransport_Create(service: str, network: str, daemon: str) -> (tibrv_status, tibrvTransport):

    tx = c_tibrvTransport(0)

    status = _rv.tibrvTransport_Create(_ctypes.byref(tx), _cstr(service), _cstr(network), _cstr(daemon))

    return status, tx.value


##
# tibrv/tport.h
# tibrv_status tibrvTransport_Send(
#                tibrvTransport      transport,
#                tibrvMsg            message
#              );
#
_rv.tibrvTransport_Send.argtypes = [c_tibrvTransport, c_tibrvMsg]
_rv.tibrvTransport_Send.restype = c_tibrv_status


def tibrvTransport_Send(transport: tibrvTransport, message: tibrvMsg) -> tibrv_status:

    tx = c_tibrvTransport(transport)
    msg = c_tibrvMsg(message)

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
_rv.tibrvTransport_SendRequest.argtypes = [c_tibrvTransport, c_tibrvMsg, _ctypes.POINTER(c_tibrvMsg), c_tibrv_f64]
_rv.tibrvTransport_SendRequest.restype = c_tibrv_status


def tibrvTransport_SendRequest(transport: tibrvTransport, message: tibrvMsg, idleTimeout: float) -> (tibrv_status, tibrvMsg):

    tx = c_tibrvTransport(transport)
    msg = c_tibrvMsg(message)
    r = c_tibrvMsg(0)
    t = c_tibrv_f64(idleTimeout)

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
_rv.tibrvTransport_SendReply.argtypes = [c_tibrvTransport, c_tibrvMsg, c_tibrvMsg]
_rv.tibrvTransport_SendReply.restype = c_tibrv_status

def tibrvTransport_SendReply(transport: tibrvTransport, message: tibrvMsg, requestMessage: tibrvMsg) -> tibrv_status:

    tx = c_tibrvTransport(transport)
    msg = c_tibrvMsg(message)
    req = c_tibrvMsg(requestMessage)

    status = _rv.tibrvTransport_SendReply(tx, msg, req)

    return status


##
# tibrv/tport.h
# tibrv_status tibrvTransport_Destroy(
#                tibrvTransport      transport
#              );
#
_rv.tibrvTransport_Destroy.argtypes = [c_tibrvTransport]
_rv.tibrvTransport_Destroy.restype = c_tibrv_status


def tibrvTransport_Destroy(transport: tibrvTransport) -> tibrv_status:

    tx = c_tibrvTransport(transport)

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
_rv.tibrvTransport_CreateInbox.argtypes = [c_tibrvTransport, _ctypes.c_char_p, c_tibrv_u32]
_rv.tibrvTransport_CreateInbox.restype = c_tibrv_status

def tibrvTransport_CreateInbox(transport: tibrvTransport) -> (tibrv_status, str):

    tx = c_tibrvTransport(transport)
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
_rv.tibrvTransport_GetService.argtypes = [c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetService.restype = c_tibrv_status

def tibrvTransport_GetService(transport: tibrvTransport) -> (tibrv_status, str):

    tx = c_tibrvTransport(transport)
    sz = _ctypes.c_char_p(0)
    status = _rv.tibrvTransport_GetService(tx, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetNetwork(
#                tibrvTransport      transport,
#                const char**        networkString
#              );
#
_rv.tibrvTransport_GetNetwork.argtypes = [c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetNetwork.restype = c_tibrv_status

def tibrvTransport_GetNetwork(transport: tibrvTransport) -> (tibrv_status, str):

    tx = c_tibrvTransport(transport)
    sz = _ctypes.c_char_p(0)
    status = _rv.tibrvTransport_GetNetwork(tx, _ctypes.byref(sz))

    return status, _pystr(sz)


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetDaemon(
#                tibrvTransport      transport,
#                const char**        daemonString
#              );
#
_rv.tibrvTransport_GetDaemon.argtypes = [c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetDaemon.restype = c_tibrv_status

def tibrvTransport_GetDaemon(transport: tibrvTransport) -> (tibrv_status, str):

    tx = c_tibrvTransport(transport)
    sz = _ctypes.c_char_p(0)
    status = _rv.tibrvTransport_GetDaemon(tx, _ctypes.byref(sz))

    return status, _pystr(sz)

##
# tibrv/tport.h
# tibrv_status tibrvTransport_SetDescription(
#                tibrvTransport      transport,
#                const char*         description
#              );
#
_rv.tibrvTransport_SetDescription.argtypes = [c_tibrvTransport, _ctypes.c_char_p]
_rv.tibrvTransport_SetDescription.restype = c_tibrv_status

def tibrvTransport_SetDescription(transport: tibrvTransport, description: str) -> tibrv_status:

    tx = c_tibrvTransport(transport)
    sz = _cstr(description)
    status = _rv.tibrvTransport_SetDescription(tx, sz)

    return status


##
# tibrv/tport.h
# tibrv_status tibrvTransport_GetDescription(
#                tibrvTransport      transport,
#                const char**        description
#              );
#
_rv.tibrvTransport_GetDescription.argtypes = [c_tibrvTransport, _ctypes.POINTER(_ctypes.c_char_p)]
_rv.tibrvTransport_GetDescription.restype = c_tibrv_status

def tibrvTransport_GetDescription(transport: tibrvTransport) -> (tibrv_status, str):

    tx = c_tibrvTransport(transport)
    sz = _ctypes.c_char_p(0)
    status = _rv.tibrvTransport_GetDescription(tx, _ctypes.byref(sz))

    return status, _pystr(sz)

##
# tibrv/tport.h
# tibrv_status tibrvTransport_RequestReliability(
#                tibrvTransport      transport,
#                tibrv_f64           reliability
#              );
#
_rv.tibrvTransport_RequestReliability.argtypes = [c_tibrvTransport, c_tibrv_f64]
_rv.tibrvTransport_RequestReliability.restype = c_tibrv_status

def tibrvTransport_RequestReliability(transport:tibrvTransport, reliability: float) -> tibrv_status:

    tx = c_tibrvTransport(transport)
    n = c_tibrv_f64(reliability)
    status = _rv.tibrvTransport_RequestReliability(tx, n)

    return status


class TibrvTx :
    def __init__(self):
        self._tx = 0
        self._err = None

    def __del__(self):
        self.destroy()

    def id(self):
        return self._tx

    def create(self, service : str, network:str, daemon:str) -> int :
        if self._tx != 0:
            status = TIBRV_ID_IN_USE
        else:
            tx = 0
            status, tx = tibrvTransport_Create(service, network, daemon);

            if status == TIBRV_OK:
                self._tx = tx

        self._err = TibrvStatus.error(status)

        return status;

    def destroy(self) -> int :
        if self._tx == 0:
            status = TIBRV_INVALID_TRANSPORT
        else:
            status = tibrvTransport_Destroy(self._tx)

        self._tx = 0

        self._err = TibrvStatus.error(status)

        return status

    @property
    def description(self) -> str:
        ret = None
        status, ret = tibrvTransport_GetDescription(self._tx)
        self._err = TibrvStatus.error(status)

        return ret

    @description.setter
    def description(self, sz: str) -> None:
        status = tibrvTransport_SetDescription(self._tx, sz)
        self._err = TibrvStatus.error(status)

    @property
    def service(self) -> str:
        ret = None
        status, ret = tibrvTransport_GetService(self._tx)
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def network(self) -> str:
        ret = None
        status, ret = tibrvTransport_GetNetwork(self._tx)
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def daemon(self) -> str:
        ret = None
        status, ret = tibrvTransport_GetDaemon(self._tx)
        self._err = TibrvStatus.error(status)

        return ret

    def inbox(self) -> str:
        ret = None
        status, ret = tibrvTransport_CreateInbox(self._tx)
        self._err = TibrvStatus.error(status)

        return ret

    def reliability(self, reliability: float) -> int:
        status = tibrvTransport_RequestReliability(self._tx, reliability)
        self._err = TibrvStatus.error(status)

        return status

    @property
    def error(self) -> TibrvError :
        return self._err

    def send(self, msg: TibrvMsg, subj: str=None) -> tibrv_status:
        if msg is None or type(msg) is not TibrvMsg :
            status = TIBRV_INVALID_MSG
        else:
            if subj is not None:
                status = tibrvMsg_SetSendSubject(msg.id(), subj)
                if status != TIBRV_OK:
                    self._err = TibrvStatus.error(status)
                    return status

            status = tibrvTransport_Send(self._tx, msg.id())

        self._err = TibrvStatus.error(status)

        return status

    def sendRequest(self, msg: TibrvMsg, timeout : float, subj:str = None) -> (tibrv_status, TibrvMsg):
        if msg is None or type(msg) is not TibrvMsg:
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status, None

        if subj is not None:
            status = tibrvMsg_SetSendSubject(msg.id(), subj)
            if status != TIBRV_OK:
                self._err = TibrvStatus.error(status)
                return status, None

        reply = None
        status, m = tibrvTransport_SendRequest(self._tx, msg.id(), timeout)
        if status == TIBRV_OK:
            reply = TibrvMsg(m)

        self._err = TibrvStatus.error(status)

        return status, reply

    def sendReply(self, msg: TibrvMsg, request: TibrvMsg) -> tibrv_status:
        if msg is None or type(msg) is not TibrvMsg:
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        if request is None or type(request) is not TibrvMsg:
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvTransport_SendReply(self._tx, msg.id(), request.id())

        self._err = TibrvStatus.error(status)

        return status



