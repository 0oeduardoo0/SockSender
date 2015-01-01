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


class Sender(Common):

    filePath = "foo"

    def __init__(self):
        self.version = "1.0.0"
        self.name = "SocketSender"

    def setFilePath(self, filePath):
        self.filePath = filePath

    def start(self):
        hParser = Files.HeadersParser()
        fileData = hParser.encode(self.filePath)

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((self.ip, self.port))

        #welcome message
        print((cliente.recv(255)))

        #sending headers
        fileSize = fileData["meta"]["size"]
        print("   M: sending headers...")
        cliente.send(fileData["headers"])
        print((cliente.recv(255)))

        #sending data
        print(((("   M: sending %s bits of data...")) % (fileSize)))
        cliente.send(fileData["meta"]["content"])

        cliente.close()


class Receiver(Common):

    def __init__(self):
        self.version = "1.0.0"
        self.name = "SocketReceiver"

    def setNetInterface(self, i):
        addrs = netifaces.ifaddresses(i)
        addrs = addrs[netifaces.AF_INET]
        self.ip = addrs[0]["addr"]

    def start(self):
        hParser = Files.HeadersParser()
        writer = Files.Writer()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(1)

        #while 1:
        add, port = server.accept()
        print("   incoming connection...")
        print("   waiting headers...\n")
        add.send("   S: hello, i'm server :3...")

        #headers
        headersPlain = add.recv(1024)
        headers = hParser.decode(headersPlain)
        print((headersPlain))

        #Content
        add.send("   S: ready for receive data...")
        print((("\n   reading %s bits of data...") % (headers["size"])))

        content = ""
        while 1:
            read = add.recv(1024)
            if not read:
                break
            else:
                content += read

        writer.write(headers["name"], content)

        add.close()
        server.shutdown(socket.SHUT_RDWR)
        server.close()