#! /usr/bin/env python3
import zlib 
import rncryptor  
import os 
import time
import shutil

#decrypt/decompress .seb file
def decrypt_decompress(settingsFile,passwd):
  hex_text = zlib.decompress(seb_open(settingsFile), zlib.MAX_WBITS | 16)
  decryptedCompXML = rncryptor.decrypt(hex_text[4:],passwd) 
  decompressedXML = zlib.decompress(decryptedCompXML, zlib.MAX_WBITS | 16)

  return decompressedXML


#first 4 bytes - pkhs | phsk | pswd | plnd | pwcc
def view_4bytes(settingsFile,passwd):
  first_decompress_text = zlib.decompress(seb_open(settingsFile), zlib.MAX_WBITS | 16)
  print("[+]Prefix: " + first_decompress_text[:4].decode("utf-8")) 
  
  return first_decompress_text[:4].decode("utf-8")

def seb_open(settingsFile):
  try:
    sebfile = open(settingsFile, 'rb').read()
    return sebfile
  except IOError: 
    print("Error: This .seb file don't exist!")
    return 0

def write2xml(fileName,xml_text):
  xmlFile= open(fileName+'.xml','wb')
  xmlFile.write(xml_text)
  print('Creating ' + fileName +'.xml...')
  time.sleep(1)

#simple way to change lines of .xml to do an screenshot in exam (PoC)
def change_xml(fileName,passwd):
 
  if passwd == '': #.xml unecrypted
    newXmlFile= open(fileName+'.xml','r')
    xmlData=newXmlFile.read()
    newXmlFile.close()

    allowScreenWindow= xmlData.replace("<key>allowScreenCapture</key><false/>","<key>allowScreenCapture</key><true/>").replace("<key>allowWindowCapture</key><false/>","<key>allowWindowCapture</key><true/>")

    newXmlFile= open(fileName+'-new.xml','w+')
    newXmlFile.write(allowScreenWindow)
    newXmlFile.close()	


  else: #.xml encrypted
    with open(fileName+'.xml','r') as xmlfile:
      xmldata = xmlfile.readlines()

    allowScreen = xmldata[36].lstrip().rstrip()
    allowWindow = xmldata[54].lstrip().rstrip()

    if allowScreen == '<key>allowScreenCapture</key>':
      xmldata[37] = '\t<true/>\n'
    else:
      print('[X]Wrong line for ScreenCapture')
      
    if allowWindow == '<key>allowWindowCapture</key>':
      xmldata[55] = '\t<true/>\n'
    else:
      print('[X]Wrong line for WindowCapture')

    with open(fileName+'-new.xml','w+') as xmlfile:
      xmlfile.writelines(xmldata)

def clean(first_compress):
  try: 
    os.remove(first_compress)
  except FileNotFoundError: 
    print("Error: File doesn't exist!")

def encrypt_compress(prefix,fileName,passwd):
  xmlFile = open(fileName+'-new.xml', 'r')
  xmlText = xmlFile.read()

  xmlParsed = bytes(xmlText, encoding='latin1')
  
  gzip = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
  gzip_wrapper = zlib.compressobj(0, zlib.DEFLATED, zlib.MAX_WBITS | 16)

  xmlCompressed = gzip.compress(xmlParsed) + gzip.flush()
  xmlEncrypted = rncryptor.encrypt(xmlCompressed, passwd)

  with open(fileName, 'wb') as f:
    f.write(bytes(prefix,encoding='latin-1'))
    f.seek(4, 0)
    f.write(xmlEncrypted)

  with open(fileName, 'rb') as binFile: 
    data = binFile.read()
    sebCracked = open(fileName+'-cracked.seb', 'wb')
    compressedData = gzip_wrapper.compress(data) + gzip_wrapper.flush()
    sebCracked.write(compressedData)

  clean(fileName)

def main():
  
  settingsFile = input('[+]Seb file: ')
  passwd = input('[+]Settings password: ')
  fileName = settingsFile[:-4] #delete extension
  prefix='pswd' 
  #prefix = view_4bytes(settingsFile,passwd) #show the prefix of .seb file
  
 #if prefix == 'pswd':
 
  if passwd == '': #unecrypted .seb 
    shutil.copyfile(settingsFile,fileName+'.xml')
  else: #encrypted .seb
    xml_text = decrypt_decompress(settingsFile,passwd)
    write2xml(fileName,xml_text)
    print("[+]Decompressed with success!") 
    
  change_xml(fileName,passwd)    
  encrypt_compress(prefix,fileName,passwd)
  print("[+]...Enjoy!") 

  #else:
  #  print("[X]Error: Prefix need to be PSWD")

if __name__ == "__main__":
  main()

 
