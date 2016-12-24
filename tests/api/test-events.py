import datetime
import time
from pytibrv.api import *
from pytibrv.events import *
from pytibrv.disp import *
from pytibrv.msg import *
import unittest


def callback(event: tibrvEvent, msg: tibrvMsg, closure):

    status, subj = tibrvMsg_GetSendSubject(msg)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)

    status, sz = tibrvMsg_ConvertToString(msg)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)


    print('RECV [{}] < {}'.format(subj, sz))

    test = tibrvClosure(closure)

    # this is for test purpose,
    # usually, do'nt need to detech msg in callback()
    # unless, you need to keep it to be use later
    test.msg_recv = msg

    # detech from TIBRV, must destroy later
    status = tibrvMsg_Detach(msg)
    assert TIBRV_OK == status, tibrvStatus_GetText(status)


class EventTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()

    def test_create(self):

        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, que = tibrvQueue_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # Create an INBOX
        status, subj = tibrvTransport_CreateInbox(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, lst = tibrvEvent_CreateListener(que, callback, tx, subj, self)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, disp = tibrvDispatcher_Create(que)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, m = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateString(m, 'DATA', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetSendSubject(m, subj)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        print('')
        self.msg_recv = 0
        status = tibrvTransport_Send(tx, m)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        timeout = time.time() + 2

        while time.time() <= timeout:
            if self.msg_recv != 0:
                break
            time.sleep(0.1)
            #print('SLEEP...')

        self.assertNotEqual(0, self.msg_recv)
        status, sz = tibrvMsg_GetString(self.msg_recv, 'DATA')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('TEST', sz)

        status = tibrvMsg_Destroy(m)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(self.msg_recv)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvDispatcher_Destroy(disp)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvEvent_Destroy(lst)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvQueue_Destroy(que)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


if __name__ == "__main__" :
    unittest.main(verbosity=2)
