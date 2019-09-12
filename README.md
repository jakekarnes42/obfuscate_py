# obfuscate_py
A simple obfuscator compatible with Python 2 and 3. This can be useful for bypassing signature-based anti-virus scans, but doesn't protect against runtime analysis or human review. 

After obfuscation, executing the output program should be functionally the same as executing the input program.

# Usage
The following will obfuscate the example Python 3 program at test/primes3.py and write the output to test/primes3_obfs.py
```bash
python3 obfuscate_py.py -i test/primes3.py -o test/primes3_obfs.py
```
Also compatible with Python 2 (both for executing the obfuscator and the output program itself)
```bash
python2 obfuscate_py.py -i test/primes2.py -o test/primes2_obfs.py
```

In these example programs, if the primes3.py or primes2.py programs were blocked by anti-virus then the output programs (primes3_obfs.py and primes2_obfs.py) should not be flagged. 


## Using with stdin and stdout
If the input or output files are not specified, then the program will use stdin and stdout respectively. This means that input and output programs can be piped easily for use with other tools. 

For example, we can pipe in some Python code and the obfuscated output is returned to stdout:
```bash
# echo "print('hello world')" | python3 obfuscate_py.py
import base64;exec(base64.b64decode('ZXhlYygnJycKaW1wb3J0IHN5cwprYiA9IGJhc2U2NC5iNjRkZWNvZGUoIk1VSTRNWEJUV0dSMU5UWkRZVlV3TlV0M1ZHVlNUbE5TWmpOdVprVklWM0U9IikKa2RiID0gKGJ5dGVzKGtiKSxieXRlYXJyYXkoa2IpKVtzeXMudmVyc2lvbl9pbmZvIDwgKDMsIDApXQoKZGIgPSBiYXNlNjQuYjY0ZGVjb2RlKCJvWTQyNmsvanAyRkxTd1gvdHY1RWNkc21Bc3FUNy8rZWVpcE1FTjFzL1MzM0VzZ3puZE1mY3ZJQmo1NTdCM1daTmtXbm5vV0p3Y3F4bm1MUEREWXBrWHdReUVkSG9nPT0iKQpkZGIgPSAoYnl0ZXMoZGIpLGJ5dGVhcnJheShkYikpW3N5cy52ZXJzaW9uX2luZm8gPCAoMywgMCldCiAgClMgPSBsaXN0KHJhbmdlKDB4MTAwKSkKaiA9IDAKZm9yIGkgaW4gcmFuZ2UoMHgxMDApOgogIGogPSAoU1tpXSArIGtkYltpICUgbGVuKGtkYildICsgaikgJiAweGZmCiAgU1tpXSwgU1tqXSA9IFNbal0sIFNbaV0KeCA9IHkgPSAwCmMgPSBbXQpmb3IgYSBpbiBkZGI6CiAgeCA9ICh4ICsgMSkgJiAweGZmCiAgeSA9IChTW3hdICsgeSkgJiAweGZmCiAgU1t4XSwgU1t5XSA9IFNbeV0sIFNbeF0KICBpID0gKFNbeF0gKyBTW3ldKSAmIDB4ZmYKICBjLmFwcGVuZChhIF4gU1tpXSkKCmNiID0gKGJ5dGVzKGMpLGJ5dGVhcnJheShjKSlbc3lzLnZlcnNpb25faW5mbyA8ICgzLCAwKV0KY3MgPSAoY2IuZGVjb2RlKCd1dGYtOCcpLHN0cihjYikpW3N5cy52ZXJzaW9uX2luZm8gPCAoMywgMCldCmV4ZWMoY3MpCiAgJycnKQ=='.encode('utf-8')))
# echo "print 'hello world'" | python2 obfuscate_py.py
import base64;exec(base64.b64decode('ZXhlYygnJycKaW1wb3J0IHN5cwprYiA9IGJhc2U2NC5iNjRkZWNvZGUoImNUaG9ZMWhyZGxwQmF6TXhkek5ITW5CdmVFbzNUVzVGV20wNE1FSlpZMHM9IikKa2RiID0gKGJ5dGVzKGtiKSxieXRlYXJyYXkoa2IpKVtzeXMudmVyc2lvbl9pbmZvIDwgKDMsIDApXQoKZGIgPSBiYXNlNjQuYjY0ZGVjb2RlKCJHT05EekloTjVIZUJGR2FqY3dqOSs4V3BQUTlZZWUvam01c0MzeGNtYmJEbnBLK081UThLU2t6L0NUSThyc0xCTHA3Yzc2MHc3OWZta1B4SHpOVlovUWlUTTY0TTV3PT0iKQpkZGIgPSAoYnl0ZXMoZGIpLGJ5dGVhcnJheShkYikpW3N5cy52ZXJzaW9uX2luZm8gPCAoMywgMCldCiAgClMgPSBsaXN0KHJhbmdlKDB4MTAwKSkKaiA9IDAKZm9yIGkgaW4gcmFuZ2UoMHgxMDApOgogIGogPSAoU1tpXSArIGtkYltpICUgbGVuKGtkYildICsgaikgJiAweGZmCiAgU1tpXSwgU1tqXSA9IFNbal0sIFNbaV0KeCA9IHkgPSAwCmMgPSBbXQpmb3IgYSBpbiBkZGI6CiAgeCA9ICh4ICsgMSkgJiAweGZmCiAgeSA9IChTW3hdICsgeSkgJiAweGZmCiAgU1t4XSwgU1t5XSA9IFNbeV0sIFNbeF0KICBpID0gKFNbeF0gKyBTW3ldKSAmIDB4ZmYKICBjLmFwcGVuZChhIF4gU1tpXSkKCmNiID0gKGJ5dGVzKGMpLGJ5dGVhcnJheShjKSlbc3lzLnZlcnNpb25faW5mbyA8ICgzLCAwKV0KY3MgPSAoY2IuZGVjb2RlKCd1dGYtOCcpLHN0cihjYikpW3N5cy52ZXJzaW9uX2luZm8gPCAoMywgMCldCmV4ZWMoY3MpCiAgJycnKQ=='.encode('utf-8')))
```

We can also obfuscate the input code and pipe it into Python to execute immediately. This doesn't actually help us much, but it's a nice verification that the program works after obfuscation.
```bash
# echo "print('hello world')" | python3 obfuscate_py.py | python3
hello world
# echo "print 'hello world'" | python2 obfuscate_py.py | python2
hello world
```

# How it works
The obfuscation program wraps the input program in layers of base64 encoding and RC4 encryption. The base64 encoding normalizes the input program and the RC4 encryption randomizes the text to help prevent signature-based detection.

When the output program is run, the layers are executed and unwrapped, and then the input program itself is executed. 

# Limitations
The obfuscation doesn't protect against run-time analysis, and it's simple for a human to "unwrap" the layers of obfuscation. The program is only "hidden" from the very specific signature-based analysis. Fortunately, this is often all we need. 

## RC4 Encryption 
It's important to note that the input program is truly encrypted with RC4, it's not actually _protected_. The RC4 encryption is used as a randomization technique and the key is included in the output program. It is trivial to decrypt the program because the encryption key and decryption code are included in the obfuscated output. 
