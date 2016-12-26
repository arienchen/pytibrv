
import threading
from datetime import datetime
import time
from pytibrv.api import *
from pytibrv.status import *
from pytibrv.tport import *
from pytibrv.events import *
from pytibrv.disp import *
from pytibrv.queue import *
from pytibrv.ft import *
import unittest


def callback(member: tibrvftMember, groupName: bytes, action: tibrvftAction, closure):
    name = groupName.decode()
    obj = tibrvClosure(closure)
    obj.action = action

    print(datetime.now(), obj.name, ' -> ', action)

def ft_mon(monitor: tibrvftMonitor, groupName: bytes, numActiveMembers: int, closure):
    name = groupName.decode()
    obj = tibrvClosure(closure)
    obj.cnt = numActiveMembers
    print(datetime.now(), name, numActiveMembers)


class App(threading.Thread):
    def __init__(self, name: str):
        threading.Thread.__init__(self)
        self.action = 0
        self.tx = 0
        self.que = 0
        self.disp = 0
        self.ft = 0
        self.name = name

    def start(self, weight: int = 50):
        status, self.tx = tibrvTransport_Create(None, None, None)
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

        status, self.que = tibrvQueue_Create()
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

        status, self.ft = tibrvftMember_Create(self.que, callback, self.tx, 'TEST', \
                                               weight, 1, 1.0, 1.5, 2.0, self)
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

        status, self.disp = tibrvDispatcher_Create(self.que)
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

        threading.Thread.start(self)

    def stop(self):
        if self.ft != 0:
            print(datetime.now(), self.name, 'IS STOPING ...')
            status = tibrvftMember_Destroy(self.ft)
            assert TIBRV_OK == status, tibrvStatus_GetText(status)
            self.ft = 0

    def close(self):
        if self.tx != 0:
            self.stop()

        if self.disp != 0:
            status = tibrvDispatcher_Destroy(self.disp)
            assert TIBRV_OK == status, tibrvStatus_GetText(status)
            self.disp = 0

        if self.que != 0:
            status = tibrvQueue_Destroy(self.que)
            assert TIBRV_OK == status, tibrvStatus_GetText(status)
            self.que = 0

        if self.tx != 0:
            status = tibrvTransport_Destroy(self.tx)
            assert TIBRV_OK == status, tibrvStatus_GetText(status)
            self.tx = 0


    def run(self):

        print(datetime.now(), self.name, 'START RUNNING ')

        # when thread stopped, self.ft is 0
        while self.ft != 0:
            if self.action != TIBRVFT_ACTIVATE:
                print(datetime.now(), self.name, 'IS DEACTIVATED')
                time.sleep(0.5)
                continue

            print(datetime.now(), self.name, 'IS ACTIVATED')
            time.sleep(1.0)
            print(datetime.now(), self.name, 'RUN SOMETHING')

        print(datetime.now(), self.name, 'EXIT NOW')


class MonitorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()


    def test_create(self):

        print('')
        ap1 = App('AP1')
        ap1.start()

        # WAIT AP1 became ACTIVATED
        # wait for activationInterval
        time.sleep(2.5)
        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)

        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        que = TIBRV_DEFAULT_QUEUE

        status, disp = tibrvDispatcher_Create(que)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # pass self as closure, reset cnt = 0
        self.cnt = 0
        status, monitor = tibrvftMonitor_Create(que, ft_mon, tx, 'TEST', 1.0, self)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # wait at least for a HBT
        time.sleep(1.5)

        self.assertEqual(1, self.cnt)

        # let ap1 do something
        time.sleep(1.0)
        ap1.stop()

        # let monitor detect the change
        time.sleep(0.1)

        self.assertEqual(0, self.cnt)

        ap1.close()

        status = tibrvDispatcher_Destroy(disp)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))



if __name__ == "__main__" :
    unittest.main(verbosity=2)
