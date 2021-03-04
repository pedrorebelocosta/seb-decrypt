import zlib
import rncryptor

FILENAME = "file-in.seb"
PASSWORD = "banana"

file = open('seb-settings.xml', 'rb')
byteStr = file.read()

prefix = bytes('pswd', encoding='latin1')
compressedXML = zlib.compress(byteStr, 9)
encryptedXML = rncryptor.encrypt(compressedXML, PASSWORD)

with open('lol'+FILENAME, 'wb+') as f:
    f.write(prefix)
    f.seek(5, 0)
    f.write(bytes(encryptedXML))

file2 = open('lol'+FILENAME, 'rb')
data = file2.read()

print(data)
print('writing another file')
file3 = open('test.seb', 'wb')
compressedData = zlib.compress(data, 0)
file3.write(compressedData)

filer = open('test.seb', 'rb')
print(filer.read())
