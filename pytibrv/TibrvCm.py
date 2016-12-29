##
# pytibrv/TibrvCm.py
#   TIBRV Library for PYTHON
#
#   TibrvCmTx               <- tibrvcmTransport_XXX
#   TibrvCmListener         <- tibrvcmEvent_XXX
#   TibrvCmMsg              <- tibrvMsg_XXX
#
# LAST MODIFIED : V1.0 20161227 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
## 1. TibrvCmTx is not a subclass of TibrvTx
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
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20161227 ARIEN V1.0
#   CREATED
#

from .status import TIBRV_OK, TIBRV_ID_IN_USE, TIBRV_INVALID_ARG, TIBRV_INVALID_CALLBACK, \
                    TIBRV_INVALID_TRANSPORT, TIBRV_INVALID_MSG

from .msg import tibrvMsg_Create

from .Tibrv import tibrv_status, tibrvMsg, tibrvClosure, \
                   tibrvMsg_SetSendSubject, \
                   TibrvQueue, TibrvTx, TibrvStatus, TibrvError, TibrvMsg

from .cm import tibrvcmTransport, tibrvcmEvent, \
                tibrvcm_Version, tibrvcmTransport_Create, tibrvcmTransport_Destroy,\
                tibrvcmTransport_Send, tibrvcmTransport_SendRequest, tibrvcmTransport_SendReply, \
                tibrvcmTransport_GetTransport, tibrvcmTransport_GetName, \
                tibrvcmTransport_GetRelayAgent, tibrvcmTransport_GetLedgerName, \
                tibrvcmTransport_GetSyncLedger, tibrvcmTransport_GetRequestOld, \
                tibrvcmTransport_AllowListener, tibrvcmTransport_DisallowListener, \
                tibrvcmTransport_AddListener, tibrvcmTransport_RemoveListener, \
                tibrvcmTransport_RemoveSendState, tibrvcmTransport_SyncLedger, \
                tibrvcmTransport_ConnectToRelayAgent, tibrvcmTransport_DisconnectFromRelayAgent, \
                tibrvcmTransport_GetDefaultCMTimeLimit, tibrvcmTransport_SetDefaultCMTimeLimit, \
                tibrvcmTransport_ReviewLedger, tibrvcmTransport_ExpireMessages, \
                tibrvcmEvent_CreateListener, tibrvcmEvent_Destroy, tibrvcmEvent_GetQueue, \
                tibrvcmEvent_GetListenerSubject, tibrvcmEvent_GetListenerTransport, \
                tibrvcmEvent_SetExplicitConfirm, tibrvcmEvent_ConfirmMsg, \
                tibrvMsg_GetCMSender, tibrvMsg_GetCMSequence, tibrvMsg_GetCMTimeLimit, \
                tibrvMsg_SetCMTimeLimit


class TibrvCmTransportOnComplete:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, cmtx, closure):
        pass

    def _register(self):
        def _cb(cmtx: tibrvcmTransport, closure):
            tx = TibrvCmTx(cmtx)
            cz = tibrvClosure(closure)

            self.callback(tx, cz)

        return _cb

class TibrvCmMsgCallback:
    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, event, message, closure):
        pass

    def _register(self):
        def _cb(event: tibrvcmEvent, message: tibrvMsg, closure):
            ev = TibrvCmListener(event)
            msg = TibrvCmMsg(message)
            cz = tibrvClosure(closure)

            self.callback(ev, msg, cz)

        return _cb


class TibrvReviewCallback:
    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, event, message, closure):
        pass

    def _register(self):
        def _cb(cmtx: tibrvcmTransport, subj: bytes, message: tibrvMsg, closure):
            tx = TibrvCmTx(cmtx)
            msg = TibrvMsg(message)
            sz = subj.decode()
            cz = tibrvClosure(closure)

            self.callback(tx, sz, msg, cz)

        return _cb



##-----------------------------------------------------------------------------
# TibrvCm
##-----------------------------------------------------------------------------
class TibrvCm:

    @staticmethod
    def version():
        status = tibrvcm_Version()
        return status

##-----------------------------------------------------------------------------
## TibrvCmMsg
##-----------------------------------------------------------------------------
class TibrvCmMsg(TibrvMsg):

    @staticmethod
    def create(initBytes: int = 0) -> 'TibrvCmMsg':
        # FAILED ONLY IF OOM, TIBRV_NO_MEMORY
        # return None if failed
        status, ret = tibrvMsg_Create(initBytes)
        if status == TIBRV_OK:
            return TibrvCmMsg(ret)

        return None

    def sender(self) -> str:

        status, ret = tibrvMsg_GetCMSender(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def sequence(self) -> int:

        status, ret = tibrvMsg_GetCMSequence(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def timeLimit(self) -> float:

        status, ret = tibrvMsg_GetCMTimeLimit(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @timeLimit.setter
    def timeLimit(self, timeout: float):

        status = tibrvMsg_SetCMTimeLimit(self.id(), timeout)
        self._err = TibrvStatus.error(status)


##-----------------------------------------------------------------------------
## TibrvCmTx
##-----------------------------------------------------------------------------
class TibrvCmTx:
    def __init__(self, cmtx: tibrvcmTransport = 0):
        self._cmtx = 0
        self._err = None

        if cmtx is not None:
            self._cmtx = cmtx

    def id(self):
        return self._cmtx

    def error(self) -> TibrvError:
        return self._err

    def create(self, tx: TibrvTx, cmName: str, reqOld: bool, ledger: str,
               syncLedger: bool, agent: str) -> tibrv_status:

        if self._cmtx != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if tx is None or not isinstance(tx, TibrvTx):
            status = TIBRV_INVALID_TRANSPORT
            self._err = TibrvStatus.error(status)
            return status

        status, cmtx = tibrvcmTransport_Create(tx.id(), cmName, reqOld, ledger, syncLedger, agent)
        if status == TIBRV_OK:
            self._cmtx = cmtx

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:
        status = tibrvcmTransport_Destroy(self._cmtx)

        self._cmtx = 0

        self._err = TibrvStatus.error(status)

        return status

    def send(self, msg: TibrvMsg, subj: str=None) -> tibrv_status:

        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status


        if subj is not None:
            status = tibrvMsg_SetSendSubject(msg.id(), subj)
            if status != TIBRV_OK:
                self._err = TibrvStatus.error(status)
                return status

        status = tibrvcmTransport_Send(self.id(), msg.id())
        self._err = TibrvStatus.error(status)

        return status


    def sendRequest(self, msg: TibrvMsg, timeout: float, subj: str = None) -> (tibrv_status, TibrvCmMsg):

        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status, None

        if subj is not None:
            status = tibrvMsg_SetSendSubject(msg.id(), subj)
            if status != TIBRV_OK:
                self._err = TibrvStatus.error(status)
                return status, None

        reply = None

        status, m = tibrvcmTransport_SendRequest(self.id(), msg.id(), timeout)
        if status == TIBRV_OK:
            reply = TibrvCmMsg(m)

        self._err = TibrvStatus.error(status)

        return status, reply

    def sendReply(self, msg: TibrvMsg, request: TibrvMsg) -> tibrv_status:

        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        if request is None or not isinstance(request, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvcmTransport_SendReply(self.id(), msg.id(), request.id())

        self._err = TibrvStatus.error(status)

        return status

    def tx(self) -> TibrvTx:
        ret = None

        status, tx = tibrvcmTransport_GetTransport(self.id())
        if status == TIBRV_OK:
            ret = TibrvTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    def name(self) -> str:

        status, ret = tibrvcmTransport_GetName(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def relayAgent(self) -> str:

        status, ret = tibrvcmTransport_GetRelayAgent(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def ledger(self) -> str:

        status, ret = tibrvcmTransport_GetLedgerName(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def isSync(self) -> bool:

        status, ret = tibrvcmTransport_GetSyncLedger(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def isRequestOld(self) -> bool:

        status, ret = tibrvcmTransport_GetRequestOld(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def allow(self, cmName: str) -> tibrv_status:

        status = tibrvcmTransport_AllowListener(self.id(), cmName)
        self._err = TibrvStatus.error(status)

        return status

    def disallow(self, cmName: str) -> tibrv_status:

        status = tibrvcmTransport_DisallowListener(self.id(), cmName)
        self._err = TibrvStatus.error(status)

        return status

    def addListener(self, cmName: str) -> tibrv_status:

        status = tibrvcmTransport_AddListener(self.id(), cmName)
        self._err = TibrvStatus.error(status)

        return status

    def removeListener(self, cmName: str) -> tibrv_status:

        status = tibrvcmTransport_RemoveListener(self.id(), cmName)
        self._err = TibrvStatus.error(status)

        return status

    def removeSubject(self, subj: str) -> tibrv_status:

        status = tibrvcmTransport_RemoveSendState(self.id(), subj)
        self._err = TibrvStatus.error(status)

        return status

    def syncLedger(self) -> tibrv_status:

        status = tibrvcmTransport_SyncLedger(self.id())
        self._err = TibrvStatus.error(status)

        return status

    def connectAgent(self) -> tibrv_status:

        status = tibrvcmTransport_ConnectToRelayAgent(self.id())
        self._err = TibrvStatus.error(status)

        return status

    def disconnectAgent(self) -> tibrv_status:

        status = tibrvcmTransport_DisconnectFromRelayAgent(self.id())
        self._err = TibrvStatus.error(status)

        return status

    @property
    def timeLimit(self) -> float:

        status, ret = tibrvcmTransport_GetDefaultCMTimeLimit(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @timeLimit.setter
    def timeLimit(self, timeout: float):

        status = tibrvcmTransport_SetDefaultCMTimeLimit(self.id(), timeout)
        self._err = TibrvStatus.error(status)

    def expire(self, subj: str, seq: int) -> tibrv_status:

        status = tibrvcmTransport_ExpireMessages(self.id(), subj, seq)
        self._err = TibrvStatus.error(status)

        return status

    def reviewLedger(self, callback: TibrvReviewCallback, subject: str, closure = None) -> tibrv_status:

        if not isinstance(callback, TibrvReviewCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvcmTransport_ReviewLedger(self.id(), callback._register(), subject, closure)

        self._err = TibrvStatus.error(status)

        return status


##-----------------------------------------------------------------------------
## TibrvCmListener
##-----------------------------------------------------------------------------
class TibrvCmListener:
    def __init__(self, event: tibrvcmEvent = 0):
        self._event = 0
        self._err = None

        if event is not None:
            self._event = event

    def id(self):
        return self._event

    def error(self) -> TibrvError:
        return self._err

    def create(self, que: TibrvQueue, callback: TibrvCmMsgCallback, tx: TibrvCmTx,
               subject: str, closure = None) -> tibrv_status:

        if self.id() != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if not isinstance(callback, TibrvCmMsgCallback):
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)
            return status

        status, ret = tibrvcmEvent_CreateListener(que.id(), callback._register(), tx.id(), subject, closure)
        if status == TIBRV_OK:
            self._event = ret

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:
        status = tibrvcmEvent_Destroy(self._event)

        self._event = 0
        self._err = TibrvStatus.error(status)

        return status

    def queue(self) -> TibrvQueue:
        ret = None

        status, q = tibrvcmEvent_GetQueue(self.id())
        if status == TIBRV_OK:
            ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret

    def subject(self) -> str:

        status, ret = tibrvcmEvent_GetListenerSubject(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    def tx(self) -> TibrvCmTx:

        status, tx = tibrvcmEvent_GetListenerTransport(self.id())
        if status == TIBRV_OK:
            ret = TibrvCmTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    def explicit(self) -> TibrvCmTx:
        status = tibrvcmEvent_SetExplicitConfirm(self.id())

        self._err = TibrvStatus.error(status)

        return status

    def confirm(self, msg: TibrvMsg) -> TibrvCmTx:
        if msg is None or not isinstance(msg, TibrvMsg):
            status = TIBRV_INVALID_MSG
            self._err = TibrvStatus.error(status)
            return status

        status = tibrvcmEvent_ConfirmMsg(self.id(), msg.id())

        self._err = TibrvStatus.error(status)

        return status

