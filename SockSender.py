#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import Interface
from data import Core


def main():

    cli = Interface.CLI()
    sender = Core.Sender()
    receiver = Core.Receiver()

    parser = cli.getArgsParser()
    args = parser.parse_args()

    if args.version:
        sv = sender.getVersion()
        rv = receiver.getVersion()
        iv = cli.getVersion()
        print((("\n%s\n%s\n%s") % (iv, sv, rv)))
        cli.terminate()

    if args.showinterfaces:
        cli.showNetInterfaces(receiver.getNetInterfaces())
        cli.terminate()

    if args.action == "send":
        if not args.file:
            cli.showError("missing file name")
            cli.terminate()

        if not args.ip:
            cli.showError("missing ip addres")
            cli.terminate()

        if args.port:
            receiver.setPort(args.port)

        sender.setIp(args.ip)
        sender.setFilePath(args.file)
        cli.senderWaitMessage(args.ip, args.file)
        sender.start()
        cli.terminate()

    elif args.action == "receive":
        if args.interface:
            try:
                receiver.setNetInterface(args.interface)
            except:
                cli.showError("invalid interface " + args.interface)
                cli.showNetInterfaces(receiver.getNetInterfaces())
                cli.terminate()
        elif args.ip:
            receiver.setIp(args.ip)
        else:
            cli.showError("missing params IP or INTERFACE")
            cli.terminate()

        if args.port:
            receiver.setPort(args.port)

        ip = receiver.getIp()
        port = receiver.getPort()
        receiver.setEventsCallbacks(cli.getReceiverEventsCallbacks())
        cli.listenerWaitMessage(ip, port)
        receiver.start()
        cli.terminate()

    #if not args
    parser.print_help()
    cli.showNetInterfaces(receiver.getNetInterfaces())
    cli.terminate()

if __name__ == "__main__":
    main()