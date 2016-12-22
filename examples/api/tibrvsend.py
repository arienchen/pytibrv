

import sys
import getopt
from tibrv.tport import *
from tibrv.msg import *

def usage() :
    print()
    print("tibrvsend.py [-service service] [-network network]")
    print("             [-daemon daemon] <subject> <message>")
    print()
    sys.exit(1)


def get_params(argv):

    try:
        opts, args = getopt.getopt(argv, '', ['service', 'network', 'daemon'])

    except getopt.GetoptError:
        usage()

    service = None
    network = None
    daemon = None

    for opt, arg in opts:
        if opt == '-service':
            service = arg
        elif opt == '-network':
            network = arg
        elif opt == '-daemon':
            daemon = arg
        else:
            usage()

    if len(args) != 2:
        usage()

    return service, network, daemon, args[0], args[1]

# MAIN PROGRAM
def main(argv):

    progname = argv[0]

    service, network, daemon, subj, msg_data = get_params(argv[1:])

    err = tibrv_Open()
    if err != TIBRV_OK:
        print('{}: Failed to open TIB/RV: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err, tx = tibrvTransport_Create(service, network, daemon)
    if err != TIBRV_OK:
        print('{}: Failed to initialize transport: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    tibrvTransport_SetDescription(tx, progname)

    err, msg = tibrvMsg_Create()
    if err != TIBRV_OK:
        print('{}: Failed to create message: {}'.format('', progname, tibrvStatus_GetText(err)))
        sys.exit(1)

    err = tibrvMsg_UpdateString(msg, 'DATA', msg_data)
    if err == TIBRV_OK:
        err = tibrvMsg_SetSendSubject(msg, subj)
        if err == TIBRV_OK:
            err = tibrvTransport_Send(tx, msg)

    if err != TIBRV_OK:
        print('{}: {} in sending "{}" to "{}"'. format(progname, tibrvStatus_GetText(err), msg_data, subj))


    tibrvMsg_Destroy(msg)
    tibrvTransport_Destroy(tx)
    tibrv_Close()

    sys.exit(0)


    return

if __name__ == "__main__" :
   main(sys.argv)



