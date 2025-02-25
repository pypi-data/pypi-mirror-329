# -*- encoding: utf-8 -*-
""" TarFile interface.

"""
__author__ = 'bibi21000 aka Sébastien GALLET'
__email__ = 'bibi21000@gmail.com'

import tarfile

from cofferfile import _open_cls
from . import CHUNK_SIZE, READ, WRITE, APPEND, EXCLUSIVE # noqa F401
from .zstd import NaclFile as ZstdNaclFile


class TarFile(tarfile.TarFile):
    """Based on TarFfile with encryption"""

    def __init__(self, name, mode='r', fileobj=None, secret_key=None, **kwargs):
        """Init the TarZstdNaclFile"""
        level_or_option = kwargs.pop('level_or_option', None)
        zstd_dict = kwargs.pop('zstd_dict', None)
        chunk_size = kwargs.pop('chunk_size', CHUNK_SIZE)
        kwargs.pop('cryptor', None)
        self.nacl_file = ZstdNaclFile(name, mode, fileobj=fileobj,
            secret_key=secret_key, level_or_option=level_or_option,
                zstd_dict=zstd_dict, chunk_size=chunk_size, **kwargs)
        try:
            super().__init__(fileobj=self.nacl_file, mode=mode.replace('b', ''), **kwargs)

        except Exception:
            self.nacl_file.close()
            raise

    def close(self):
        """Close the TarZstdNaclFile"""
        try:
            super().close()

        finally:
            if self.nacl_file is not None:
                self.nacl_file.close()

    def __repr__(self):
        """ """
        s = repr(self.nacl_file)
        return '<TarZstdNacl ' + s[1:-1] + ' ' + hex(id(self)) + '>'

def open(filename, mode="rb", secret_key=None,
        chunk_size=CHUNK_SIZE,
        level_or_option=None, zstd_dict=None,
        **cryptor_args):
    """Open a file in binary or text mode.

    The filename argument can be an actual filename (a str or bytes object), or
    an existing file object to read from or write to.

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab" for
    binary mode.

    """
    return _open_cls(filename, mode=mode,
        chunk_size=chunk_size, secret_key=secret_key,
        coffer_cls = TarFile,
        level_or_option=level_or_option, zstd_dict=zstd_dict,
        cryptor='nacl', **cryptor_args)
