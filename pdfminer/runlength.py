#
# RunLength decoder (Adobe version) implementation based on PDF Reference
# version 1.4 section 3.3.4.
#
#  * public domain *
#


def rldecode(data: bytes) -> bytes:
    """
    RunLength decoder (Adobe version) implementation based on PDF Reference
    version 1.4 section 3.3.4:
        The RunLengthDecode filter decodes data that has been encoded in a
        simple byte-oriented format based on run length. The encoded data
        is a sequence of runs, where each run consists of a length byte
        followed by 1 to 128 bytes of data. If the length byte is in the
        range 0 to 127, the following length + 1 (1 to 128) bytes are
        copied literally during decompression. If length is in the range
        129 to 255, the following single byte is to be copied 257 - length
        (2 to 128) times during decompression. A length value of 128
        denotes EOD.
    """
    decoded = bytearray()
    i = 0
    while i < len(data):
        length = data[i]
        if length == 128:
            break

        if length >= 0 and length < 128:
            end = i + length + 2
            if end > len(data):
                raise IndexError('RunLength literal run exceeds input')
            decoded.extend(data[i+1:end])
            i = end

        if length > 128:
            if i + 1 >= len(data):
                raise IndexError('RunLength repeat run exceeds input')
            run = bytes((data[i+1],))*(257-length)
            decoded.extend(run)
            i = (i+1) + 1

    return bytes(decoded)
