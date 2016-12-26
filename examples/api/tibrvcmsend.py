##
# tibrvcmsend.py - sample CM Rendezvous message publisher
#
# rewrite TIBRV example: tibrvcmsend.c
#
# LAST MODIFIED: V1.0 2016-12-26 ARIEN arien.chen@gmail.com
#
import sys
import signal
import time
import getopt
from pytibrv.api import *
from pytibrv.status import *
from pytibrv.msg import *
from pytibrv.tport import *
from pytibrv.events import *
from pytibrv.queue import *
from pytibrv.disp import *
from pytibrv.cm import *

# Module Variable
_running = True


def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')


def usage():
    print()
    print('tibrvcmsend.py [options] subject message')
    print('')
    print('options:')
    print('     [--service service]         RVD Service')
    print('     [--network network]         RVD Network')
    print('     [--daemon daemon]           RVD Daemon')
    print('     [--ledger filename]         RVCM Ledger Name')
    print('     [--cmname cmname]           RVCM Name')
    print('     [--interval num]            RVCM ')
    print('     [--rounds num]              RVCM ')
    print('     subject                     Message Subject')
    print('     message                     Message Text')
    print()
    sys.exit(1)


def get_params(argv):

    params = ['service=', 'network=', 'daemon=',
              'ledger=', 'cmnme=', 'interval=', 'rounds=']
    try:
        opts, args = getopt.getopt(argv, '', params)

    except getopt.GetoptError:
        usage()

    service = network = daemon = ledger = None
    cmname = 'RVCMPUB'
    int_sec = 1.0
    rounds = 10


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
        elif opt == '--interval':
            int_sec = float(arg)
        elif opt == '--rounds':
            rounds = int(arg)
        else:
            usage()

    if len(args) != 2:
        usage()

    return {'service': service,
            'network': network,
            'daemon': daemon,
            'cmname': cmname,
            'ledger': ledger,
            'interval': int_sec,
            'rounds': rounds,
            'subject': args[0],
            'message': args[1]}


def sendMsgCallback(event: tibrvEvent, message: tibrvMsg, closure):

    global _running

    data = tibrvClosure(closure)


    err = tibrvcmTransport_Send(data['cmtx'], data['msg'])

    if err == TIBRV_OK:
        print('{}: {} in sending message {}'.format(
                 data['progname'], tibrvStatus_GetText(err), data['current_round']))
    else:
        print('{}: Error sending message -- {}'.format(data['progname'], tibrvStatus_GetText(err)))


    data['current_round'] += 1

    if data['rounds'] < data['current_round']:
        tibrvEvent_Destroy(event)
        _running = False

    return

def cm_callback(event: tibrvEvent, message: tibrvMsg, closure):
    err, adv_subj = tibrvMsg_GetSendSubject(message)
    #err, msg_str = tibrvMsg_ConvertToString(message)

    if adv_subj is None:
        return

    if adv_subj.startswith('_RV.INFO.RVCM.DELIVERY.CONFIRM.'):
        err, subj = tibrvMsg_GetString(message, 'subject')
        err, cm_name = tibrvMsg_GetString(message, 'listener')
        err, cm_seq = tibrvMsg_GetU64(message, 'seqno')

        print('CONFIRM  {} - {} #{}'.format(cm_name, subj, cm_seq))
        return

    if adv_subj.startswith('_RV.INFO.RVCM.DELIVERY.COMPLETE.'):
        err, subj = tibrvMsg_GetString(message, 'subject')
        err, cm_seq = tibrvMsg_GetU64(message, 'seqno')

        print('COMPLETE {} #{}'.format(subj, cm_seq))
        return

    if adv_subj.startswith('_RV.ERROR.RVCM.DELIVERY.FAILED.'):
        err, subj = tibrvMsg_GetString(message, 'subject')
        err, cm_name = tibrvMsg_GetString(message, 'listener')
        err, cm_seq = tibrvMsg_GetU64(message, 'seqno')

        print('FAILED  {} - {} #{}'.format(cm_name, subj, cm_seq))
        return

    if adv_subj.startswith('_RV.WARN.RVCM.DELIVERY.NO_RESPONSE.'):
        err, cm_name = tibrvMsg_GetString(message, 'listener')

        print('NO_RESPONSE  {}'.format(cm_name))
        return



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

    err, cmtx = tibrvcmTransport_Create(tx, params['cmname'], True, params['ledger'], False, None)

    if err != TIBRV_OK:
        print('{} : Failed to initialize CM transport -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1);

    tibrvTransport_SetDescription(tx, progname)

    err, msg = tibrvMsg_Create()
    if err != TIBRV_OK:
        print('{}: Failed to create message: {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    print('Publishing: subject={} "{}"'.format(params['subject'], params['message']))\

    err = tibrvMsg_UpdateString(msg, 'DATA', params['message'])
    if err != TIBRV_OK:
        print('{} : Failed to add the input string to the message -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err = tibrvMsg_SetSendSubject(msg, params['subject'])
    if err != TIBRV_OK:
        print('{} : Failed to set the send subject in the message -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)


    # Set up a timer to send the message
    # pass data as closure
    data = {'progname': progname,
            'cmtx': cmtx,
            'msg': msg,
            'rounds': params['rounds'],
            'current_round': 1}

    err, timerId = tibrvEvent_CreateTimer(TIBRV_DEFAULT_QUEUE, sendMsgCallback, params['interval'], data)

    if err != TIBRV_OK:
        print('{}: Failed to start the timer -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    print('{}: Sending "{}" -> {} '.format(progname, params['message'], params['subject']))

    # Listen CM Advisory
    adv_subj = '_RV.*.RVCM.DELIVERY.*.' + params['subject']
    err, event = tibrvEvent_CreateListener(TIBRV_DEFAULT_QUEUE, cm_callback, tx, adv_subj, data)
    if err != TIBRV_OK:
        print('{} : Failed to listen RVCM advisory {} -- {}'.format(progname, adv_subj, tibrvStatus_GetText(err)))
        sys.exit(1)

    # dispatcher thread for timer and advisory
    err, disp = tibrvDispatcher_Create(TIBRV_DEFAULT_QUEUE)
    if err != TIBRV_OK:
        print('{}: Failed to create dispatcher thread -- {}'.format(progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    # Set Signal Handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_proc)
    global _running

    while _running:
        time.sleep(0.5)

    tibrvEvent_Destroy(timerId)
    tibrvDispatcher_Destroy(disp)
    tibrvEvent_Destroy(event)
    tibrvMsg_Destroy(msg)
    tibrvcmTransport_Destroy(cmtx)
    tibrvTransport_Destroy(tx)

    tibrv_Close()

    sys.exit(0)


    return

if __name__ == "__main__":
    main(sys.argv)



