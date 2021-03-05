import zlib
import rncryptor

FILENAME = "SebCfgFile.seb"
PASSWORD = "banana"

compressedFile = open(FILENAME, 'rb').read()
_bytes = zlib.decompress(compressedFile, zlib.MAX_WBITS | 16)

decryptedCompressedXML = rncryptor.decrypt(_bytes[4:], PASSWORD)
decompressedXML = zlib.decompress(decryptedCompressedXML, zlib.MAX_WBITS | 16)

writetoxml = open('seb-settings_enc.xml', 'wb')
writetoxml.write(bytes(decompressedXML))
