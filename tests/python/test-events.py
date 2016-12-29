import datetime
import time
from pytibrv.Tibrv import *
import unittest

class EventTest(unittest.TestCase, TibrvMsgCallback):

    @classmethod
    def setUpClass(cls):
        status = Tibrv.open()
        if status != TIBRV_OK:
            raise TibrvError(status)

    @classmethod
    def tearDownClass(cls):
        Tibrv.close()

    def callback(self, event: TibrvEvent, msg: TibrvMsg, closure):
        print('RECV [{}] < {}'.format(msg.sendSubject, str(msg)))

        self.msg_recv = msg
        # detech from TIBRV, must destroy later
        status = msg.detach()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))


    def test_create(self):

        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        que = TibrvQueue()
        status = que.create('TEST')
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        # Create an INBOX
        subj = tx.inbox()
        lst = TibrvListener()
        status = lst.create(que, self, tx, subj)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        disp = TibrvDispatcher()
        status = disp.create(que)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        m = TibrvMsg.create()
        m.setStr('DATA', 'TEST')

        print('')
        self.msg_recv = None
        status = tx.send(m, subj)

        self.timeout = time.time() + 10000

        while time.time() <= self.timeout:
            if self.msg_recv is not None:
                break
            time.sleep(0.1)
            #print('SLEEP...')

        self.assertIsNotNone(self.msg_recv)
        self.assertEqual(m.getStr('DATA'), self.msg_recv.getStr('DATA'))

        del self.msg_recv
        del m
        del disp
        del lst
        del que
        del tx



if __name__ == "__main__" :
   unittest.main(verbosity=2)
