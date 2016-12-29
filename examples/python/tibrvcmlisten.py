##
# tibrvcmlisten.py - generic CM Rendezvous subscriber
#
# rewrite TIBRV example: tibrvcmlisten.c
#
# LAST MODIFIED: V1.0 2016-12-26 ARIEN arien.chen@gmail.com
#
import sys
import signal
import getopt
import time
from pytibrv.Tibrv import *
from pytibrv.TibrvCm import *

# Module Variable
_running = True


def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')


def usage():
    print()
    print('tibrvcmlisten.py [options] subjects')
    print('')
    print('options:')
    print('     [--service service]         RVD Service')
    print('     [--network network]         RVD Network')
    print('     [--daemon daemon]           RVD Daemon')
    print('     [--ledger filename]         RVCM Ledger Name')
    print('     [--cmname cmname]           RVCM Name')
    print('     subjects1 [ subject2]       Multiple Subjects, delimited by space')
    print()
    sys.exit(1)


def get_params(argv):

    params = ['service=', 'network=', 'daemon=',
              'ledger=', 'cmnme=']
    try:
        opts, args = getopt.getopt(argv, '', params)

    except getopt.GetoptError:
        usage()

    service = network = daemon = ledger = None
    cmname = 'RVCMSUB'


    for opt, arg in opts:
        if opt == '--service':
            service = arg
        elif opt == '--network':
            network = arg
        elif opt == '--daemon':
            daemon = arg
        elif opt == '--ledger':
            ledger = arg
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
            'ledger': ledger,
            'subjects': subj}

def my_callback(event: TibrvCmListener, message: TibrvCmMsg, closure):
    # it would return None if failed
    subj_send = message.sendSubject
    subj_reply = message.replySubject
    cm_sender = message.sender()
    cm_seq = message.sequence()
    msg_str = str(message)

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

    err = Tibrv.open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, TibrvStatus.text(err)))
        sys.exit(1)

    tx = TibrvTx()
    err = tx.create(params['service'], params['network'], params['daemon'])
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    cmtx = TibrvCmTx()
    err = cmtx.create(tx, params['cmname'], True, params['ledger'], False, None)

    if err != TIBRV_OK:
        print('{} : Failed to initialize CM transport -- {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    tx.description = progname
    que = TibrvQueue()
    disp = TibrvDispatcher()
    err = disp.create(que)
    if err != TIBRV_OK:
        print('{} : Failed to create dispatcher thread -- {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    for subj in params['subjects']:
        event = TibrvCmListener()
        err = event.create(que, TibrvCmMsgCallback(my_callback), cmtx, subj, None)

        if err != TIBRV_OK:
            print('{}: Error {} listening to "{}"'.format(progname, TibrvStatus.text(err), subj))
            sys.exit(2)

        print('LISTEN FOR "{}"'.format(subj))


    # Set Signal Handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_proc)
    global _running

    while _running:
        time.sleep(0.5)

    disp.destroy()
    cmtx.destroy()
    tx.destroy()

    Tibrv.close()

    sys.exit(0)

    return

if __name__ == "__main__":
    main(sys.argv)



