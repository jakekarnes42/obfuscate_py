# obfuscate_py
A simple obfuscator compatible with Python 2 and 3. This can be useful for bypassing signature-based anti-virus scans, but doesn't protect against runtime analysis or human review. 

After obfuscation, executing the output program should be functionally the same as executing the input program.

# Usage
The following will obfuscate the example Python 3 program at test/primes3.py and write the output to test/primes3_obfs.py
```
python3 obfuscate_py.py -i test/primes3.py -o test/primes3_obfs.py
```
Also compatible with Python 2 (both for executing the obfuscator and the output program itself)
```
python2 obfuscate_py.py -i test/primes2.py -o test/primes2_obfs.py
```

In these example programs, if the primes3.py or primes2.py programs were blocked by anti-virus then the output programs (primes3_obfs.py and primes2_obfs.py) should not be flagged. 

## stdin and stdout
If the input or output files are not specified, then the program will use stdin and stdout respectively. This means that input and output programs can be piped easily for use with other tools. 

# How it works
The obfuscation program wraps the input program in layers of base64 encoding and RC4 encryption. The base64 encoding normalizes the input program and the RC4 encryption randomizes the text to help prevent signature-based detection.

When the output program is run, the layers are executed and unwrapped, and then the input program itself is executed. 

# Limitations
The obfuscation doesn't protect against run-time analysis, and it's fairly simple for a human to "unwrap" the layers of obfuscation.

## RC4 Encryption
It's important to note that the input program is truly encrypted with RC4, it's not actually _protected_. The RC4 encryption is used as a randomization technique and the key is included in the output program. It is trivial to decrypt the program because the encryption key and decryption code are included in the obfuscated output. 
