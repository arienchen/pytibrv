
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

def ft_mon(monitor: TibrvFtMonitor, groupName: str, numActiveMembers: int, closure):
    obj = closure
    obj.cnt = numActiveMembers
    print(datetime.now(), groupName, numActiveMembers)


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


class MonitorTest(unittest.TestCase):

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

        # WAIT AP1 became ACTIVATED
        # wait for activationInterval
        time.sleep(2.5)
        self.assertEqual(TIBRVFT_ACTIVATE, ap1.action)

        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))
        que = TibrvQueue()
        disp = TibrvDispatcher()
        status = disp.create(que)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        # pass self as closure, reset cnt = 0
        self.cnt = 0
        monitor = TibrvFtMonitor()
        status = monitor.create(que, TibrvFtMonitorCallback(ft_mon), tx, 'TEST', 1.0, self)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

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

        status = disp.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        status = tx.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

    def test_getset(self):
        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))
        que = TibrvQueue()

        # pass self as closure, reset cnt = 0
        self.cnt = 0
        monitor = TibrvFtMonitor()
        status = monitor.create(que, TibrvFtMonitorCallback(ft_mon), tx, 'MonitorTest', 1.0, self)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        q = monitor.queue()
        self.assertIsNotNone(q)
        self.assertEqual(que.id(), q.id())

        t = monitor.tx()
        self.assertIsNotNone(t)
        self.assertEqual(tx.id(), t.id())

        sz = monitor.name()
        self.assertIsNotNone(sz)
        self.assertEqual('MonitorTest', sz)

        status = monitor.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        status = tx.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))


if __name__ == "__main__" :
    unittest.main(verbosity=2)
