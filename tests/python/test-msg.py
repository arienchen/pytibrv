from pytibrv.Tibrv import *
from ctypes import c_float
import unittest

class MsgTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = Tibrv.open()
        assert TIBRV_OK == status, TibrvStatus.text(status)

    @classmethod
    def tearDownClass(cls):
        status = Tibrv.close()

    def test_new(self):
        # Default Constructor
        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        sz = str(msg)

        self.assertEqual("{}", sz)

        m = msg.id()

        status = msg.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))
        self.assertEqual(0, msg.id())

        # destroy again
        status = tibrvMsg_Destroy(m)
        self.assertEqual(TIBRV_INVALID_MSG, status, TibrvStatus.text(status))

    def test_copy(self):
        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        msg.setStr('A', 'TEST')
        m = msg.id()
        msg2 = msg.copy()
        # msg content must be same
        self.assertEqual(str(msg), str(msg2))

        # enable exception
        TibrvStatus.exception(True)
        try:
            del msg
            del msg2
        except:
            self.fail('MUST NO EXCEPTION')

        # disable exception
        TibrvStatus.exception(False)

    def test_invalid(self):

        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        m = msg.id()
        status = msg.destroy()
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        # construct by invalid msg id, which just destroyed
        msg = TibrvMsg(m)
        msg.sendSubject = 'TEST'
        status = msg.error().code()
        self.assertEqual(TIBRV_INVALID_MSG, status, TibrvStatus.text(status))

        status = msg.destroy()
        self.assertEqual(TIBRV_INVALID_MSG, status, TibrvStatus.text(status))


        # assign random msg id, ex: 12345
        # msg = TibrvMsg(12345)
        # DONT TRY IT, SEGMENT FAULT
        #

    def test_subject(self):
        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        msg.sendSubject = 'TEST'
        self.assertEqual('TEST', msg.sendSubject)\

        msg.replySubject = 'TEST2'
        self.assertEqual('TEST2', msg.replySubject)\

        msg.destroy()

    def test_get(self):
        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        msg.setI8('I8', 0xFFFF)
        self.assertEqual(-1, msg.getI8('I8'))
        self.assertEqual(-1, msg.get(tibrv_i8, 'I8'))

        msg.setU8('U8', 0xFFFF)
        self.assertEqual(0xFF, msg.getU8('U8'))
        self.assertEqual(0xFF, msg.get(tibrv_u8, 'U8'))

        msg.setI16('I16', 0xFFFFFFFE)
        self.assertEqual(-2, msg.getI16('I16'))
        self.assertEqual(-2, msg.get(tibrv_i16, 'I16'))

        msg.setU16('U16', 0xFFFFFFFE)
        self.assertEqual(0xFFFE, msg.getU16('U16'))
        self.assertEqual(0xFFFE, msg.get(tibrv_u16, 'U16'))

        msg.setI32('I32', 0x0000FFFFFFFFFFFD)
        self.assertEqual(-3, msg.getI32('I32'))
        self.assertEqual(-3, msg.get(tibrv_i32, 'I32'))

        msg.setU32('U32', 0x0000FFFFFFFFFFFD)
        self.assertEqual(0xFFFFFFFD, msg.getU32('U32'))
        self.assertEqual(0xFFFFFFFD, msg.get(tibrv_u32, 'U32'))

        msg.setI64('I64', 0xfffffffffffffffc)
        self.assertEqual(-4, msg.getI64('I64'))
        self.assertEqual(-4, msg.get(tibrv_i64, 'I64'))

        msg.setU64('U64', 0xFFFFFFFFFFFFFFFC)
        self.assertEqual(0xFFFFFFFFFFFFFFFC, msg.getU64('U64'))
        self.assertEqual(0xFFFFFFFFFFFFFFFC, msg.get(tibrv_u64, 'U64'))

        msg.setF32('F32', 1.1)
        self.assertEqual(c_float(1.1).value, msg.getF32('F32'))
        self.assertEqual(c_float(1.1).value, msg.get(tibrv_f32, 'F32'))

        msg.setF64('F64', 1.2)
        self.assertEqual(1.2, msg.getF64('F64'))
        self.assertEqual(1.2, msg.get(tibrv_f64, 'F64'))

        msg.setStr('STR', 'TEST')
        self.assertEqual('TEST', msg.getStr('STR'))
        self.assertEqual('TEST', msg.get(tibrv_str, 'STR'))

        msg2 = TibrvMsg.create()
        msg2.set(tibrv_str, 'DATA', 'TEST')
        msg.setMsg('MSG', msg2)
        msgx = msg.getMsg('MSG')
        self.assertEqual(str(msg2), str(msgx))
        msgx = msg.get(TibrvMsg, 'MSG')
        self.assertEqual(str(msg2), str(msgx))

        msg.destroy()
        msg2.destroy()
        msgx.destroy()


    def test_datetime(self):
        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        status = msg.addDateTime('DT', None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        status = msg.setDateTime('DT', None)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.getDateTime('DT')
        self.assertIsNotNone(ret)

        ret = msg.getDateTime('NOW')
        self.assertIsNone(ret)

        dt = TibrvMsg.now()
        status = msg.setDateTime('NOW', dt)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.getDateTime('NOW')
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))
        self.assertIsNotNone(ret)
        self.assertEqual(dt, ret)

        msg.destroy()


    def test_array(self):

        msg = TibrvMsg.create()
        self.assertIsNotNone(msg)

        # I8
        data = [1,2,3,4,5]
        status = msg.setI8('I8', data)
        self.assertEqual(TIBRV_OK, status , TibrvStatus.text(status))

        ret = msg.listI8('I8')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_i8, 'I8')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # U8
        data = [1,2,3,4,5]
        status = msg.setU8('U8', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listU8('U8')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_u8, 'U8')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # I16
        data = [1,2,3,4,5]
        status = msg.setI16('I16', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listI16('I16')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_i16, 'I16')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # U16
        data = [1,2,3,4,5]
        status = msg.setU16('U16', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listU16('U16')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_u16, 'U16')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # I32
        data = [1,2,3,4,5]
        status = msg.setI32('I32', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listI32('I32')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_i32, 'I32')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # U32
        data = [1,2,3,4,5]
        status = msg.setU32('U32', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listU32('U32')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_u32, 'U32')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # I64
        data = [1,2,3,4,5]
        status = msg.setI64('I64', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listI64('I64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_i64, 'I64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # U64
        data = [1,2,3,4,5]
        status = msg.setU64('U64', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listU64('U64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_u64, 'U64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # F32
        data = [1.1,2.2,3.3,4.4,5.5]
        status = msg.setF32('F32', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listF32('F32')
        self.assertIsNotNone(ret)
        #self.assertEqual(data, ret)
        for x in range(len(data)):
            f = c_float(data[x]).value   # convert to F32
            self.assertEqual(f, ret[x])

        ret = msg.list(tibrv_f32, 'F32')
        self.assertIsNotNone(ret)
        #self.assertEqual(data, ret)
        for x in range(len(data)):
            f = c_float(data[x]).value   # convert to F32
            self.assertEqual(f, ret[x])

        # F64
        data = [1.1,2.2,3.3,4.4,5.5]
        status = msg.setF64('F64', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listF64('F64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_f64, 'F64')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # str
        data = ['1', '2', '3', 'A', 'B']
        status = msg.setStr('STR', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listStr('STR')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        ret = msg.list(tibrv_str, 'STR')
        self.assertIsNotNone(ret)
        self.assertEqual(data, ret)

        # msg
        msg1 = TibrvMsg.create()
        msg1.setStr('STR', 'MSG 1')

        msg2 = TibrvMsg.create()
        msg2.setStr('STR', 'MSG 2')

        msg3 = TibrvMsg.create()
        msg3.setStr('STR', 'MSG 3')

        data = [msg1, msg2, msg3]
        status = msg.setMsg('MSG', data)
        self.assertEqual(TIBRV_OK, status, TibrvStatus.text(status))

        ret = msg.listMsg('MSG')
        self.assertIsNotNone(ret)
        for x in range(len(data)):
            self.assertEqual(str(data[x]), str(ret[x]))

        ret = msg.list(TibrvMsg, 'MSG')
        self.assertIsNotNone(ret)
        for x in range(len(data)):
            self.assertEqual(str(data[x]), str(ret[x]))

        msg.destroy()
        msg1.destroy()
        msg2.destroy()
        msg3.destroy()

if __name__ == "__main__":
    unittest.main(verbosity=2)
