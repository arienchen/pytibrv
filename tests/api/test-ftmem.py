
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


class MemberTest(unittest.TestCase):

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

        timeout = time.time() + 5
        while time.time() <= timeout:
            if ap1.action == TIBRVFT_ACTIVATE:
                break
            time.sleep(1.0)

        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)

        # let ap1 to run 5 sec
        time.sleep(5)

        ap1.stop()
        # when you destroy ftMember
        # there is no chance to get callback
        # so, self.action would be still TIBRVFT_ACTIVATE
        self.assertEqual(0, ap1.ft)

        ap1.close()

    def test_failove(self):

        # action matrix
        #           AP1           AP2           DESCRIPTION
        # ---------------------------------------------------
        # 1.        0                           AP1 CREATED
        # 2.        0 -> ACT                    AP1 FT CALLBACK
        # 3.        ACT                         AP1 ACTIVATED
        # 4.                      0             AP2 CREATED
        # 5.        ACT                         AP1 CLOSED, NO CALLBACK
        # 6.                      0 -> ACT      AP2 FT CALLBACK
        # 7.                      ACT           AP2 ACTIVATED
        #
        print('\nTEST FAILOVER')
        ap1 = App('AP1')
        ap1.start()

        # let ap1 became ACTIVATE
        timeout = time.time() + 5
        while time.time() <= timeout:
            if ap1.action == TIBRVFT_ACTIVATE:
                break
            time.sleep(1.0)

        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)

        # start another instance
        ap2 = App('AP2')
        ap2.start()

        # let time going
        # ap1 should be ACTIVATE
        # ap2 should be still 0 (initial value)
        time.sleep(5.0)
        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)
        self.assertEqual(0, ap2.action)

        # simulate ap1 is dead
        ap1.close()
        self.assertEqual(0, ap1.ft)
        time.sleep(0.1)

        time.sleep(2)
        self.assertEqual(TIBRVFT_ACTIVATE, ap2.action)

        # let time going
        time.sleep(5)
        ap2.close()
        self.assertEqual(0, ap2.ft)

    def test_primary(self):

        # action matrix: AP1 is PRIMARY
        #           AP1           AP2           DESCRIPTION
        # ---------------------------------------------------
        # 1.        0                           AP1 CREATED, PRIMARY
        # 2.        0 -> ACT                    AP1 FT CALLBACK
        # 3.        ACT                         AP1 ACTIVATED
        # 4.                      0             AP2 CREATED
        # 5.        ACT                         AP1 CLOSED, NO CALLBACK
        # 6.                      0 -> ACT      AP2 FT CALLBACK
        # 7.                      ACT           AP2 ACTIVATED
        # 8.        0                           AP1 CREATED, PRIMARY
        # 9.                      ACT -> DEACT  AP2 FT CALLBACK
        # 10.                     DEACT         AP2 DEACTIVATED
        # 11.       0 -> ACT                    AP1 FT CALLBACK
        # 12.       ACT                         AP1 ACTIVATED
        #
        print('\nTEST PRIMARY')
        ap1 = App('AP1')
        ap1.start(100)          # More Weight

        # let ap1 became ACTIVATE
        timeout = time.time() + 5
        while time.time() <= timeout:
            if ap1.action == TIBRVFT_ACTIVATE:
                break
            time.sleep(1.0)

        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)

        # start another instance
        ap2 = App('AP2')
        ap2.start(50)           #

        # let time going
        # ap1 should be ACTIVATE
        # ap2 should be still 0 (initial value)
        time.sleep(5.0)
        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)
        self.assertEqual(0, ap2.action)

        # simulate ap1 is dead
        ap1.close()
        self.assertEqual(0, ap1.ft)
        time.sleep(0.1)

        time.sleep(2)
        self.assertEqual(TIBRVFT_ACTIVATE, ap2.action)


        # ap1 is back again
        ap1 = App('AP1')
        ap1.start(100)  # More Weight

        # let time going
        time.sleep(5)
        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)
        self.assertEqual(TIBRVFT_DEACTIVATE, ap2.action)

        ap1.close()
        ap2.close()

    def test_getset(self):
        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        que = TIBRV_DEFAULT_QUEUE

        status, ft = tibrvftMember_Create(que, callback, tx, 'MemberTest',
                                          50, 1, 1.0, 1.5, 2.0, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, q = tibrvftMember_GetQueue(ft)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(que, q)

        status, t = tibrvftMember_GetTransport(ft)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(tx, t)

        status, sz = tibrvftMember_GetGroupName(ft)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('MemberTest', sz)

        status = tibrvftMember_SetWeight(ft, 100)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, w = tibrvftMember_GetWeight(ft)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(100, w)

        status = tibrvftMember_Destroy(ft)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


if __name__ == "__main__" :
    unittest.main(verbosity=2)
