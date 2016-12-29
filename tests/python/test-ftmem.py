
import threading
from datetime import datetime
import time
from pytibrv.Tibrv import *
from pytibrv.TibrvFt import *
import unittest


def callback(member: TibrvFtMember, groupName: str, action: tibrvftAction, closure):
    obj = closure
    obj.action = action

    print(datetime.now(), obj.name, ' -> ', action)

class App(threading.Thread):
    def __init__(self, name: str):
        threading.Thread.__init__(self)
        self.action = 0
        self.tx = None
        self.que = None
        self.disp = None
        self.ft = None
        self.name = name

    def start(self, weight: int = 50):
        self.tx = TibrvTx()
        status = self.tx.create(None, None, None)
        assert TIBRV_OK == status, TibrvStatus.text(status)

        self.que = TibrvQueue()
        status = self.que.create()
        assert TIBRV_OK == status, TibrvStatus.text(status)

        self.ft = TibrvFtMember()
        status = self.ft.create(self.que, TibrvFtMemberCallback(callback), self.tx,
                                'TEST', weight, 1, 1.0, 1.5, 2.0, self)
        assert TIBRV_OK == status, TibrvStatus.text(status)

        self.disp = TibrvDispatcher()
        status = self.disp.create(self.que)
        assert TIBRV_OK == status, TibrvStatus.text(status)

        threading.Thread.start(self)

    def stop(self):
        if self.ft != None:
            print(datetime.now(), self.name, 'IS STOPING ...')
            status = self.ft.destroy()
            assert TIBRV_OK == status, TibrvStatus.text(status)
            self.ft = None

    def close(self):
        self.stop()

        if self.disp is not None:
            status = self.disp.destroy()
            assert TIBRV_OK == status, TibrvStatus.text(status)
            self.disp = None

        if self.que is not None :
            status = self.que.destroy()
            assert TIBRV_OK == status, TibrvStatus.text(status)
            self.que = None

        if self.tx != 0:
            status = self.tx.destroy()
            assert TIBRV_OK == status, TibrvStatus.text(status)
            self.tx = None


    def run(self):

        print(datetime.now(), self.name, 'START RUNNING ')

        # when thread stopped, self.ft is 0
        while self.ft is not None:
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
        status = Tibrv.open()
        assert TIBRV_OK == status, TibrvStatus.text(status)

    @classmethod
    def tearDownClass(cls):
        Tibrv.close()

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
        self.assertIsNone(ap1.ft)

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
        self.assertIsNone(ap1.ft)
        time.sleep(0.1)

        time.sleep(2)
        self.assertEqual(TIBRVFT_ACTIVATE, ap2.action)

        # let time going
        time.sleep(5)
        ap2.close()
        self.assertIsNone(ap2.ft)

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
        self.assertIsNone(ap1.ft)
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
        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        que = TibrvQueue()
        ft = TibrvFtMember()
        status = ft.create(que, TibrvFtMemberCallback(callback), tx,
                           'MemberTest', 50, 1, 1.0, 1.5, 2.0, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        q = ft.queue()
        self.assertIsNotNone(q)
        self.assertEqual(que.id(), q.id())

        t = ft.tx()
        self.assertIsNotNone(t)
        self.assertEqual(tx.id(), t.id())

        sz = ft.name()
        self.assertIsNotNone(sz)
        self.assertEqual('MemberTest', sz)

        ft.weight = 100
        w = ft.weight
        self.assertEqual(100, w)

        status = ft.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        status = tx.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))


if __name__ == "__main__" :
    unittest.main(verbosity=2)
