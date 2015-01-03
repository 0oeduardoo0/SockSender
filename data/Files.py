# -*- coding: utf-8 -*-
# author: Eduardo B <ms7rbeta@gmail.com>
# site: http://root404.com/eduardo
import os


class Reader():

    def listDirFiles(self, dirPath):
        """Lista los archivos del directorio indicado

        Solo archivos del directorio, el listado no es recursivo
        retorna las rutas de los archivos en una cadena separados
        por "," (coma).

        Parámetros:
        dirPath -- Ruta del directorio a listar

        """
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
        """Escribir un archivo

        Escribe en el fichero indicado el contenido.

        Parámetros:
        path -- Ruta del archivo
        content -- Contenido del archivo

        """
        f = open(path, "wb")
        f.write(content)
        f.close()


class HeadersParser:
    contentEncodeFlag = "<ss[file_ending]ss>"

    def encode(self, filePaths):
        """Codifica las cabeceras

        Codifica los datos de los archivos que se van a enviar, en una cadena
        que pueda ser transmitida por el socket y posteriormente decodificada
        por el servicio receptor.

        Parámetros:
        filePaths -- Ruta(s) de el/los archivos (separadas por ",").

        """

        headers = ""
        size = 0
        content = []
        names = []

        for filePath in filePaths.split(","):
            fileObj = open(filePath, "rb")
            names.append(os.path.basename(filePath))
            size += os.path.getsize(filePath)
            content.append(fileObj.read())

        content = self.contentEncodeFlag.join(content)

        meta = {
            "files": ",".join(names),
            "nfiles": len(names),
            "size": size,
            "content": content
        }

        headers += "   files: %s\n" % (meta["files"])
        headers += "  nfiles: %s\n" % (meta["nfiles"])
        headers += "    size: %s" % (meta["size"])

        return {"meta": meta, "headers": headers}

    def decode(self, encoded):
        """Decodifica una cadena de cabecera

        Devuelve un diccionario con los datos de las cabeceras recibidas

        Parámetros:
        encoded -- Cadena de las cabeceras

        """

        encoded = encoded.split("\n")
        meta = {}

        for line in encoded:
            line = line.split(":")
            var, val = line[0].strip(), line[1].strip()
            meta[var] = val

        return meta

    def decodeContent(self, c):
        """Decodifica el contenido de los archivos

        Separa en un arreglo el contenido de cada archivo en base
        a la bandera de codificacion para el contenido de los archivos.

        Parámetros:
        c -- Datos enviados por el servicio cliente

        """
        return c.split(self.contentEncodeFlag)

    def decodeNames(self, n):
        """Decodifica los nombres de los archivos

        Separa en un arreglo los nombres de los archivos enviados
        por el servicio cliente

        Parámetros:
        n -- Cadena de la cabecera nombres

        """
        return n.split(",")