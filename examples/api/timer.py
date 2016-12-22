##
# timer.py
#   Demo TIBRV Timer Callback
#
# LAST MODIFIED: V1.0 2016-12-22 ARIEN arien.chen@gmail.com
#
import sys
import time
from pytibrv.events import *
from pytibrv.disp import *
from datetime import datetime


def callback(event:tibrvEvent, msg: tibrvMsg, closure):
    print('HI', datetime.now())

# MAIN PROGRAM
def main(argv):

    status = tibrv_Open()
    assert TIBRV_OK == status, tibrvStatus_GetText(status)

    # DEFAULT QUE
    que = TIBRV_DEFAULT_QUEUE

    # create timer
    status, event = tibrvEvent_CreateTimer(que, callback, 0.5)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)

    # use dispatcher thread
    print('create dispacher thread')
    status, disp = tibrvDispatcher_Create(que, TIBRV_WAIT_FOREVER)

    # run for 5 sec
    timeout = time.time() + 5
    cnt = 0
    while time.time() <= timeout:
        cnt += 1
        print(cnt, 'WAITING ...')
        time.sleep(1.0)

    status = tibrvDispatcher_Destroy(disp)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)

    # dispatch in main(current) thread
    # run for 5 sec
    print('run in main thread')
    timeout = time.time() + 5
    while time.time() <= timeout:
        tibrvQueue_TimedDispatch(que, 1.0)

    status = tibrvEvent_DestroyEx(event)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)

    tibrv_Close()
    print('end')

if __name__ == "__main__":
    main(sys.argv)
