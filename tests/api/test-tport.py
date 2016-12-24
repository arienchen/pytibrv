from pytibrv.api import *
from pytibrv.status import *
from pytibrv.tport import *
from pytibrv.msg import *
import unittest

class TransportTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        assert status == TIBRV_OK, tibrvStatus_GetText(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()

    def test_create_default(self):

        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvTransport_GetService(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('', sz)

        status, sz = tibrvTransport_GetNetwork(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('', sz)

        status, sz = tibrvTransport_GetDaemon(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('7500', sz)

        status, sz = tibrvTransport_GetDescription(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertIsNone(sz)

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # transport destroyed
        # should return TIBRV_INVALID_TRANSPORT
        status, sz = tibrvTransport_GetService(tx)
        self.assertEqual(TIBRV_INVALID_TRANSPORT, status)

        status, sz = tibrvTransport_GetNetwork(tx)
        self.assertEqual(TIBRV_INVALID_TRANSPORT, status)

        status, sz = tibrvTransport_GetDaemon(tx)
        self.assertEqual(TIBRV_INVALID_TRANSPORT, status)

        status, sz = tibrvTransport_GetDescription(tx)
        self.assertEqual(TIBRV_INVALID_TRANSPORT, status)

    def test_create(self):

        service = '12345'
        network = ';225.1.1.1'
        daemon  = '2000'
        status, tx = tibrvTransport_Create(service, network, daemon)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvTransport_GetService(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(service, sz)

        status, sz = tibrvTransport_GetNetwork(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(network, sz)

        status, sz = tibrvTransport_GetDaemon(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(daemon, sz)

        status = tibrvTransport_SetDescription(tx, 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvTransport_GetDescription(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('TEST', sz)

        status, subj = tibrvTransport_CreateInbox(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertIsNotNone(subj)

        status = tibrvTransport_RequestReliability(tx, 100)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def test_send(self):

        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateString(msg, 'DATA', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetSendSubject(msg, 'TEST.A')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Send(tx, msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetReplySubject(msg, 'TEST.ACK')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetSendSubject(msg, 'TEST.B')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Send(tx, msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def test_request(self):

        status, tx = tibrvTransport_Create(None, None, None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateString(msg, 'DATA', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetSendSubject(msg, 'TEST.A')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ack = tibrvTransport_SendRequest(tx, msg,  1.0)
        #self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(TIBRV_TIMEOUT, status, tibrvStatus_GetText(status))
        self.assertIsNone(ack)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvTransport_Destroy(tx)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


if __name__ == "__main__":
    unittest.main(verbosity=2)
