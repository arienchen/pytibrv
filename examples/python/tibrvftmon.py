##
# tibrvftmon.py - example TIB/Rendezvous fault tolerant group
#                 monitor program
#
# rewrite TIBRV example: tibrvftmon.c
#
# LAST MODIFIED: V1.0 2016-12-26 ARIEN arien.chen@gmail.com
#
import sys
import signal
import getopt
from pytibrv.Tibrv import *
from pytibrv.TibrvFt import *

# Module Variables
_running = True
_oldNumActives = 0

def signal_proc(signal, frame):
    global _running
    _running = False
    print()
    print('CRTL-C PRESSED')

def usage():
    print()
    print('tibrvftmon.py [options]')
    print('')
    print('options:')
    print('    [--service service]          RVD Service')
    print('    [--network network]          RVD Network')
    print('    [--daemon daemon]            RVD Daemon')
    print()
    sys.exit(1)


def get_params(argv):

    params = ['service=', 'network=', 'daemon=']
    try:
        opts, args = getopt.getopt(argv, '', params)

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

    if len(args) != 0:
        usage()

    return service, network, daemon


def monCB(monitor: TibrvFtMonitor, groupName: str, numActiveMembers: int, closure):
    global _oldNumActives

    if _oldNumActives > numActiveMembers:
        txt = 'one deactivated'
    else:
        txt = 'one activated'

    print('Group [{}]: has {} active members (after {})'.format(
           groupName,
           numActiveMembers,
           txt
         ))

    _oldNumActives = numActiveMembers

    return


# MAIN PROGRAM
def main(argv):

    service, network, daemon = get_params(argv[1:])
    progname = argv[0]
    lostInt = 4.8

    err = Tibrv.open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, TibrvStatus.text(err)))
        sys.exit(1)

    tx = TibrvTx()
    err = tx.create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format(progname, TibrvStatus.text(err)))
        sys.exit(1)

    que = TibrvQueue()

    monitor = TibrvFtMonitor()
    err = monitor.create(que, TibrvFtMonitorCallback(monCB), tx, 'TIBRVFT_TIME_EXAMPLE', lostInt, None)

    if err != TIBRV_OK:
        print('{} : Failed to start group monitor - {}', progname, TibrvStatus.text(err))
        sys.exit(1)\


    print('{} : Waiting for group information...'.format(progname))

    # Set Signal Handler for Ctrl-C
    global _running
    signal.signal(signal.SIGINT, signal_proc)

    while _running:
        que.timedDispatch(0.5)

    # CTRL-C PRESSED
    # when ftMonitor destroyed,
    # callback would be triggered within numActiveMembers = 0
    # it is fault alert, and should be ignored
    monitor.destroy()
    tx.destroy()

    Tibrv.close()


    return

if __name__ == "__main__":
    main(sys.argv)



