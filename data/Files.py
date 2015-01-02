# -*- coding: utf-8 -*-
import os


class Reader():

    def listDirFiles(self, dirPath):
        l = os.listdir(dirPath)
        files = []

        if dirPath[-1:] != "/" or dirPath[-1:] != "\\":
            if os.name == "nt":  # win
                dirPath += "\\"
            else:
                dirPath += "/"

        for item in l:
            item = dirPath + item
            if os.path.isfile(item):
                files.append(item)

        return ",".join(files)


class Writer():

    def write(self, path, content):
        f = open(path, "wb")
        f.write(content)
        f.close()


class HeadersParser:

    def encode(self, filePaths):
        headers = ""
        content = []
        names = []

        for filePath in filePaths.split(","):
            fileObj = open(filePath, "rb")
            names.append(os.path.basename(fileObj.name))
            content.append(fileObj.read())

        content = "<ss[file_ending]ss>".join(content)

        meta = {
            "files": ",".join(names),
            "nfiles": len(names),
            "size": len(content),
            "content": content
        }

        headers += "   files: %s\n" % (meta["files"])
        headers += "  nfiles: %s\n" % (meta["nfiles"])
        headers += "    size: %s" % (meta["size"])

        return {"meta": meta, "headers": headers}

    def decode(self, encoded):
        encoded = encoded.split("\n")
        meta = {}

        for line in encoded:
            line = line.split(":")
            var, val = line[0].strip(), line[1].strip()
            meta[var] = val

        return meta

    def decodeContent(self, c):
        return c.split("<ss[file_ending]ss>")

    def decodeNames(self, n):
        return n.split(",")