##
# pytibrv/TibrvFt.py
#   TIBRV Library for PYTHON
#   TibrvFtMember       <- tibrvftMember_XXX
#   TibrvFtMonitor      <- tibrvftMonitor_XXX
#
# LAST MODIFIED : V1.1 20161227 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
# 1.
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20161227 V1.1 ARIEN arien.chen@gmail.com
#   change readonly property to normal function
#
# 20161226 V1,0 ARIEN arien.chen@gmail.com
#   CREATED
#

from pytibrv.status import TIBRV_INVALID_CALLBACK, TIBRV_INVALID_QUEUE, TIBRV_INVALID_TRANSPORT,\
                           TIBRV_INVALID_ARG

from pytibrv.events import tibrvClosure

from pytibrv.Tibrv import TibrvQueue, TibrvTx, TibrvStatus, TibrvError

from pytibrv.ft import *

class TibrvFtMemberCallback:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, member, groupName: str, action: int, closure):
        pass

    def _register(self):
        def _cb(member: tibrvftMember, groupName: bytes, action: tibrvftAction, closure):
            ftmem = TibrvFtMember(member)
            grp = groupName.decode()
            cz = tibrvClosure(closure)

            self.callback(ftmem, grp, action, cz)

        return _cb

class TibrvFtMember:
    def __init__(self, member: tibrvftMember = 0):
        self._ftmem = tibrvftMember(member)
        self._err = None

    def id(self):
        return self._ftmem

    def create(self, que: TibrvQueue, callback: TibrvFtMemberCallback, tx: TibrvTx,
               groupName: str, weight: int = 50, activeGoal: int = 1, hbt: float = 1.0,
               prepare: float = 2.5, activate: float = 4.0, closure = None) -> tibrv_status:

        if que is None or not isinstance(que, TibrvQueue):
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        if tx is None or not isinstance(tx, TibrvTx):
            status = TIBRV_INVALID_TRANSPORT
            self._err = TibrvStatus.error(status)
            return status

        if groupName is None:
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)
            return status

        if callback is None or not isinstance(callback, TibrvFtMemberCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status, self._ftmem = tibrvftMember_Create(que.id(), callback._register(), tx.id(), groupName,
                                                   weight, activeGoal, hbt, prepare, activate, closure)

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:

        status = tibrvftMember_Destroy(self._ftmem)
        self._ftmem = 0

        return status

    def error(self) -> TibrvError:
        return self._err

    def queue(self) -> TibrvQueue:
        ret = None

        status, q = tibrvftMember_GetQueue(self.id())
        if status == TIBRV_OK:
            ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret

    def tx(self) -> TibrvTx:
        ret = None

        status, tx = tibrvftMember_GetTransport(self.id())
        if status == TIBRV_OK:
            ret = TibrvTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    def name(self) -> str:

        status, ret = tibrvftMember_GetGroupName(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def weight(self) -> int:

        status, ret = tibrvftMember_GetWeight(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @weight.setter
    def weight(self, wt: int):

        status = tibrvftMember_SetWeight(self.id(), wt)
        self._err = TibrvStatus.error(status)



class TibrvFtMonitorCallback:

    def __init__(self, cb = None):
        if cb is not None:
            self.callback = cb

    def callback(self, monitor, groupName: str, members: int, closure):
        pass

    def _register(self):
        def _cb(monitor: tibrvftMonitor, groupName: bytes, members: int, closure):
            ftmon = TibrvFtMonitor(monitor)
            grp = groupName.decode()
            cz = tibrvClosure(closure)

            self.callback(ftmon, grp, members, cz)

        return _cb


class TibrvFtMonitor:
    def __init__(self, monitor: tibrvftMonitor = 0):
        self._ftmon = tibrvftMonitor(monitor)
        self._err = None

    def id(self):
        return self._ftmon

    def create(self, que: TibrvQueue, callback: TibrvFtMemberCallback, tx: TibrvTx, groupName: str,
               hbt: float, closure) -> tibrv_status:

        if que is None or not isinstance(que, TibrvQueue):
            status = TIBRV_INVALID_QUEUE
            self._err = TibrvStatus.error(status)
            return status

        if callback is None or not isinstance(callback, TibrvFtMonitorCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        if tx is None or not isinstance(tx, TibrvTx):
            status = TIBRV_INVALID_TRANSPORT
            self._err = TibrvStatus.error(status)
            return status

        if groupName is None or hbt is None:
            status = TIBRV_INVALID_ARG
            self._err = TibrvStatus.error(status)
            return status

        status, self._ftmon = tibrvftMonitor_Create(que.id(), callback._register(), tx.id(), groupName,
                                                    hbt, closure)

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:

        status = tibrvftMonitor_Destroy(self._ftmon)
        self._ftmon = 0

        return status

    def error(self) -> TibrvError:
        return self._err

    def queue(self) -> TibrvQueue:
        ret = None

        status, q = tibrvftMonitor_GetQueue(self.id())
        if status == TIBRV_OK:
            ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret

    def tx(self) -> TibrvTx:

        ret = None

        status, tx = tibrvftMonitor_GetTransport(self.id())
        if status == TIBRV_OK:
            ret = TibrvTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    def name(self) -> str:

        status, ret = tibrvftMonitor_GetGroupName(self.id())
        self._err = TibrvStatus.error(status)

        return ret
