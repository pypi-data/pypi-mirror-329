[![CircleCI](https://dl.circleci.com/status-badge/img/gh/bibi21000/NaclFile/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/bibi21000/NaclFile/tree/main)
[![codecov](https://codecov.io/gh/bibi21000/NaclFile/graph/badge.svg?token=4124GIOJAK)](https://codecov.io/gh/bibi21000/NaclFile)
![PyPI - Downloads](https://img.shields.io/pypi/dm/naclfile)

# NaclFile

A python xxxFile like (ie TarFile, GzipFile, BZ2File, pyzstd.ZstdFile, ...)
for encrypting files with PyNacl SecretBox.

This project is part of the CofferFile : https://github.com/bibi21000/CofferFile.

If you're looking for a more powerfull storage for your sensible datas,
look at PyCoffer : https://github.com/bibi21000/PyCoffer.

## Install

```
    pip install naclfile
```

## Create your encryption key

```
    from nacl import utils

    key = utils.random(SecretBox.KEY_SIZE)
```
and store it in a safe place (disk, database, ...).

This key is essential to encrypt and decrypt data.
Losing this key means losing the data.

## "open" your encrypted files like normal files

Text files :

```
    from naclfile import open as nacl_open

    with nacl_open('test.nacl', mode='wt', secret_key=key, encoding="utf-8") as ff:
        ff.write(data)

    with nacl_open('test.nacl', "rt", secret_key=key, encoding="utf-8") as ff:
        data = ff.read()

    with nacl_open('test.nacl', mode='wt', secret_key=key, encoding="utf-8") as ff:
        ff.writelines(data)

    with nacl_open('test.nacl', "rt", secret_key=key, encoding="utf-8") as ff:
        data = ff.readlines()
```

Binary files :

```

    with nacl_open('test.nacl', mode='wb', secret_key=key) as ff:
        ff.write(data)

    with nacl_open('test.nacl', "rb", secret_key=key) as ff:
        data = ff.read()
```

## Crypt and compress ... for better performances.

Look at https://github.com/bibi21000/CofferFile/blob/main/BENCHMARK.md.

```
    from naclfile.zstd import open as nacl_open

    with nacl_open('test.nacz', mode='wb', secret_key=key) as ff:
        ff.write(data)

    with nacl_open('test.nacz', "rb", secret_key=key) as ff:
        data = ff.read()
```

## Crypt and compress your tar files

```
    from naclfile.tar import open as tar_open

    with tar_open('test.tarcz', mode='w', secret_key=key) as ff:
        ff.add(file1,'file1.data')
        ff.add(file2,'file2.data')

    with tar_open('test.tarcz', "r", secret_key=key) as ff:
        ff.extractall()
```

Look at documentation : https://bibi21000.github.io/NaclFile/
