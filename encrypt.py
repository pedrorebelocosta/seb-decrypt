import zlib
import rncryptor

FILENAME = "SebCfgFile"
PASSWORD = "banana"

xmlFile = open('seb-settings.xml', 'r')
rawXML = xmlFile.read()

prefix = bytes('pswd', encoding='latin1')
parsedXml = bytes(rawXML, encoding='latin1')

gzip = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
wrapper = zlib.compressobj(0, zlib.DEFLATED, zlib.MAX_WBITS | 16)

compressedXML = gzip.compress(parsedXml) + gzip.flush()
encryptedXML = rncryptor.encrypt(compressedXML, PASSWORD)

with open(FILENAME, 'wb') as file:
	file.write(prefix)
	file.seek(4, 0)
	file.write(encryptedXML)

with open(FILENAME, 'rb') as binFile: 
	data = binFile.read()
	finalSeb = open(FILENAME+'.seb', 'wb')
	compressedData = wrapper.compress(data) + wrapper.flush()
	finalSeb.write(compressedData)
