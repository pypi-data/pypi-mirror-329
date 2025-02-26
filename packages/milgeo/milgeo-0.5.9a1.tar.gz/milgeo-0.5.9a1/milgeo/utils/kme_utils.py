from typing import IO
import io
import random
import struct
import sys
from hashlib import sha256
from pathlib import Path
from tkinter import filedialog, simpledialog
from zipfile import ZipFile

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


KME_MAGIC = b"KME\xfc"
KME_SALT = b"GhfMWz,<v|KRuQ1b@P51"
HASH_COUNT = 100000
ERROR_UNSUPPORTED_FILE_VERSION = "Unsupported KME file version: %d"
ERROR_INVALID_PASSWORD = "Password is invalid!"
AES_STREAM_MIN_DATA_SIZE = 1024

MAX_BUFFER_SIZE = 2**16


def is_kme_file(file: IO[bytes]) -> bool:
    file.seek(0)
    signature = file.read(len(KME_MAGIC))
    file.seek(0)
    return signature == KME_MAGIC


def _unpack_int(buf) -> int:
    return struct.unpack("<i", buf)[0]


def _pack_int(num: int) -> bytes:
    return struct.pack("<i", num)


def _preview(buffer, crc_bytes=2, print_bytes=16):
    crc_format_str = f"0{crc_bytes*2}x"
    crc = sum(buffer[:print_bytes]) % (256**crc_bytes)
    return f"{buffer[:print_bytes].hex()} (len={len(buffer)} CRC={format(crc, crc_format_str)})"


class CipherBufferStream:
    BUFFER_MAGIC = 0x4F681AB7

    def __init__(self, cipher_stream, raw_stream, min_data_size):
        self.cipher_stream = cipher_stream
        self.raw_stream = raw_stream
        self.is_first_chunk = True
        self.min_data_size = min_data_size
        self.buf_avail = 0
        self.buffer = bytearray(MAX_BUFFER_SIZE)
        self.buf_pos = 0

    @staticmethod
    def xor_buffer(buffer, count):
        for i in range(count // 2):
            buffer[i] ^= buffer[count - i - 1]

    def read(self, count: int = sys.maxsize):
        result = b""
        while count > 0:
            if self.buf_avail == 0:
                if self.is_first_chunk:
                    self.buf_avail = (
                        _unpack_int(self.raw_stream.read(4)) ^ self.BUFFER_MAGIC
                    )
                    if self.buf_avail < 0 or self.buf_avail > len(self.buffer):
                        return result
                    buf = self.cipher_stream.read(self.buf_avail)
                    self.buffer[: len(buf)] = buf
                    self.xor_buffer(self.buffer, self.buf_avail)
                    self.is_first_chunk = False
                else:
                    buf = self.cipher_stream.read(MAX_BUFFER_SIZE)
                    if len(buf) == 0:
                        return result
                    self.buf_avail = len(buf)
                    self.buffer[: len(buf)] = buf
                self.buf_pos = 0
            length = min(count, self.buf_avail)
            result += self.buffer[self.buf_pos : self.buf_pos + length]
            self.buf_pos += length
            self.buf_avail -= length
            count -= length
        return result

    def write(self, buffer):
        input_cursor = 0
        while input_cursor < len(buffer):
            if self.buf_avail == len(self.buffer):
                self.flush()
            input_left = len(buffer) - input_cursor
            available = len(self.buffer) - self.buf_avail
            length = min(input_left, available)
            self.buffer[self.buf_avail : self.buf_avail + length] = buffer[
                input_cursor : input_cursor + length
            ]
            self.buf_avail += length
            input_cursor += length

    def flush(self):
        if self.is_first_chunk and self.buf_avail < self.min_data_size:
            padding_cursor = self.min_data_size
        else:
            padding_cursor = (self.buf_avail + 15) // 16 * 16

        if self.buf_avail < padding_cursor:
            self.buffer[self.buf_avail : padding_cursor] = random.randbytes(
                padding_cursor - self.buf_avail
            )
            self.buf_avail = padding_cursor

        if self.is_first_chunk:
            num = self.buf_avail ^ self.BUFFER_MAGIC
            self.raw_stream.write(_pack_int(num))
            self.xor_buffer(self.buffer, self.buf_avail)
            self.is_first_chunk = False

        if self.buf_avail > 0:
            self.cipher_stream.write(self.buffer[: self.buf_avail])

        self.buf_avail = 0


class CipherStream:
    MAX_CHUNK_SIZE = 2**13

    def __init__(self, core_stream, cipher):
        self.cipher = cipher
        self.core_stream = core_stream

    def read(self, count: int = sys.maxsize):
        result = b""
        if count == 0:
            return result
        while True:
            chunk_size = min(count, self.MAX_CHUNK_SIZE)
            count -= chunk_size
            chunk = self.core_stream.read(chunk_size)
            if len(chunk) == 0:
                break
            chunk = self.cipher.decrypt(chunk)
            result += chunk
            if count == 0 or chunk_size != len(chunk):
                break
        return result

    def write(self, chunk: bytes):
        self.core_stream.write(self.cipher.encrypt(chunk))


def make_default_iv(key: bytes) -> bytes:
    return AES.new(key, AES.MODE_ECB).encrypt(bytes(AES.block_size))


def _create_aes_stream(stream: io.BufferedReader, password: bytes):
    key = SHA256.new(password).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv=make_default_iv(key))
    cs = CipherStream(stream, cipher)
    return CipherBufferStream(cs, stream, AES_STREAM_MIN_DATA_SIZE)


def _prepare_password_hash(kme_password: str, salt: bytes):
    total_password = kme_password.encode("utf-8") + salt
    if not total_password:
        return total_password
    hash_cnt = HASH_COUNT if len(kme_password) < 20 else HASH_COUNT // 10

    dig_len = sha256().digest_size
    digest = bytearray(dig_len)
    for i in range(1, hash_cnt + 1):
        h = sha256()
        h.update(i.to_bytes(4, "little"))
        h.update(digest)
        h.update(total_password)
        digest = h.digest()
    return bytes(digest)


class InvalidPasswordException(ValueError):
    pass


def import_kme_stream(kme_password: str, kme_input_stream: io.BufferedReader):
    kme_magic_buf = kme_input_stream.read(len(KME_MAGIC))
    # Checking zip signature (4 bytes)
    if kme_magic_buf != KME_MAGIC:
        kme_input_stream.seek(-len(kme_magic_buf), io.SEEK_CUR)
        raise ValueError("Not a KME file.")
    password = _prepare_password_hash(kme_password, KME_SALT)

    # Checking Version (4 bytes) == 1
    version = _unpack_int(kme_input_stream.read(4))
    if version != 1:
        raise IOError(ERROR_UNSUPPORTED_FILE_VERSION % version)

    cs = _create_aes_stream(kme_input_stream, password)

    length = AES_STREAM_MIN_DATA_SIZE
    buf = cs.read(length)
    if buf[4:6] != b"PK":
        raise InvalidPasswordException(ERROR_INVALID_PASSWORD)

    data_size = _unpack_int(buf[:4])
    length -= 4
    if data_size < length:
        length = data_size

    yield buf[4 : length + 4]
    data_size -= length
    if data_size > 0:
        yield cs.read(data_size)


def read_kme(kme_password: str, kme_input_stream: io.BufferedReader):
    """
    Read KME file and return its content as bytes. Probably it will contain KMZ file.
    """
    return b"".join(import_kme_stream(kme_password, kme_input_stream))


def export_kme_stream(password: str, kmz_input_stream, kme_output_stream):
    kme_output_stream.write(KME_MAGIC + _pack_int(1))
    key = _prepare_password_hash(password, KME_SALT)
    cipher_stream = _create_aes_stream(kme_output_stream, key)

    plaintext = kmz_input_stream.read()
    cipher_stream.write(_pack_int(len(plaintext)))
    cipher_stream.write(plaintext)
    cipher_stream.flush()


def write_kml_as_kme(kml_str: str, password: str, output_stream):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'a') as zip_file:
        zip_file.writestr('main.kml', kml_str)
    
    zip_buffer.seek(0)
    export_kme_stream(password, zip_buffer, output_stream)

def read_kme_as_kml(kme_password: str, kme_input_stream: io.BufferedReader):
    kmz_content = read_kme(kme_password, kme_input_stream)
    kmz = ZipFile(io.BytesIO(kmz_content))
    inner_kml = next(info.filename for info in kmz.filelist if info.filename.endswith('.kml'))
    return kmz.read(inner_kml)

if __name__ == "__main__":
    input_file = Path(
        filedialog.askopenfilename(
            filetypes=(("KME (encrypted)", "*.kme"), ("KML (plaintext)", "*.kml"))
        )
    )
    password = simpledialog.askstring("KME Password", "Password:")
    if password is None:
        exit()

    match input_file.suffix:
        case ".kml":
            zip_buffer = io.BytesIO()
            with open(input_file, "rb") as fi:
                with ZipFile(zip_buffer, "a") as zip_file:
                    zip_file.writestr("main.kml", fi.read())
            print("ZIP buffer:", _preview(zip_buffer.getvalue()))

            zip_buffer.seek(0)
            output_file = input_file.with_suffix(".kme")
            with open(output_file, "wb") as fo:
                export_kme_stream(password, zip_buffer, fo)

        case ".kme":
            with open(input_file, "rb") as fi:
                kmz_content = b"".join(import_kme_stream(password, fi))

            print("Decrypted KMZ:", _preview(kmz_content))
            with open(input_file.with_suffix(".kmz"), "wb") as kmz_file:
                kmz_file.write(kmz_content)

            kmz = ZipFile(io.BytesIO(kmz_content))
            inner_kml = next(info.filename for info in kmz.filelist if info.filename.endswith('.kml'))

            output_file = input_file.with_suffix(".kml")
            with open(output_file, "wb") as ofile:
                ofile.write(kmz.read(inner_kml))
