
import ctypes

from pytibrv.api import *
from pytibrv.status import *
from pytibrv.msg import *
import unittest

class MsgTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        status = tibrv_Open()
        assert TIBRV_OK == status, tibrvStatus_GetText(status)

    @classmethod
    def tearDownClass(cls):
        tibrv_Close()

    def test_new(self):

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvMsg_ConvertToString(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        self.assertEqual("{}", sz)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def test_copy(self):

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateString(msg, 'A', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, msg2 = tibrvMsg_CreateCopy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvMsg_ConvertToString(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz2 = tibrvMsg_ConvertToString(msg2)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        self.assertEqual(sz, sz2)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(msg2)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

    def test_invalid(self):

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # construct by invalid msg id, which just destroyed
        status = tibrvMsg_SetSendSubject(msg, 'TEST')
        self.assertEqual(TIBRV_INVALID_MSG, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_INVALID_MSG, status, tibrvStatus_GetText(status))


        # assign random msg id, ex: 12345
        # DONT TRY IT, SEGMENT FAULT
        #
        #status = tibrvMsg_Destroy(12345)

    def test_subject(self):
        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_SetSendSubject(msg, 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, subj = tibrvMsg_GetSendSubject(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        self.assertEqual('TEST', subj)

        status = tibrvMsg_SetReplySubject(msg, 'TEST2')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, subj = tibrvMsg_GetReplySubject(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('TEST2', subj)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


    def test_get(self):
        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateI8(msg, 'I8', 0xFFFF)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetI8(msg, 'I8')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(-1, n)

        status = tibrvMsg_UpdateU8(msg, 'U8', 0xFFFF)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetU8(msg, 'U8')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(0x00FF, n)

        status = tibrvMsg_UpdateI16(msg, 'I16', 0xFFFFFFFE)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetI16(msg, 'I16')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(-2, n)

        status = tibrvMsg_UpdateU16(msg, 'U16', 0xFFFFFFFE)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetU16(msg, 'U16')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(0x00FFFE, n)

        status = tibrvMsg_UpdateI32(msg, 'I32', 0x0000FFFFFFFFFFFD)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetI32(msg, 'I32')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(-3, n)

        status = tibrvMsg_UpdateU32(msg, 'U32', 0x0000FFFFFFFFFFFD)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetU32(msg, 'U32')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(0x00FFFFFFFD, n)

        status = tibrvMsg_UpdateI64(msg, 'I64', 0xfffffffffffffffc)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetI64(msg, 'I64')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(-4, n)

        status = tibrvMsg_UpdateU64(msg, 'U64', 0xFFFFFFFFFFFFFFFC)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, n = tibrvMsg_GetU64(msg, 'U64')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(0x00FFFFFFFFFFFFFFFC, n)

        status = tibrvMsg_UpdateString(msg, 'STR', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status, sz = tibrvMsg_GetString(msg, 'STR')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual('TEST', sz)

        status, msg2 = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        status = tibrvMsg_UpdateString(msg2, 'DATA', 'TEST')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateMsg(msg, 'MSG', msg2)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, mm = tibrvMsg_GetMsg(msg, 'MSG')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz = tibrvMsg_ConvertToString(msg2)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, sz2 = tibrvMsg_ConvertToString(mm)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        self.assertEqual(sz, sz2)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_Destroy(msg2)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


    def test_datetime(self):

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_AddDateTime(msg, 'DT', None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status = tibrvMsg_UpdateDateTime(msg, 'DT', None)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetDateTime(msg, 'DT')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert ret is not None

        status, dt = tibrvMsg_GetCurrentTime()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertTrue(type(dt) is tibrvMsgDateTime)
        print(dt)

        status = tibrvMsg_UpdateDateTime(msg, 'DT', dt)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, dt2 = tibrvMsg_GetDateTime(msg, 'DT')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertTrue(type(dt2) is tibrvMsgDateTime)
        self.assertEqual(dt, dt2)

        dt3 = tibrvMsgDateTime()
        status = tibrvMsg_UpdateDateTime(msg, 'DT3', dt3)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, dt4 = tibrvMsg_GetDateTime(msg, 'DT3')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        self.assertEqual(dt3, dt4)

        status = tibrvMsg_Destroy(msg)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))


    def test_array(self):

        status, msg = tibrvMsg_Create()
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        # I8
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateI8Array(msg, 'I8', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetI8Array(msg, 'I8')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # U8
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateU8Array(msg, 'U8', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetU8Array(msg, 'U8')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # I16
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateI16Array(msg, 'I16', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetI16Array(msg, 'I16')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # U16
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateU16Array(msg, 'U16', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetU16Array(msg, 'U16')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # I32
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateI32Array(msg, 'I32', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetI32Array(msg, 'I32')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # U32
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateU32Array(msg, 'U32', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetU32Array(msg, 'U32')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # I64
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateI64Array(msg, 'I64', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetI32Array(msg, 'I64')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # U64
        data = [1,2,3,4,5]
        status = tibrvMsg_UpdateU64Array(msg, 'U64', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetU64Array(msg, 'U64')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret

        # F32
        data = [1.1,2.2,3.3,4.4,5.5]
        status = tibrvMsg_UpdateF32Array(msg, 'F32', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetF32Array(msg, 'F32')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        for x in range(len(data)):
            f = ctypes.c_float(data[x]).value   # convert to F32
            assert f == ret[x]

        # F64
        data = [1.1,2.2,3.3,4.4,5.5]
        status = tibrvMsg_UpdateF64Array(msg, 'F64', data)
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))

        status, ret = tibrvMsg_GetF64Array(msg, 'F64')
        self.assertEqual(TIBRV_OK, status, tibrvStatus_GetText(status))
        assert data == ret


if __name__ == "__main__":
    unittest.main(verbosity=2)
