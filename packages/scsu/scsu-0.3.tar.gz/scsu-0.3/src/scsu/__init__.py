from codecs import Codec, CodecInfo, StreamReader, StreamWriter, register

from .codecs.encoder import SCSUIncrementalEncoder, SignedSCSUIncrementalEncoder
from .codecs.decoder import SCSUIncrementalDecoder, SignedSCSUIncrementalDecoder
from .codecs.info import CODEC_NAME, ENCODING_NAME, SIGNATURE_SUFFIX


class SCSUCodec(Codec):
    add_signature = False

    def encode(self, s, errors="strict"):
        encoder = SignedSCSUIncrementalEncoder(errors) if self.add_signature else SCSUIncrementalEncoder(errors)
        return encoder.encode(s, True), len(s)

    def decode(self, s, errors="strict"):
        decoder = SignedSCSUIncrementalDecoder(errors) if self.add_signature else SCSUIncrementalDecoder(errors)
        return decoder.decode(s, True), len(s)


class SCSUStreamReader(SCSUCodec, StreamReader):
    pass


class SCSUStreamWriter(SCSUCodec, StreamWriter):
    pass


class SignedSCSUCodec(SCSUCodec):
    add_signature = True


class SignedSCSUStreamReader(SignedSCSUCodec, StreamReader):
    pass


class SignedSCSUStreamWriter(SignedSCSUCodec, StreamWriter):
    pass


def scsu_search_function(encoding_name: str):
    if encoding_name[:len(CODEC_NAME)].casefold() == CODEC_NAME.casefold():
        if encoding_name[len(CODEC_NAME):].casefold() == SIGNATURE_SUFFIX.casefold():
            return CodecInfo(name=ENCODING_NAME + SIGNATURE_SUFFIX,
                             encode=SignedSCSUCodec().encode,
                             decode=SignedSCSUCodec().decode,
                             streamreader=SignedSCSUStreamReader,
                             streamwriter=SignedSCSUStreamWriter,
                             incrementalencoder=SignedSCSUIncrementalEncoder,
                             incrementaldecoder=SignedSCSUIncrementalDecoder)
        else:
            return CodecInfo(name=ENCODING_NAME,
                             encode=SCSUCodec().encode,
                             decode=SCSUCodec().decode,
                             streamreader=SCSUStreamReader,
                             streamwriter=SCSUStreamWriter,
                             incrementalencoder=SCSUIncrementalEncoder,
                             incrementaldecoder=SCSUIncrementalDecoder)

    return None


register(scsu_search_function)
