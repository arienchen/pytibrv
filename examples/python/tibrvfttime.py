##
# tibrvfttime.py - example timestamp message program using
#                  TIBRV Fault Tolerant API
#
# rewrite TIBRV example: tibrvfttime.c
#
# LAST MODIFIED: V1.0 2016-12-26 ARIEN arien.chen@gmail.com
#
import sys
import signal
import getopt
from datetime import datetime
from pytibrv.Tibrv import *
from pytibrv.TibrvFt import *

# Module Variables
_running = True

def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')

def usage():
    print()
    print('tibrvfttime.py [options]')
    print('')
    print('options:')
    print('    [--service service]          RVD Service')
    print('    [--network network]          RVD Network')
    print('    [--daemon daemon]            RVD Daemon')
    print('    [--ft-service ft-svc]        RVFT Service')
    print('    [--ft-network ft-net]        RVFT Network')
    print('    [--ft-daemon  ft-daemon]     RVFT Daemon')
    print('    [--ft-weight weight]         RVFT Weight, default 50')
    print()
    sys.exit(1)


def get_params(argv):

    params = ['service=', 'network=', 'daemon=',
              'ft-service=', 'ft-network=', 'ft-daemon=', 'ft-weight='
             ]
    try:
        opts, args = getopt.getopt(argv, '', params)

    except getopt.GetoptError:
        usage()

    service = None
    network = None
    daemon = None
    ft_svc = None
    ft_net = None
    ft_daemon = None
    ft_weight = 50

    for opt, arg in opts:
        if opt == '--service':
            service = arg
        elif opt == '--network':
            network = arg
        elif opt == '--daemon':
            daemon = arg
        elif opt == '--ft-service':
            ft_svc = arg
        elif opt == '--ft-network':
            ft_net = arg
        elif opt == '--ft-daemon':
            ft_daemon = arg
        elif opt == '--ft-weight':
            ft_weight = arg
        else:
            usage()

    if len(args) != 0:
        usage()

    return service, network, daemon, ft_svc, ft_net, ft_daemon, ft_weight

class App:
    def __init__(self):
        self.tx = None
        self.timerId = None
        self.ft_tx = None
        self.ft_mem = None
        self.active = False
        self.subj = ''
        self.progname = ''

def advCB(event: TibrvEvent, message: TibrvMsg, closure):

    print('#### RVFT ADVISORY: {}'.format(message.sendSubject))
    print('Advisory message is: {}'.format(str(message)))

    return

def pubTime(event: TibrvEvent, message: TibrvMsg, closure):

    ap = closure

    # do nothing if not active
    if not ap.active:
        return

    tt = TibrvMsgDateTime.now()

    msg = TibrvMsg()

    err = msg.addDateTime('DATA', tt)
    if err != TIBRV_OK:
        print('Error generating timestamp data: {}'.format(TibrvStatus.text(err)))
        tibrvMsg_Destroy(msg)
        return

    err = ap.tx.send(msg, ap.subj)

    if err != TIBRV_OK:
        print('Error publishing timestamp message: {}'.format(TibrvStatus.text(err)))

    print(datetime.now(), '>', str(msg))

    msg.destroy()


def processInstruction(id: TibrvFtMember, groupName: str, action: int, closure):

    ap = closure

    if action == TIBRVFT_PREPARE_TO_ACTIVATE:
        print('####### PREPARE TO ACTIVATE: {}'.format(groupName))

    elif action == TIBRVFT_ACTIVATE:
        print('####### ACTIVATE: {}'.format(groupName))
        ap.active = True

    elif action == TIBRVFT_DEACTIVATE:
        print('####### DEACTIVATE: {}'.format(groupName))
        ap.active = False

    return


# MAIN PROGRAM
def main(argv):


    service, network, daemon, ft_svc, ft_net, ft_daemon, ft_weight = get_params(argv[1:])
    timeInt = 10.0
    groupName = 'TIBRVFT_TIME_EXAMPLE'
    numactive = 1
    hbInterval = 1.5
    prepareInterval = 0
    activateInterval = 4.8

    ap = App()
    ap.progname = argv[0]
    ap.subj = 'TIBRVFT_TIME'

    err = Tibrv.open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', ap.progname, TibrvStatus.text(err)))
        sys.exit(1)

    ap.tx = TibrvTx()
    err = ap.tx.create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format('', ap.progname, TibrvStatus.text(err)))
        sys.exit(1)


    print('Active group member will publish time every {} seconds.'.format(timeInt))
    print('Subject is {}'.format(ap.subj))
    print('Inactive will not publish time')

    que = TibrvQueue()
    ap.timerId = TibrvTimer()
    err = ap.timerId.create(que, TibrvTimerCallback(pubTime), timeInt, ap)

    if err != TIBRV_OK:
        print('Error adding repeating timer: -- {}'.foramt(TibrvStatus.text(err)))
        sys.exit(3)

    # create RVFT
    ap.ft_tx = TibrvTx()
    err = ap.ft_tx.create(ft_svc, ft_net, ft_daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize fault tolerant transport -- {}'.format(
                    ap.progname, TibrvStatus.text(err)))
        sys.exit(3)

    # join RVFT
    ap.ft_mem = TibrvFtMember()
    err = ap.ft_mem.create(que, TibrvFtMemberCallback(processInstruction), ap.ft_tx,
                        groupName, ft_weight, numactive,
                        hbInterval, prepareInterval, activateInterval,
                        ap)

    if err != TIBRV_OK:
        print('{} : Failed to join group - {}'.format(ap.progname,TibrvStatus.text(err)))
        sys.exit(4)

    # Subscribe to RVFT advisories
    advId = TibrvListener()
    err = advId.create(que, TibrvMsgCallback(advCB), ap.ft_tx,
                       '_RV.*.RVFT.*.' + groupName,
                       ap)

    if err != TIBRV_OK:
        print('{} : Failed to start listening to advisories - {}'.format(
                    ap.progname, TibrvStatus.text(err)))
        sys.exit(5)

    # Set Signal Handler for Ctrl-C
    global _running
    signal.signal(signal.SIGINT, signal_proc)

    while _running:
        que.timedDispatch(0.5)

    advId.destroy()
    ap.timerId.destroy()
    ap.ft_mem.destroy()

    Tibrv.close()

    return

if __name__ == "__main__":
    main(sys.argv)



