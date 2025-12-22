```
CryptoCoreUtils/
├── cryptocoreutils/           
│   ├── crypto/               
│   │   ├── __init__.py
│   │   ├── aes.py           
│   │   └── padding.py       
│   ├── hash/                 
│   │   ├── __init__.py
│   │   ├── sha256.py        
│   │   └── sha3_256.py 
│   ├── kdf/
│   │   ├── __init__.py
│   │   ├── hkdf.py   
│   │   └── pbkdf2.py 
│   ├── mac/                  
│   │   ├── __init__.py
│   │   └── hmac.py          
│   ├── modes/               
│   │   ├── __init__.py
│   │   ├── ecb.py          
│   │   ├── cbc.py          
│   │   ├── cfb.py          
│   │   ├── ofb.py          
│   │   ├── ctr.py 
│   │   ├── etm.py        
│   │   └── gcm.py          
│   ├── __init__.py         
│   ├── cli.py              
│   ├── csprng.py           
│   ├── exceptions.py       
│   └── file_io.py 
├── docs/ 
│   ├── API.md
│   ├── DEVELOPMENT.md
│   ├── CHANGELOG.md
│   └── USERGUIDE.md        
├── tests/                  
│   ├── __init__.py
│   ├── integration/  
│   │   ├── __init__.py
│   │   ├── test_cli_crypto.py
│   │   ├── test_cli_derive.py
│   │   └── test_cli_hash.py
│   ├── unit/  
│   │   ├── __init__.py
│   │   ├── test_aes.py
│   │   ├── test_csprng.py
│   │   ├── test_gcm.py
│   │   ├── test_hkdf.py
│   │   ├── test_hmac.py
│   │   ├── test_modes.py
│   │   ├── test_pbkdf2.py
│   │   ├── test_sha3_256.py
│   │   ├── test_sha256.py
│   │   └── test_hash.py
│   ├── vectors/
│   │   ├── __init__.py
│   │   ├── test_aes_vectors.py
│   │   ├── test_hmac_vectors.py
│   │   ├── test_pbkdf2_vectors.py
│   │   └── test_sha_vectors.py
│   ├── plain.txt        
│   ├── cipher.bin
│   ├── decrypted.txt
│   ├── run_tests.py
│   └── modified.txt
├── .gitignore
├── main.py               
├── README.md             
└── requirements.txt
```
## Требования

- Python 3.8 или выше
- pycryptodome 3.23.0 или выше
- numba
- numpy
