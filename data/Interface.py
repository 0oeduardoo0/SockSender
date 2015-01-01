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

    def senderWaitMessage(self, ip, fileName):
        print("\n [ SockSender ]")
        print(("   Enviando " + fileName + " a " + ip + "...\n"))

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

        h = "direccion IP para enviar/recibir"
        parser.add_argument("--ip", help=h, metavar='IP')

        h = "interfaz para enviar/recibir"
        parser.add_argument("-i", "--interface", help=h, metavar='INTERFAZ')

        h = "puerto para enviar/recibir (9500 default)"
        parser.add_argument("--port", help=h, metavar='PORT', type=int)

        return parser

    def terminate(self):
        print("   exiting ...")
        sys.exit()