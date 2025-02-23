# -*- encoding: utf-8 -*-
"""

.. include:: ../README.md
   :start-line: 1


"""
__author__ = 'bibi21000 aka Sébastien GALLET'
__email__ = 'bibi21000@gmail.com'

from cofferfile import EncryptFile, Cryptor, _open_t
from cofferfile import WRITE_BUFFER_SIZE, CHUNK_SIZE, READ, WRITE, APPEND, EXCLUSIVE # noqa F401
from cofferfile.decorator import reify

__all__ = ["NaclCryptor", "NaclFile", "open"]

class NaclFile(EncryptFile):
    """
    `naclfile.zstd`
    `naclfile.tar`
    """
    def __init__(self, filename=None, mode=None, fileobj=None,
            chunk_size=CHUNK_SIZE, write_buffer_size=WRITE_BUFFER_SIZE,
            secret_key=None
        ):
        """Constructor for the NaclFile class.

        At least one of fileobj and filename must be given a
        non-trivial value.

        The new class instance is based on fileobj, which can be a regular
        file, an io.BytesIO object, or any other object which simulates a file.
        It defaults to None, in which case filename is opened to provide
        a file object.

        When fileobj is not None, the filename argument is only used to be
        included in the gzip file header, which may include the original
        filename of the uncompressed file.  It defaults to the filename of
        fileobj, if discernible; otherwise, it defaults to the empty string,
        and in this case the original filename is not included in the header.

        The mode argument can be any of 'r', 'rb', 'a', 'ab', 'w', 'wb', 'x', or
        'xb' depending on whether the file will be read or written.  The default
        is the mode of fileobj if discernible; otherwise, the default is 'rb'.
        A mode of 'r' is equivalent to one of 'rb', and similarly for 'w' and
        'wb', 'a' and 'ab', and 'x' and 'xb'.

        The fernet_key argument is the Fernet key used to crypt/decrypt data.

        Encryption is done by chunks to reduce memory footprint. The default
        chunk_size is 64KB.
        """
        super().__init__(filename=filename, mode=mode, fileobj=fileobj,
            chunk_size=chunk_size, write_buffer_size=write_buffer_size,
            cryptor='nacl', secret_key=secret_key)

    def __repr__(self):
        """ """
        s = repr(self.myfileobj)
        return '<NaclFile ' + s[1:-1] + ' ' + hex(id(self)) + '>'

class NaclCryptor(Cryptor):

    @reify
    def _imp_nacl_secret(cls):
        """Lazy loader for nacl.secret"""
        import importlib
        return importlib.import_module('nacl.secret')

    @reify
    def _imp_nacl_utils(cls):
        """Lazy loader for nacl.utils"""
        import importlib
        return importlib.import_module('nacl.utils')

    @reify
    def _imp_nacl_pwhash_argon2i(cls):
        """Lazy loader for nacl.pwhash.argon2id"""
        import importlib
        return importlib.import_module('nacl.pwhash.argon2i')

    # ~ @reify
    # ~ def _imp_nacl_pwhash_scrypt(cls):
        # ~ """Lazy loader for nacl.pwhash.scrypt"""
        # ~ import importlib
        # ~ return importlib.import_module('nacl.pwhash.scrypt')

    def __init__(self, secret_key=None, **kwargs):
        """ """
        super().__init__(**kwargs)
        if secret_key is None:
            raise ValueError("Invalid secret_key: {!r}".format(secret_key))
        self.secret = self._imp_nacl_secret.SecretBox(secret_key)

    def derive(self, password, salt=None, key_len=64, ops=None, mem=None):
        """Derive a key from password (experimental)
        See https://pynacl.readthedocs.io/en/latest/password_hashing/#key-derivation
        """
        if salt is None:
            salt = self._imp_nacl_utils.random(self._imp_nacl_pwhash_argon2i.SALTBYTES)
        if ops is None:
            ops = self._imp_nacl_pwhash_argon2i.OPSLIMIT_SENSITIVE
        if mem is None:
            mem = self._imp_nacl_pwhash_argon2i.MEMLIMIT_SENSITIVE
        if isinstance(password, str):
            password = password.encode()
        return self._imp_nacl_pwhash_argon2i.kdf(key_len, password, salt,
                 opslimit=ops, memlimit=mem)

    # ~ def derive(self, password, salt=None, key_len=64, ops=None, mem=None):
        # ~ """Derive a key from password (experimental)
        # ~ See https://pynacl.readthedocs.io/en/latest/password_hashing/#key-derivation
        # ~ """
        # ~ if salt is None:
            # ~ salt = self._imp_nacl_utils.get_random_bytes(self._imp_nacl_pwhash_scrypt.SALTBYTES)
        # ~ if ops is None:
            # ~ ops = self._imp_nacl_pwhash_scrypt.OPSLIMIT_SENSITIVE
        # ~ if mem is None:
            # ~ mem = self._imp_nacl_pwhash_scrypt.MEMLIMIT_SENSITIVE
        # ~ return self._imp_nacl_pwhash_scrypt.kdf(key_len, password, salt,
                 # ~ opslimit=ops, memlimit=mem)

    def _decrypt(self, chunk):
        """ """
        return self.secret.decrypt(chunk)

    def _encrypt(self, chunk):
        """ """
        return self.secret.encrypt(chunk)

def open(filename, mode="rb", secret_key=None,
         encoding=None, errors=None, newline=None,
         chunk_size=CHUNK_SIZE):
    """Open an Nacl file in binary or text mode.

    The filename argument can be an actual filename (a str or bytes object), or
    an existing file object to read from or write to.

    The mode argument can be "r", "rb", "w", "wb", "x", "xb", "a" or "ab" for
    binary mode, or "rt", "wt", "xt" or "at" for text mode. The default mode is
    "rb".

    For binary mode, this function is equivalent to the NaclFile constructor:
    FernetFile(filename, mode, secret_key). In this case, the encoding, errors
    and newline arguments must not be provided.

    For text mode, a NaclFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).

    Encryption is done by chunks to reduce memory footprint. The default
    chunk_size is 64KB.
    """
    return _open_t(filename, mode=mode,
         encoding=encoding, errors=errors, newline=newline,
         chunk_size=chunk_size,
         cryptor='nacl', secret_key=secret_key)
