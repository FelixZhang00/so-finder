# so-finder
A simple script to find a share-library(so) which has the symbol name you give in a Android device.

## Usage

```sh
-i give the symbol name which is a import symbol in the so file to find;
-e give the symbol name which is a export symbol in the so file to find;
-a give the symbol name will find all so files which has the symbol name in it's symtab;
```

### Example
1.Get usage information.

```sh
$ python sofinder.py -h  
usage: sofinder.py [-h] [--impor IMPOR] [--export EXPORT] [--all ALL]

Uses sofinder to find a Share-Librarys(so) which has the symbol name you give in a Android device.

optional arguments:
  -h, --help            show this help message and exit
  --impor IMPOR, -i IMPOR
                        A symbol name which is a import symbol in the so file to find.
  --export EXPORT, -e EXPORT
                        A symbol name which is a export symbol in the so file to find.
  --all ALL, -a ALL     A the symbol name will find all so files which has the symbol name in its symtab

```

2.Give a symbol name which is a import symbol in the so file's symtab,and then this script will find these so files.
This example shows how to find so files which import `getaddrinfo` symbol on Android device. 

```sh
$ python sofinder.py -i getaddrinfo
/system/app/WebViewGoogle/lib/arm/libwebviewchromium.so
/system/lib/libffmpeg-miplayer.so
/system/lib/liblebodlna-jni.so
/system/lib/libnetutils.so
/system/lib/libnl.so
/system/lib/libplatinum-jni.so
/system/lib/libxiaomimediaplayer.so
/system/vendor/lib/libHCDNClientNet.so
/system/vendor/lib/libIOTCAPIs.so
/system/vendor/lib/libKey.so
/system/vendor/lib/libMiGallery.so
/system/vendor/lib/libUiManager.so
...
```

3.This example shows how to find so files which export 
`getaddrinfo` symbol on Android device. 

```sh
$ python sofinder.py -e getaddrinfo
/system/lib/libc.so
```
