##
# pytibrv/cm.py
#   tibrvcmTransport_XXX
#
# LAST MODIFIED : V1.0 20161226 ARIEN
#
# DESCRIPTIONS
# ------------------------------------------------------
#
#
# FEATURES: * = un-implement
# ------------------------------------------------------
#   tibrvcmTransport_CreateDistributedQueue
#   tibrvcmTransport_CreateDistributedQueueEx
#   tibrvcmTransport_SetCompleteTime
#   tibrvcmTransport_GetCompleteTime
#   tibrvcmTransport_SetWorkerWeight
#   tibrvcmTransport_GetWorkerWeight
#   tibrvcmTransport_SetWorkerTasks
#   tibrvcmTransport_GetWorkerTasks
#   tibrvcmTransport_SetTaskBacklogLimit
#   tibrvcmTransport_SetTaskBacklogLimitInBytes
#   tibrvcmTransport_SetTaskBacklogLimitInMessages
#   tibrvcmTransport_SetPublisherInactivityDiscardInterval
#   tibrvcmTransport_GetUnassignedMessageCount
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
                 _c_tibrv_status, _c_tibrvTransport, \
                 _c_tibrv_u16, _c_tibrv_i32, _c_tibrv_u32, _c_tibrv_f64, \
                 _c_tibrv_str, tibrvTransport

from .cm import _c_tibrvcmTransport, tibrvcmTransport


# module variable
_rvdq = _load('tibrvcmq')

# CONSTANTS
TIBRVCM_DEFAULT_COMPLETE_TIME       = 0
TIBRVCM_DEFAULT_WORKER_WEIGHT       = 1
TIBRVCM_DEFAULT_WORKER_TASKS        = 1
TIBRVCM_DEFAULT_SCHEDULER_WEIGHT    = 1
TIBRVCM_DEFAULT_SCHEDULER_HB        = 1.0
TIBRVCM_DEFAULT_SCHEDULER_ACTIVE    = 3.5
TIBRVCMQ_LIMIT_MSGS                 = 0
TIBRVCMQ_LIMIT_BYTES                = 1

##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_CreateDistributedQueueEx(
#                   tibrvcmTransport*           cmTransport,
#                   tibrvTransport              transport,
#                   const char*                 cmName,
#                   tibrv_u32                   workerWeight,
#                   tibrv_u32                   workerTasks,
#                   tibrv_u16                   schedulerWeight,
#                   tibrv_f64                   schedulerHeartbeat,
#                   tibrv_f64                   schedulerActivation
#               );
#
_rvdq.tibrvcmTransport_CreateDistributedQueueEx.argtypes = [_ctypes.POINTER(_c_tibrvcmTransport),
                                                            _c_tibrvTransport,
                                                            _c_tibrv_str,
                                                            _c_tibrv_u32,
                                                            _c_tibrv_u32,
                                                            _c_tibrv_u16,
                                                            _c_tibrv_f64,
                                                            _c_tibrv_f64]
_rvdq.tibrvcmTransport_CreateDistributedQueueEx.restype = _c_tibrv_status

def tibrvcmTransport_CreateDistributedQueueEx(tx: tibrvTransport, cmName: str,
                            workerWeight: int, workerTasks: int, schedulerWeight: int,
                            schedulerHeartbeat: float, schedulerActivation: float) \
        -> (tibrv_status, tibrvcmTransport):

    cmtx = _c_tibrvcmTransport(0)
    tx = _c_tibrvTransport(tx)
    name = _cstr(cmName)
    wrk_wt = _c_tibrv_u32(workerWeight)
    wrk_tasks = _c_tibrv_u32(workerTasks)
    sch_wt = _c_tibrv_u16(schedulerWeight)
    sch_hbt = _c_tibrv_f64(schedulerHeartbeat)
    sch_act = _c_tibrv_f64(schedulerActivation)

    status = _rvdq.tibrvcmTransport_CreateDistributedQueueEx(
                    _ctypes.byref(cmtx), tx, name,
                    wrk_wt, wrk_tasks, sch_wt, sch_hbt, sch_act)

    return status, cmtx.value



def tibrvcmTransport_CreateDistributedQueue(tx: tibrvTransport, cmName: str) \
                            -> (tibrv_status, tibrvcmTransport):

    return tibrvcmTransport_CreateDistributedQueueEx(
                    tx, cmName,
                    TIBRVCM_DEFAULT_WORKER_WEIGHT,
                    TIBRVCM_DEFAULT_WORKER_TASKS,
                    TIBRVCM_DEFAULT_SCHEDULER_WEIGHT,
                    TIBRVCM_DEFAULT_SCHEDULER_HB,
                    TIBRVCM_DEFAULT_SCHEDULER_ACTIVE)


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SetCompleteTime(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_f64                   completeTime
#               );
#
_rvdq.tibrvcmTransport_SetCompleteTime.argtypes = [_c_tibrvcmTransport, _c_tibrv_f64]
_rvdq.tibrvcmTransport_SetCompleteTime.restype = _c_tibrv_status

def tibrvcmTransport_SetCompleteTime(cmTransport: tibrvcmTransport, completeTime: float) -> tibrv_status:

    cmtx = _c_tibrvcmTransport(cmTransport)
    tt = _c_tibrv_f64(completeTime)

    status = _rvdq.tibrvcmTransport_SetCompleteTime(cmtx, tt)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetCompleteTime(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_f64*                  completeTime
#               );
#
_rvdq.tibrvcmTransport_GetCompleteTime.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_f64)]
_rvdq.tibrvcmTransport_GetCompleteTime.restype = _c_tibrv_status

def tibrvcmTransport_GetCompleteTime(cmTransport: tibrvcmTransport) -> (tibrv_status, float):

    cmtx = _c_tibrvcmTransport(cmTransport)
    ret = _c_tibrv_f64(0)

    status = _rvdq.tibrvcmTransport_GetCompleteTime(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SetWorkerWeight(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_u32                   workerWeight
#               );
#
_rvdq.tibrvcmTransport_SetWorkerWeight.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetWorkerWeight.restype = _c_tibrv_status

def tibrvcmTransport_SetWorkerWeight(cmTransport: tibrvcmTransport, workerWeight: int) -> tibrv_status:

    cmtx = _c_tibrvcmTransport(cmTransport)
    val = _c_tibrv_u32(workerWeight)

    status = _rvdq.tibrvcmTransport_SetWorkerWeight(cmtx, val)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetWorkerWeight(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_u32*                  workerWeight
#               );
#
_rvdq.tibrvcmTransport_GetWorkerWeight.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetWorkerWeight.restype = _c_tibrv_status

def tibrvcmTransport_GetWorkerWeight(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    cmtx = _c_tibrvcmTransport(cmTransport)
    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetWorkerWeight(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv_status tibrvcmTransport_SetWorkerTasks(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_u32                   listenerTasks
#               );
#
_rvdq.tibrvcmTransport_SetWorkerTasks.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetWorkerTasks.restype = _c_tibrv_status

def tibrvcmTransport_SetWorkerTasks(cmTransport: tibrvcmTransport, listenerTasks: int) -> tibrv_status:

    cmtx = _c_tibrvcmTransport(cmTransport)
    val = _c_tibrv_u32(listenerTasks)

    status = _rvdq.tibrvcmTransport_SetWorkerTasks(cmtx, val)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetWorkerTasks(
#                   tibrvcmTransport            cmTransport,
#                   tibrv_u32*                  listenerTasks
#               );
#
_rvdq.tibrvcmTransport_GetWorkerTasks.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetWorkerTasks.restype = _c_tibrv_status

def tibrvcmTransport_GetWorkerTasks(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    cmtx = _c_tibrvcmTransport(cmTransport)
    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetWorkerTasks(cmtx, _ctypes.byref(ret))

    return status, ret.value


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SetTaskBacklogLimit(
#                   tibrvcmTransport	cmTransport,
#                   tibrv_u32			limitType,
#                   tibrv_u32			limitValue
#               );
#
_rvdq.tibrvcmTransport_SetTaskBacklogLimit.argtypes = [_c_tibrvcmTransport, _c_tibrv_u32, _c_tibrv_u32]
_rvdq.tibrvcmTransport_SetTaskBacklogLimit.restype = _c_tibrv_status

def tibrvcmTransport_SetTaskBacklogLimit(cmTransport: tibrvcmTransport, limitType: int,
                                         limitValue: int) -> tibrv_status:

    cmtx = _c_tibrvcmTransport(cmTransport)
    ty = _c_tibrv_u32(limitType)
    val = _c_tibrv_u32(limitValue)

    status = _rvdq.tibrvcmTransport_SetTaskBacklogLimit(cmtx, ty, val)

    return status


def tibrvcmTransport_SetTaskBacklogLimitInBytes(cmTransport: tibrvcmTransport,
                                                limitBySizeInBytes: int) -> tibrv_status:

    return tibrvcmTransport_SetTaskBacklogLimit(cmTransport, TIBRVCMQ_LIMIT_BYTES, limitBySizeInBytes)


def tibrvcmTransport_SetTaskBacklogLimitInMessages(cmTransport: tibrvcmTransport,
                                                   limitByMessages: int) -> tibrv_status:

    return tibrvcmTransport_SetTaskBacklogLimit(cmTransport, TIBRVCMQ_LIMIT_MSGS, limitByMessages)


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_SetPublisherInactivityDiscardInterval(
#                   tibrvcmTransport    cmTransport,
#                   tibrv_i32           timeout
#               );
#
_rvdq.tibrvcmTransport_SetPublisherInactivityDiscardInterval.argtypes = [_c_tibrvcmTransport, _c_tibrv_i32]
_rvdq.tibrvcmTransport_SetPublisherInactivityDiscardInterval.restype = _c_tibrv_status


def tibrvcmTransport_SetPublisherInactivityDiscardInterval(cmTransport: tibrvcmTransport,
                                                           timeout: int) -> tibrv_status:
    cmtx = _c_tibrvcmTransport(cmTransport)
    val = _c_tibrv_i32(timeout)

    status = _rvdq.tibrvcmTransport_SetPublisherInactivityDiscardInterval(cmtx, val)

    return status


##
# tibrv/cm.h
# tibrv_status tibrvcmTransport_GetUnassignedMessageCount(
#                   tibrvcmTransport	cmTransport,
#                   tibrv_u32			*msgCount);
#
_rvdq.tibrvcmTransport_GetUnassignedMessageCount.argtypes = [_c_tibrvcmTransport, _ctypes.POINTER(_c_tibrv_u32)]
_rvdq.tibrvcmTransport_GetUnassignedMessageCount.restype = _c_tibrv_status

def tibrvcmTransport_GetUnassignedMessageCount(cmTransport: tibrvcmTransport) -> (tibrv_status, int):

    cmtx = _c_tibrvcmTransport(cmTransport)
    ret = _c_tibrv_u32(0)

    status = _rvdq.tibrvcmTransport_GetUnassignedMessageCount(cmtx, _ctypes.byref(ret))

    return status, ret.value
