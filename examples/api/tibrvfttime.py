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
from pytibrv.api import *
from pytibrv.status import *
from pytibrv.msg import *
from pytibrv.queue import *
from pytibrv.events import *
from pytibrv.tport import *
from pytibrv.ft import *

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
        self.tx = 0
        self.timerId = 0
        self.ft_tx = 0
        self.ft_mem = 0
        self.active = False
        self.subj = ''
        self.progname = ''

def advCB(event: tibrvEvent, message: tibrvMsg, closure):

    err, name = tibrvMsg_GetSendSubject(message)

    err, sz = tibrvMsg_ConvertToString(message)

    print('#### RVFT ADVISORY: {}'.format(name))
    print('Advisory message is: {}'.format(sz))

    return



def pubTime(event: tibrvEvent, message: tibrvMsg, closure):

    ap = tibrvClosure(closure)

    # do nothing if not active
    if not ap.active:
        return

    tt = tibrvMsgDateTime.now()

    err, msg = tibrvMsg_Create()

    if err != TIBRV_OK:
        print('{}: Failed to create message -- {}'.format(ap.progname, tibrvStatus_GetText(err)))
        return

    err = tibrvMsg_AddDateTime(msg, 'DATA', tt)
    if err != TIBRV_OK:
        print('Error generating timestamp data: {}'.format(tibrvStatus_GetText(err)))
        tibrvMsg_Destroy(msg)
        return

    err = tibrvMsg_SetSendSubject(msg, ap.subj)
    if err != TIBRV_OK:
        print('Error setting send subject: {}'.format(tibrvStatus_GetText(err)))
        tibrvMsg_Destroy(msg)
        return

    err = tibrvTransport_Send(ap.tx, msg);
    if err != TIBRV_OK:
        print('Error publishing timestamp message: {}'.format(tibrvStatus_GetText(err)))

    err, sz = tibrvMsg_ConvertToString(msg)
    print(datetime.now(), '>', sz)

    tibrvMsg_Destroy(msg)


def processInstruction(id: tibrvftMember, ftGroupName: bytes, action: tibrvftAction, closure):

    ap = tibrvClosure(closure)
    grp = ftGroupName.decode()

    if action == TIBRVFT_PREPARE_TO_ACTIVATE:
        print('####### PREPARE TO ACTIVATE: {}'.format(grp))

    elif action == TIBRVFT_ACTIVATE:
        print('####### ACTIVATE: {}'.format(grp))
        ap.active = True

    elif action == TIBRVFT_DEACTIVATE:
        print('####### DEACTIVATE: {}'.format(grp))
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

    err = tibrv_Open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', ap.progname, tibrvStatus_GetText(err)))
        sys.exit(1)


    err, ap.tx = tibrvTransport_Create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format('', ap.progname, tibrvStatus_GetText(err)))
        sys.exit(1)


    print('Active group member will publish time every {} seconds.'.format(timeInt))
    print('Subject is {}'.format(ap.subj))
    print('Inactive will not publish time')

    err, ap.timerId = tibrvEvent_CreateTimer(TIBRV_DEFAULT_QUEUE, pubTime, timeInt, ap)

    if err != TIBRV_OK:
        print('Error adding repeating timer: -- {}'.foramt(tibrvStatus_GetText(err)))
        sys.exit(3)

    # create RVFT
    err, ap.ft_tx = tibrvTransport_Create(ft_svc, ft_net, ft_daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize fault tolerant transport -- {}'.format(
                    ap.progname, tibrvStatus_GetText(err)))
        sys.exit(3)

    # join RVFT
    err, ap.ft_mem = tibrvftMember_Create(TIBRV_DEFAULT_QUEUE,
                        processInstruction,
                        ap.ft_tx,
                        groupName,
                        ft_weight,
                        numactive,
                        hbInterval,
                        prepareInterval,
                        activateInterval,
                        ap)

    if err != TIBRV_OK:
        print('{} : Failed to join group - {}'.format(ap.progname,tibrvStatus_GetText(err)))
        sys.exit(4)

    # Subscribe to RVFT advisories
    err, advId = tibrvEvent_CreateListener(
                        TIBRV_DEFAULT_QUEUE,
                        advCB, ap.ft_tx,
                        '_RV.*.RVFT.*.' + groupName,
                        ap)

    if err != TIBRV_OK:
        print('{} : Failed to start listening to advisories - {}'.format(
                    ap.progname, tibrvStatus_GetText(err)))
        sys.exit(5)

    # Set Signal Handler for Ctrl-C
    global _running
    signal.signal(signal.SIGINT, signal_proc)

    while _running:
        tibrvQueue_Dispatch(TIBRV_DEFAULT_QUEUE)

    tibrvEvent_Destroy(advId)
    tibrvEvent_Destroy(ap.timerId)
    tibrvftMember_Destroy(ap.ft_mem)

    tibrv_Close()

    return

if __name__ == "__main__":
    main(sys.argv)



