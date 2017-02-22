##
# pytibrv/TibrvDQ.py
#   TIBRV Library for PYTHON
#
#
# LAST MODIFIED : V1.0 20170222 ARIEN arien.chen@gmail.com
#
# DESCRIPTIONS
# -----------------------------------------------------------------------------
#
#
# CHANGED LOGS
# -----------------------------------------------------------------------------
# 20170222 ARIEN V1.0
#   CREATED
#

from .status import TIBRV_OK, TIBRV_ID_IN_USE, TIBRV_INVALID_ARG, TIBRV_INVALID_CALLBACK, \
                    TIBRV_INVALID_TRANSPORT, TIBRV_INVALID_MSG

from .Tibrv import tibrv_status, TibrvTx, TibrvStatus, TibrvError

from .cm import tibrvcmTransport, tibrvcmTransport_Destroy
from .dq import tibrvcmTransport_CreateDistributedQueueEx, \
                tibrvcmTransport_GetCompleteTime, tibrvcmTransport_SetCompleteTime, \
                tibrvcmTransport_GetUnassignedMessageCount, \
                tibrvcmTransport_GetWorkerWeight, tibrvcmTransport_SetWorkerWeight, \
                tibrvcmTransport_GetWorkerTasks, tibrvcmTransport_SetWorkerTasks, \
                tibrvcmTransport_SetTaskBacklogLimitInBytes, tibrvcmTransport_SetTaskBacklogLimitInMessages



##-----------------------------------------------------------------------------
## TibrvDQ
##-----------------------------------------------------------------------------
class TibrvDQ:
    def __init__(self, cmdq: tibrvcmTransport = 0):
        self._cmdq = 0
        self._err = None

        if cmdq is not None:
            self._cmdq = cmdq

    def id(self):
        return self._cmdq

    def error(self) -> TibrvError:
        return self._err

    def create(self, tx: TibrvTx, cmName: str, wk_weight: int, wk_tasks: int,
               sch_weight: int, sch_hbt: int, sch_act: int) -> tibrv_status:

        if self._cmdq != 0:
            status = TIBRV_ID_IN_USE
            self._err = TibrvStatus.error(status)
            return status

        if tx is None or not isinstance(tx, TibrvTx):
            status = TIBRV_INVALID_TRANSPORT
            self._err = TibrvStatus.error(status)
            return status

        status, cmdq = tibrvcmTransport_CreateDistributedQueueEx(tx.id(), cmName, wk_weight, wk_tasks,
                                                                sch_weight, sch_hbt, sch_act)
        if status == TIBRV_OK:
            self._cmdq = cmdq

        self._err = TibrvStatus.error(status)

        return status

    def destroy(self) -> tibrv_status:
        status = tibrvcmTransport_Destroy(self._cmdq)

        self._cmdq = 0

        self._err = TibrvStatus.error(status)

        return status

    @property
    def completeTime(self) -> float:

        status, ret = tibrvcmTransport_GetCompleteTime(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @completeTime.setter
    def completeTime(self, timeout: float):

        status = tibrvcmTransport_SetCompleteTime(self.id(), timeout)
        self._err = TibrvStatus.error(status)


    def count(self) -> int:

        status, ret = tibrvcmTransport_GetUnassignedMessageCount(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @property
    def workerWeight(self) -> float:

        status, ret = tibrvcmTransport_GetWorkerWeight(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @workerWeight.setter
    def workerWeight(self, weight: int):

        status = tibrvcmTransport_SetWorkerWeight(self.id(), weight)
        self._err = TibrvStatus.error(status)

    @property
    def workerTasks(self) -> float:

        status, ret = tibrvcmTransport_GetWorkerTasks(self.id())
        self._err = TibrvStatus.error(status)

        return ret

    @workerTasks.setter
    def workerTasks(self, weight: int):

        status = tibrvcmTransport_SetWorkerTasks(self.id(), weight)
        self._err = TibrvStatus.error(status)


    def setBytesLimit(self, bytes: int) -> tibrv_status:

        status, ret = tibrvcmTransport_SetTaskBacklogLimitInBytes(self.id(), bytes)
        self._err = TibrvStatus.error(status)

        return ret

    def setMsgLimit(self, msgs: int) -> tibrv_status:

        status, ret = tibrvcmTransport_SetTaskBacklogLimitInMessages(self.id(), msgs)
        self._err = TibrvStatus.error(status)

        return ret

