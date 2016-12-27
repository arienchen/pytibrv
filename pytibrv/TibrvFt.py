##
# pytibrv/Tibrv.py
#   TIBRV Library for PYTHON
#
# LAST MODIFIED : V1.0 20161224 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
#
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20161224 ARIEN V1.0
#   CREATED
#

from pytibrv.status import TIBRV_ID_IN_USE, TIBRV_INVALID_ARG, TIBRV_INVALID_CALLBACK
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

    def create(self, que: TibrvQueue, callback: TibrvFtMemberCallback, tx: TibrvTx, groupName: str,
               weight: int, activeGoal: int, hbt: float, prepare: float, activate: float, closure) -> tibrv_status:

        if self.id() != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if not isinstance(callback, TibrvFtMemberCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status, self._ftmem = tibrvftMember_Create(que.id(), callback._register(), tx.id(), groupName,
                                 weight, activeGoal, hbt, prepare, activate, closure)

        self._err = TibrvStatus.error(status)
        return status

    def destroy(self) -> tibrv_status:
        if self._ftmem == 0:
            return TIBRV_INVALID_ARG

        status = tibrvftMember_Destroy(self._ftmem)
        self._ftmem = 0

        return status

    @property
    def error(self) -> TibrvError:
        return self._err


    @property
    def queue(self) -> TibrvQueue:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_ARG
        else:
            status, q = tibrvftMember_GetQueue(self.id())
            if status == TIBRV_OK:
                ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret

    @property
    def tx(self) -> TibrvTx:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_ARG
        else:
            status, tx = tibrvftMember_GetTransport(self.id())
            if status == TIBRV_OK:
                ret = TibrvTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    @property
    def name(self) -> str:
        ret = None
        status, ret = tibrvftMember_GetGroupName(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def weight(self) -> int:
        ret = None
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

        if self.id() != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if not isinstance(callback, TibrvFtMonitorCallback):
            status = TIBRV_INVALID_CALLBACK
            self._err = TibrvStatus.error(status)
            return status

        status, self._ftmon = tibrvftMonitor_Create(que.id(), callback._register(), tx.id(), groupName,
                                 hbt, closure)

        self._err = TibrvStatus.error(status)
        return status

    def destroy(self) -> tibrv_status:
        if self._ftmon == 0:
            return TIBRV_INVALID_ARG

        status = tibrvftMonitor_Destroy(self._ftmon)
        self._ftmon = 0

        return status

    @property
    def error(self) -> TibrvError:
        return self._err

    @property
    def queue(self) -> TibrvQueue:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_ARG
        else:
            status, q = tibrvftMonitor_GetQueue(self.id())
            if status == TIBRV_OK:
                ret = TibrvQueue(q)

        self._err = TibrvStatus.error(status)

        return ret

    @property
    def tx(self) -> TibrvTx:
        ret = None
        if self.id() == 0:
            status = TIBRV_INVALID_ARG
        else:
            status, tx = tibrvftMonitor_GetTransport(self.id())
            if status == TIBRV_OK:
                ret = TibrvTx(tx)

        self._err = TibrvStatus.error(status)

        return ret

    @property
    def name(self) -> str:
        ret = None
        status, ret = tibrvftMonitor_GetGroupName(self.id())
        self._err = TibrvStatus.error(status)

        return ret
