# -*- coding: utf-8 -*-
import argparse
import sys


class CLI:

    def __init__(self):
        self.version = "1.0.0"

    def getVersion(self):
        return "SockSend CLI version: " + self.version

    def showError(self, msg):
        print(("\n[!] ERROR: " + msg))
        print(("try: SockSender.py --help\n"))

    def showNetInterfaces(self, interfaces):
        print(("\ndiaposable network interfaces:\n  " + interfaces))

    def listenerWaitMessage(self, ip, port):
        print("\n [ SockReceiver ]")
        print(("   Listo para recibir en: [%s:%s]\n" % (ip, port)))

    def senderWaitMessage(self, ip):
        print("\n [ SockSender ]")
        print(("   Enviando a " + ip + "...\n"))

    ## Receiver EventsCallbacks
    def receiverInConn(self):
        print("   incoming connection...")
        print("   waiting headers...\n")

    def receiverInHeaders(self, headers):
        print(("   files sent: %s" % (headers["nfiles"])))

    def receiverReadyRead(self, size):
        tag = "   reading %s bits of data... " % size
        sys.stdout.write(tag + "0%" + (chr(8) * (2)))
        sys.stdout.flush()

    def receiverReadPackage(self, dataReceived, totalData):
        perCent = "%.1f" % ((float(dataReceived) * 100) / float(totalData))
        sys.stdout.write(perCent + "%" + (chr(8) * (len(perCent) + 1)))
        sys.stdout.flush()

    def receiverReadyToSave(self):
        print("\n   saving...")

    def receiverDataSaved(self, path):
        print((("   file saved on %s...") % (path)))

    def getReceiverEventsCallbacks(self):
        events = {
            "onIncomingConnection": self.receiverInConn,
            "onHeadersReceived": self.receiverInHeaders,
            "onReadyToRead": self.receiverReadyRead,
            "onReadPackage": self.receiverReadPackage,
            "onDataSaved": self.receiverDataSaved,
            "onReadyToSave": self.receiverReadyToSave
        }

        return events

    ## Sender EventsCallbacks
    def senderConnectionSuccess(self, welcomeMsg):
        print((welcomeMsg))

    def senderSendingHeaders(self):
        print("   [-] sending headers...")

    def senderSendingHeadersSuccess(self, msg):
        print((msg))

    def senderReadyToSend(self, dataSize):
        print(((("   [-] sending %s bits of data...")) % (dataSize)))

    def senderSendingSuccess(self):
        print("\n   file was sended :D")

    def getSenderEventsCallbacks(self):
        events = {
            "onConnectionSuccess": self.senderConnectionSuccess,
            "onSendingHeaders": self.senderSendingHeaders,
            "onSendingHeadersSuccess": self.senderSendingHeadersSuccess,
            "onReadyToSend": self.senderReadyToSend,
            "onSendingSuccess": self.senderSendingSuccess
        }

        return events

    def getArgsParser(self):
        h = 'Envia y recibe archivos por medio de sockets'
        parser = argparse.ArgumentParser(description=h)

        h = "mostrar información del programa"
        parser.add_argument("-v", "--version", help=h, action="store_true")

        h = "mostrar interfaces disponibles"
        parser.add_argument("-s", "--showinterfaces", help=h,
        action="store_true")

        h = "accion a realizar, enviar/recibir archivos"
        parser.add_argument('-a', '--action',
        choices=['send', 'receive'], help=h)

        h = "archivo para enviar"
        parser.add_argument("-f", "--file", help=h, metavar='FILE')

        h = "carpeta para enviar"
        parser.add_argument("-fl", "--folder", help=h, metavar='FOLDER')

        h = "direccion IP para enviar/recibir"
        parser.add_argument("--ip", help=h, metavar='IP')

        h = "interfaz para enviar/recibir"
        parser.add_argument("-i", "--interface", help=h, metavar='INTERFACE')

        h = "puerto para enviar/recibir (9500 default)"
        parser.add_argument("--port", help=h, metavar='PORT', type=int)

        return parser

    def terminate(self):
        print("   exiting...")
        sys.exit()