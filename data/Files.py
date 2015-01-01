# -*- coding: utf-8 -*-


class Writer():

    def write(self, path, content):
        f = open(path, "wb")
        f.write(content)
        print((("   file saved on %s...") % (path)))
        f.close()


class HeadersParser:

    def encode(self, filePath):
        fileObj = open(filePath, "rb")

        content = fileObj.read()

        meta = {
            "name": fileObj.name,
            "size": len(content),
            "type": fileObj.name.split(".")[1],
            "content": content
        }

        headers = ""
        headers += "   name: %s\n" % (meta["name"])
        headers += "   size: %s\n" % (meta["size"])
        headers += "   type: %s" % (meta["type"])

        return {"meta": meta, "headers": headers}

    def decode(self, encoded):
        encoded = encoded.split("\n")
        meta = {}

        for line in encoded:
            line = line.split(":")
            var, val = line[0].strip(), line[1].strip()
            meta[var] = val

        return meta