import os
import sys
import ctypes
from tibrv.msg import *
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
        msg = TibrvMsg()
        sz = str(msg)

        self.assertEqual("{}", sz)

        m = msg._msg

        del msg

        # tibrvMsg_Destroy() should be called at __del__
        status = tibrvMsg_Destroy(m)
        self.assertEqual(TIBRV_INVALID_MSG, status, TibrvStatus.text(status))

    def test_copy(self):
        msg = TibrvMsg()
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

        msg = TibrvMsg()
        m = msg.id()
        del msg

        # construct by invalid msg id, which just destroyed
        msg = TibrvMsg(m)
        msg.sendSubject = 'TEST'
        status = msg.error.code()

        self.assertEqual(TIBRV_INVALID_MSG, status, TibrvStatus.text(status))

        del msg

        # assign random msg id, ex: 12345
        # msg = TibrvMsg(12345)
        # DONT TRY IT, SEGMENT FAULT
        #

    def test_subject(self):
        msg = TibrvMsg()
        msg.sendSubject = 'TEST'
        self.assertEqual('TEST', msg.sendSubject)\

        msg.replySubject = 'TEST2'
        self.assertEqual('TEST2', msg.replySubject)\

        del msg

    def test_get(self):
        msg = TibrvMsg()

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

        msg.setStr('STR', 'TEST')
        self.assertEqual('TEST', msg.getStr('STR'))
        self.assertEqual('TEST', msg.get(tibrv_str, 'STR'))

        msg2 = TibrvMsg()
        msg2.set(tibrv_str, 'DATA', 'TEST')
        msg.setMsg('MSG', msg2)
        msgx = msg.getMsg('MSG')
        self.assertEqual(str(msg2), str(msgx))
        msgx = msg.get(TibrvMsg, 'MSG')
        self.assertEqual(str(msg2), str(msgx))


        del msg


    def test_datetime(self):

        status, msg = tibrvMsg_Create()
        assert status == TIBRV_OK, TibrvStatus.text(status)

        status = tibrvMsg_AddDateTime(msg, 'DT', None)
        assert status == TIBRV_OK, TibrvStatus.text(status)

        status = tibrvMsg_UpdateDateTime(msg, 'DT', None)
        assert status == TIBRV_OK, TibrvStatus.text(status)

        status, ret = tibrvMsg_GetDateTime(msg, 'DT')
        assert status == TIBRV_OK, TibrvStatus.text(status)
        assert ret is not None

        status = tibrvMsg_Destroy(msg)
        assert status == TIBRV_OK, TibrvStatus.text(status)

        msg = TibrvMsg()
        dt = TibrvMsg.now()

        status = msg.addDateTime('DT', dt)
        assert status == TIBRV_OK, TibrvStatus.text(status)

        status = msg.setDateTime('DT', dt)
        assert status == TIBRV_OK, TibrvStatus.text(status)

        ret = msg.getDateTime('DT')
        assert ret is not None
        # print(ret, dt)
        assert ret == dt, str(ret) + ' != ' + str(dt)

        del msg



def test_array():

    status = TIBRV_OK
    status, msg = tibrvMsg_Create()
    assert status == TIBRV_OK, TibrvStatus.text(status)

    # I8
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateI8Array(msg, 'I8', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetI8Array(msg, 'I8')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # U8
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateU8Array(msg, 'U8', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetU8Array(msg, 'U8')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # I16
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateI16Array(msg, 'I16', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetI16Array(msg, 'I16')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # U16
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateU16Array(msg, 'U16', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetU16Array(msg, 'U16')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # I32
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateI32Array(msg, 'I32', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetI32Array(msg, 'I32')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # U32
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateU32Array(msg, 'U32', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetU32Array(msg, 'U32')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # I64
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateI64Array(msg, 'I64', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetI32Array(msg, 'I64')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # U64
    data = [1,2,3,4,5]
    status = tibrvMsg_UpdateU64Array(msg, 'U64', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetU64Array(msg, 'U64')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret

    # F32
    data = [1.1,2.2,3.3,4.4,5.5]
    status = tibrvMsg_UpdateF32Array(msg, 'F32', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetF32Array(msg, 'F32')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    for x in range(len(data)):
        f = ctypes.c_float(data[x]).value   # convert to F32
        assert f == ret[x]

    # F64
    data = [1.1,2.2,3.3,4.4,5.5]
    status = tibrvMsg_UpdateF64Array(msg, 'F64', data)
    assert status == TIBRV_OK, TibrvStatus.text(status)

    status, ret = tibrvMsg_GetF64Array(msg, 'F64')
    assert status == TIBRV_OK, TibrvStatus.text(status)
    assert data == ret


if __name__ == "__main__":
    unittest.main(verbosity=2)
