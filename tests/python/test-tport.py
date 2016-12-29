from pytibrv.Tibrv import *
import unittest

class TransportTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = Tibrv.open()
        if status != TIBRV_OK:
            raise TibrvError(status)

    @classmethod
    def tearDownClass(cls):
        Tibrv.close()

    def test_create(self):

        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        self.assertEqual('', tx.service())
        self.assertEqual('', tx.network())
        self.assertEqual('7500', tx.daemon())     # Default is 7500
        self.assertIsNone(tx.description)

        tx.destroy()

        # transport destroyed
        # should return None
        self.assertIsNone(tx.service())
        self.assertIsNone(tx.network())
        self.assertIsNone(tx.daemon())
        self.assertIsNone(tx.description)

        del tx

        tx = TibrvTx()
        service = '12345'
        network=';225.1.1.1'
        daemon='2000'
        status = tx.create(service, network, daemon)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        self.assertEqual(service, tx.service())
        self.assertEqual(network, tx.network())
        self.assertEqual(daemon, tx.daemon())
        self.assertIsNone(tx.description)

        tx.description = 'TEST'
        self.assertEqual('TEST', tx.description)

        subj = tx.inbox()
        self.assertIsNotNone(subj)

        status = tx.reliability(100)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        #tx.destroy();

        del tx

    def test_send(self):

        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        msg = TibrvMsg.create()
        msg.setStr('DATA', 'TEST')
        msg.sendSubject = 'TEST.A'

        status = tx.send(msg)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        msg.replySubject = 'TEST.ACK'
        status = tx.send(msg, 'TEST.B')
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        del msg
        del tx

    def test_request(self):
        tx = TibrvTx()
        status = tx.create(None, None, None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        msg = TibrvMsg.create()
        msg.setStr('DATA', 'TEST')
        msg.sendSubject = 'TEST.A'

        status, ack = tx.sendRequest(msg, 1.0)
        #self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))
        self.assertEqual(TIBRV_TIMEOUT, status, TibrvStatus.text(status))
        self.assertIsNone(ack)

        del msg
        del tx


if __name__ == "__main__":
    unittest.main(verbosity=2)
