import zlib
import rncryptor
import gzip

FILENAME = "SebCfgFile"
PASSWORD = "banana"

xmlFile = open('seb-settings.xml', 'r')
rawXML = xmlFile.read()

prefix = bytes('pswd', encoding='latin1')
parsedXml = bytes(rawXML, encoding='utf-8')

compressedXML = zlib.compress(parsedXml)
encryptedXML = rncryptor.encrypt(compressedXML, PASSWORD)

file = open(FILENAME, 'wb')
file.write(prefix)
file.seek(4, 0)
file.write(bytes(encryptedXML))

file2 = open(FILENAME, 'rb')
data = file2.read()

# Last step would be to create a .seb file
# Which is nothing more than a gzip archive without the file headers
