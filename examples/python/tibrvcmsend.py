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


def sendMsgCallback(event: TibrvTimer, message: TibrvMsg, closure):

    global _running

    data = closure

    err = data['cmtx'].send(data['msg'])

    if err == TIBRV_OK:
        print('{}: {} in sending message {}'.format(
                 data['progname'], TibrvStatus.text(err), data['current_round']))
    else:
        print('{}: Error sending message -- {}'.format(data['progname'], TibrvStatus.text(err)))


    data['current_round'] += 1

    if data['rounds'] < data['current_round']:
        event.destroy()
        _running = False

    return

def cm_callback(event: TibrvListener, message: TibrvMsg, closure):
    adv_subj = message.sendSubject
    #err, msg_str = tibrvMsg_ConvertToString(message)

    if adv_subj is None:
        return

    if adv_subj.startswith('_RV.INFO.RVCM.DELIVERY.CONFIRM.'):
        subj = message.getStr('subject')
        cm_name = message.getStr('listener')
        cm_seq = message.getU64('seqno')

        print('CONFIRM  {} - {} #{}'.format(cm_name, subj, cm_seq))
        return

    if adv_subj.startswith('_RV.INFO.RVCM.DELIVERY.COMPLETE.'):
        subj = message.getStr('subject')
        cm_seq = message.getU64('seqno')

        print('COMPLETE {} #{}'.format(subj, cm_seq))
        return

    if adv_subj.startswith('_RV.ERROR.RVCM.DELIVERY.FAILED.'):
        subj = message.getStr('subject')
        cm_name = message.getStr('listener')
        cm_seq = message.getU64('seqno')

        print('FAILED  {} - {} #{}'.format(cm_name, subj, cm_seq))
        return

    if adv_subj.startswith('_RV.WARN.RVCM.DELIVERY.NO_RESPONSE.'):
        cm_name = message.getStr('listener')

        print('NO_RESPONSE  {}'.format(cm_name))
        return



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
        sys.exit(1);

    tx.description = progname

    msg = TibrvMsg.create()
    if msg is None:
        print('{}: Failed to create message: {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    print('Publishing: subject={} "{}"'.format(params['subject'], params['message']))\

    err = msg.setStr('DATA', params['message'])
    if err != TIBRV_OK:
        print('{} : Failed to add the input string to the message -- {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    msg.sendSubject = params['subject']
    if msg.error() is not None:
        print('{} : Failed to set the send subject in the message -- {}'.format(progname, msg.error().text()))
        sys.exit(1)


    # Set up a timer to send the message
    # pass data as closure
    data = {'progname': progname,
            'cmtx': cmtx,
            'msg': msg,
            'rounds': params['rounds'],
            'current_round': 1}

    timerId = TibrvTimer()
    err = timerId.create(TibrvQueue(), TibrvTimerCallback(sendMsgCallback), params['interval'], data)

    if err != TIBRV_OK:
        print('{}: Failed to start the timer -- {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    print('{}: Sending "{}" -> {} '.format(progname, params['message'], params['subject']))

    # Listen CM Advisory
    adv_subj = '_RV.*.RVCM.DELIVERY.*.' + params['subject']
    event = TibrvListener()
    err = event.create(TibrvQueue(), TibrvMsgCallback(cm_callback), tx, adv_subj, data)
    if err != TIBRV_OK:
        print('{} : Failed to listen RVCM advisory {} -- {}'.format(progname, adv_subj, TibrvStatus.text(err)))
        sys.exit(1)

    # dispatcher thread for timer and advisory
    disp = TibrvDispatcher()
    err = disp.create(TibrvQueue())
    if err != TIBRV_OK:
        print('{}: Failed to create dispatcher thread -- {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    # Set Signal Handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_proc)
    global _running

    while _running:
        time.sleep(0.5)

    timerId.destroy()
    disp.destroy()
    event.destroy()
    msg.destroy()
    cmtx.destroy()
    tx.destroy()

    Tibrv.close()

    sys.exit(0)


    return

if __name__ == "__main__":
    main(sys.argv)



