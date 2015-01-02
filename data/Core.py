# -*- coding: utf-8 -*-
import socket
from . import Files
try:
    import netifaces
except ImportError:
    print(("""
        SockSender requiere 'netiface':\n
        sudo apt-get install python-netifaces - para debian y derivados
    """))


class Common:
    version = "1.0.0"
    name = "foo"
    port = 9601
    ip = "localhost"

    def setIp(self, ip):
        self.ip = ip

    def setPort(self, port):
        self.port = port

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port

    def getNetInterfaces(self):
        return ", ".join(netifaces.interfaces())

    def getVersion(self):
        return self.name + " version: " + self.version

    def setEventsCallbacks(self, events):
        raise NotImplementedError("should have implemented this")


class Sender(Common):
    filePath = ""
    onConnectionSuccess = ""
    onSendingHeaders = ""
    onSendingHeadersSuccess = ""
    onReadyToSend = ""
    onSendingSuccess = ""

    def __init__(self):
        self.version = "1.0.0"
        self.name = "SocketSender"

    def setFilePath(self, filePath):
        self.filePath = filePath

    def setEventsCallbacks(self, events):
        self.onConnectionSuccess = events["onConnectionSuccess"]
        self.onSendingHeaders = events["onSendingHeaders"]
        self.onSendingHeadersSuccess = events["onSendingHeadersSuccess"]
        self.onReadyToSend = events["onReadyToSend"]
        self.onSendingSuccess = events["onSendingSuccess"]

    def start(self):
        hParser = Files.HeadersParser()
        fileData = hParser.encode(self.filePath)

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((self.ip, self.port))

        #welcome message
        welcomeMsg = cliente.recv(255)
        self.onConnectionSuccess(welcomeMsg)  # event

        #sending headers
        self.onSendingHeaders()  # event
        cliente.send(fileData["headers"])
        msg = cliente.recv(255)
        self.onSendingHeadersSuccess(msg)  # event

        #sending data
        self.onReadyToSend(fileData["meta"]["size"])  # event
        cliente.send(fileData["meta"]["content"])
        self.onSendingSuccess()  # event

        cliente.close()


class Receiver(Common):
    onIncomingConnection = ""
    onHeadersReceived = ""
    onReadyToRead = ""
    onDataSaved = ""
    onReadPackage = ""
    onReadyToSave = ""

    def __init__(self):
        self.version = "1.0.0"
        self.name = "SocketReceiver"

    def setNetInterface(self, i):
        addrs = netifaces.ifaddresses(i)
        addrs = addrs[netifaces.AF_INET]
        self.ip = addrs[0]["addr"]

    def setEventsCallbacks(self, events):
        self.onIncomingConnection = events["onIncomingConnection"]
        self.onHeadersReceived = events["onHeadersReceived"]
        self.onReadyToRead = events["onReadyToRead"]
        self.onDataSaved = events["onDataSaved"]
        self.onReadPackage = events["onReadPackage"]
        self.onReadyToSave = events["onReadyToSave"]

    def start(self):
        hParser = Files.HeadersParser()
        writer = Files.Writer()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(1)

        add, port = server.accept()
        self.onIncomingConnection()  # event
        add.send("   [+] hello, i'm server :3...")

        #headers
        headers = hParser.decode(add.recv(1024))
        self.onHeadersReceived(headers)  # event

        #Content
        add.send("   [+] i'm ready for receive data...")
        self.onReadyToRead(headers["size"])  # event

        content = ""
        dataReceived = 0
        while 1:
            read = add.recv(1024)
            if not read:
                break
            else:
                content += read
                dataReceived += len(read)
                self.onReadPackage(dataReceived, headers["size"])

        self.onReadyToSave()  # event
        files = hParser.decodeContent(content)
        names = hParser.decodeNames(headers["files"])
        i = 0

        for f in files:
            writer.write(names[i], f)
            self.onDataSaved(names[i])  # event
            i += 1

        add.close()
        server.shutdown(socket.SHUT_RDWR)
        server.close()