import zlib
import rncryptor

FILENAME = "SebClientSettings-RC.seb"
PASSWORD = "setnow"

compressedFile = open(FILENAME, 'rb').read()
_bytes = zlib.decompress(compressedFile, zlib.MAX_WBITS | 16)

decryptedCompressedXML = rncryptor.decrypt(_bytes[4:], PASSWORD)
decompressedXML = zlib.decompress(decryptedCompressedXML, zlib.MAX_WBITS | 16)

writetoxml = open('seb-settings.xml', 'wb')
writetoxml.write(bytes(decompressedXML))
