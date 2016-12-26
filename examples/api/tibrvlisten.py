##
# tibrvlisten.py
#   rewrite TIBRV example: tibrvlisten.c
#
# LAST MODIFIED: V1.0 2016-12-22 ARIEN arien.chen@gmail.com
#
import sys, signal
import getopt
from pytibrv.api import *
from pytibrv.status import *
from pytibrv.events import *
from pytibrv.msg import *
from pytibrv.tport import *
from pytibrv.queue import *

# Module Variables
_running = True         # set to False when Ctrl-C

def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')

def usage():
    print('TIBRV Listener : tibrvlisten.py')
    print('')
    print('tibrvlisten.py [--service service] [--network network]')
    print('               [--daemon daemon] <subject> ')
    print()
    sys.exit(1)


def get_params(argv):

    try:
        opts, args = getopt.getopt(argv, '', ['service=', 'network=', 'daemon='])

    except getopt.GetoptError:
        usage()

    service = None
    network = None
    daemon = None

    for opt, arg in opts:
        if opt == '--service':
            service = arg
        elif opt == '--network':
            network = arg
        elif opt == '--daemon':
            daemon = arg
        else:
            usage()

    if len(args) != 1:
        usage()

    return service, network, daemon, args[0]

def my_callback(event, msg, closure):

    err, send_subject = tibrvMsg_GetSendSubject(msg)

    err, reply_subject = tibrvMsg_GetReplySubject(msg)

    err, theString = tibrvMsg_ConvertToString(msg)

    err, localTime, gmtTime = tibrvMsg_GetCurrentTimeString()

    if reply_subject is not None:
        print("{} ({}): subject={}, reply={}, message={}".format(
               localTime, gmtTime, send_subject, reply_subject, theString));
    else:
        print("{} ({}): subject={}, message={}".format(
               localTime, gmtTime, send_subject, theString));


# MAIN PROGRAM
def main(argv):

    progname = argv[0]

    service, network, daemon, subj = get_params(argv[1:])

    err = tibrv_Open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err, tx = tibrvTransport_Create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    tibrvTransport_SetDescription(tx, progname)

    print("tibrvlisten: Listening to subject {}".format(subj))

    err, lst = tibrvEvent_CreateListener(TIBRV_DEFAULT_QUEUE, my_callback, tx, subj, None)
    if err != TIBRV_OK:
        print('{}: Error {} listening to {}'.format('', progname, tibrvStatus_GetText(err), subj))
        sys.exit(2)

    # Set Signal Handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_proc)
    global _running

    while _running:
        tibrvQueue_TimedDispatch(TIBRV_DEFAULT_QUEUE, 0.5)

    tibrvEvent_Destroy(lst)
    tibrvTransport_Destroy(tx)
    tibrv_Close()

    sys.exit(0)

    return

if __name__ == "__main__":
    main(sys.argv)



