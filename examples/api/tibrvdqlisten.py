##
# tibrvdqlisten.py - generic DQ Rendezvous subscriber
#
# rewrite TIBRV example: tibrvcmlisten.c
#
# LAST MODIFIED: V1.0 2016-12-26 ARIEN arien.chen@gmail.com
#
import sys
import signal
import getopt
import time
from pytibrv.api import *
from pytibrv.status import *
from pytibrv.msg import *
from pytibrv.tport import *
from pytibrv.queue import *
from pytibrv.disp import *
from pytibrv.cm import *
from pytibrv.dq import *

# Module Variable
_running = True


def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')


def usage():
    print()
    print('tibrvdqlisten.py [options] subjects')
    print('')
    print('options:')
    print('     [--service service]         RVD Service')
    print('     [--network network]         RVD Network')
    print('     [--daemon daemon]           RVD Daemon')
    print('     [--cmname cmname]           RVCM Name')
    print('     subjects1 [ subject2]       Multiple Subjects, delimited by space')
    print()
    sys.exit(1)


def get_params(argv):

    params = ['service=', 'network=', 'daemon=', 'cmnme=']
    try:
        opts, args = getopt.getopt(argv, '', params)

    except getopt.GetoptError:
        usage()

    service = network = daemon = None
    cmname = 'RVCMSUB'


    for opt, arg in opts:
        if opt == '--service':
            service = arg
        elif opt == '--network':
            network = arg
        elif opt == '--daemon':
            daemon = arg
        elif opt == '--cmname':
            cmname = arg
        else:
            usage()

    if len(args) == 0:
        usage()

    subj = []
    subj.extend(args)

    return {'service': service,
            'network': network,
            'daemon': daemon,
            'cmname': cmname,
            'subjects': subj}

def my_callback(event: tibrvcmEvent, message: tibrvMsg, closure):
    # it would return None if failed
    err, subj_send = tibrvMsg_GetSendSubject(message)
    err, subj_reply = tibrvMsg_GetReplySubject(message)
    err, cm_sender = tibrvMsg_GetCMSender(message)
    err, cm_seq = tibrvMsg_GetCMSequence(message)
    err, msg_str = tibrvMsg_ConvertToString(message)


    if cm_sender is None:
        # Reliable
        print('subject={}, reply={}, messages={}'.format(subj_send, subj_reply, msg_str))
    else:
        # Certified Message
        print('certified sender={}, sequence={}, subject={}, reply={}, messages={}'.format(
              cm_sender, cm_seq, subj_send, subj_reply, msg_str))


# MAIN PROGRAM
def main(argv):

    progname = argv[0]

    params = get_params(argv[1:])

    err = tibrv_Open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err, tx = tibrvTransport_Create(params['service'], params['network'], params['daemon'])
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err, cmtx = tibrvcmTransport_CreateDistributedQueue(tx, params['cmname'])

    if err != TIBRV_OK:
        print('{} : Failed to create distributed queue member -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    tibrvTransport_SetDescription(tx, progname)

    err, disp = tibrvDispatcher_Create(TIBRV_DEFAULT_QUEUE)
    if err != TIBRV_OK:
        print('{} : Failed to create dispatcher thread -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    for subj in params['subjects']:
        err, event = tibrvcmEvent_CreateListener(TIBRV_DEFAULT_QUEUE, my_callback, cmtx, subj, None)

        if err != TIBRV_OK:
            print('{}: Error {} listening to "{}"'.format(progname, tibrvStatus_GetText(err), subj))
            sys.exit(2)

        print('LISTEN FOR "{}"'.format(subj))


    # Set Signal Handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_proc)
    global _running

    while _running:
        time.sleep(0.5)

    tibrvDispatcher_Destroy(disp)
    tibrvcmTransport_Destroy(cmtx)
    tibrvTransport_Destroy(tx)

    tibrv_Close()

    sys.exit(0)

    return

if __name__ == "__main__":
    main(sys.argv)



