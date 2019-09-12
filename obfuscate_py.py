#!/usr/bin/env python
import argparse
import os.path
import sys, random, string, base64

#Takes in bytes, and returns a b64 encoded string of the bytes
def b64_bytes(my_bytes):
  assert(isinstance(my_bytes, (bytes, bytearray)))
  #base64 encode the bytes
  if sys.version_info < (3, 0):
      my_str = str(base64.b64encode(my_bytes))
  else:
      my_str = base64.b64encode(my_bytes).decode('utf-8')
  return my_str

#Takes in BYTES of key and data. Returns BYTES of RC4 crypted data
def rc4_encrypt(key_bytes, data_bytes):
  assert(isinstance(key_bytes, (bytes, bytearray)))
  assert(isinstance(data_bytes, (bytes, bytearray)))

  #Encrypt those data_bytes with rc4 using the key_bytes
  S = list(range(0x100))
  j = 0
  for i in range(0x100):
    j = (S[i] + key_bytes[i % len(key_bytes)] + j) & 0xff
    S[i], S[j] = S[j], S[i]
  x = y = 0
  crypted = []
  for a in data_bytes:
    x = (x + 1) & 0xff
    y = (S[x] + y) & 0xff
    S[x], S[y] = S[y], S[x]
    i = (S[x] + S[y]) & 0xff
    crypted.append(a ^ S[i])

  #The crypted list is a list of crypted bytes. Convert to bytes or bytearray
  if sys.version_info < (3, 0):
      crypted_bytes = bytearray(crypted)
  else:
      crypted_bytes = bytes(crypted)
  
  return crypted_bytes

def rc4_crypt_wrap(key_bytes, data_bytes):
  #base64 encode the key and data so they can be injected into the code string later
  key_str = b64_bytes(key_bytes)
  data_str = b64_bytes(data_bytes)

  rc4_magic = '''
import sys
kb = base64.b64decode("{insert_key_str}")
kdb = (bytes(kb),bytearray(kb))[sys.version_info < (3, 0)]

db = base64.b64decode("{insert_data_str}")
ddb = (bytes(db),bytearray(db))[sys.version_info < (3, 0)]
  
S = list(range(0x100))
j = 0
for i in range(0x100):
  j = (S[i] + kdb[i % len(kdb)] + j) & 0xff
  S[i], S[j] = S[j], S[i]
x = y = 0
c = []
for a in ddb:
  x = (x + 1) & 0xff
  y = (S[x] + y) & 0xff
  S[x], S[y] = S[y], S[x]
  i = (S[x] + S[y]) & 0xff
  c.append(a ^ S[i])

cb = (bytes(c),bytearray(c))[sys.version_info < (3, 0)]
cs = (cb.decode('utf-8'),str(cb))[sys.version_info < (3, 0)]
exec(cs)
  '''.format(insert_key_str=key_str, insert_data_str=data_str)
  my_output = "exec('''" + rc4_magic +"''')"
  return (my_output)

#Takes in code, encrypts with rc4, returns code to decrypt and execute.
def rc4_py(code):

  #Let's generate a pseudo-random key and convert it to bytes or bytearray
  my_key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
  if sys.version_info < (3, 0):
    my_key_bytes = bytearray(my_key,'utf8')
  else:
    my_key_bytes = bytes(my_key, 'utf8')

  #Convert the code to bytes
  if sys.version_info < (3, 0):
    code_bytes = bytearray(code,'utf8')
  else:
    code_bytes = bytes(code,'utf8')

  #Encrypt the code with the key
  encrypted_bytes = rc4_encrypt(my_key_bytes, code_bytes)

  #Now, encrypted_bytes has our encrypted source code.
  #Wrap the code in the decyption function
  wrapped_code = rc4_crypt_wrap(my_key_bytes, encrypted_bytes)

  return wrapped_code

#Takes in code, encodes as base 64, returns code to decode and execute.
def b64_py(code):
  b64_encoded = base64.b64encode(code.encode('utf-8'))
  return "exec(base64.b64decode('"+b64_encoded.decode('utf-8')+"'.encode('utf-8')))"


if __name__ == '__main__':
  #Setup command line args and parser
  parser = argparse.ArgumentParser(description='Obfuscate the input python program. This is not hard to foil. User beware.')
  parser.add_argument('-i','--infile', type=argparse.FileType('r'), default=sys.stdin, help='the input Python program. If omitted, use stdin.')
  parser.add_argument('-o','--outfile', type=argparse.FileType('w'), default=sys.stdout, help='the output file. If omitted, use stdout.')
  parser.add_argument('-b1','--base64_1', type=int, default=1, help='the number of rounds for base64 encoding. If omitted, use a single round.')
  args = parser.parse_args()
  
  #Load the python code
  program_body = args.infile.read()
  args.infile.close()

  #N rounds of base64 encoding
  for n in range(args.base64_1):
    program_body = b64_py(program_body)

  #A round of rc4 for randomness
  program_body = rc4_py(program_body)
  
  #N rounds of base64 encoding
  for n in range(args.base64_1):
    program_body = b64_py(program_body)
  
  #Add an import statement at the beginning so we can base64 decode  
  program_body = "import base64;" + program_body
  
  #print(program_body)
  args.outfile.write(program_body)
  args.outfile.close()
