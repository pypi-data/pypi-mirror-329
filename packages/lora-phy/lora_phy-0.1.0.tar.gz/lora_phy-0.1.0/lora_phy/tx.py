import math

import numpy as np
from numpy.typing import NDArray

from .common import calc_checksum, calc_crc, calc_sym_num, chirp, dewhiten
from .errors import InvalidCodingRateError, InvalidInputError


class LoRaTransmitter:
    """LoRa PHY layer implementation.

    Parameters
    ----------
    spreading_factor : int
        Spreading factor.
    bandwidth : float
        LoRa bandwidth parameter.
    sample_rate : float
        Sampling rate of the signal.
    has_header : bool
        Whether the packet has a header (False for implicit header mode).
    coding_rate : int
        Coding rate (1:4/5 2:4/6 3:4/7 4:4/8).
    enable_crc : bool
        Whether to enable CRC checking.
    preamble_len : int
        Number of preamble chirps.
    """

    def __init__(
        self,
        spreading_factor: int,
        bandwidth: float,
        sample_rate: float,
        *,
        has_header: bool = True,
        coding_rate: int = 4,
        enable_crc: bool = True,
        preamble_len: int = 6,
    ):
        self._spreading_factor = spreading_factor
        self._bandwidth = bandwidth
        self._sample_rate = sample_rate
        self._has_header = has_header
        self._preamble_len = preamble_len
        self._down_chirp = chirp(
            False, self._spreading_factor, self._bandwidth, self._sample_rate)
        self._up_chirp = chirp(
            True, self._spreading_factor, self._bandwidth, self._sample_rate)
        self._coding_rate = coding_rate
        self._enable_crc = enable_crc
        # Low Data Rate Optimization: if the chirp period is larger than 16ms,
        # then the least significant two bits are considered unreliable.
        low_data_rate_optimization: bool = (
            2 ** self._spreading_factor / self._bandwidth > 16e-3)
        self._proc = TxProcessing(
            spreading_factor,
            low_data_rate_optimization=low_data_rate_optimization,
        )

    def modulate(self, symbols: NDArray[np.uint16], cfo: float = 0.0) -> NDArray[np.complex128]:
        """Modulate a baseband signal.

        Parameters
        ----------
        symbols : NDArray[np.uint16]
            A vector of chirp symbols to be modulated.
            Valit symbols are in the range [0, 2^spreading_factor).
        cfo : float, optional
            Starting carrier frequency offset, defaults to 0.0.

        Returns
        -------
        NDArray[np.complex128]
            A valid LoRa baseband signal.
        """
        def up_chirp_symbol(symbol: int) -> NDArray[np.complex128]:
            return chirp(
                True, self._spreading_factor,
                self._bandwidth, self._sample_rate,
                start_freq_offset=symbol, cfo=cfo
            )
        up_chirp = up_chirp_symbol(0)
        down_chirp = chirp(False, self._spreading_factor,
                           self._bandwidth, self._sample_rate, cfo=cfo)
        preamble = np.tile(up_chirp, self._preamble_len)
        netid = np.concatenate(
            (up_chirp_symbol(24), up_chirp_symbol(32)))
        chirp_len = len(up_chirp)
        sfd = np.tile(down_chirp, 3)[:round(chirp_len * 2.25)]
        data = np.empty(len(symbols) * chirp_len, dtype=np.complex64)
        for i, symbol in enumerate(symbols):
            data[i * chirp_len:(i + 1) * chirp_len] = up_chirp_symbol(symbol)
        return np.concatenate((preamble, netid, sfd, data))

    def encode(
        self,
        payload: NDArray[np.uint8],
    ) -> NDArray[np.uint16]:
        """Encode bytes to symbols.

        Parameters
        ----------
        payload : NDArray[np.uint8]
            The payload to encode into a LoRa packet.

        Returns
        -------
        NDArray[np.uint16]
            Encoded LoRa chirp symbols.

        Examples
        --------
        >>> LoRaTransmitter(8, 125e3, 250e3).encode(np.array([1], dtype=np.uint8))
        array([ 17, 125,  61, 237,  65, 197, 113,  57, 190, 161,  81,  41,  44,
                11, 246, 134], dtype=uint16)
        """
        # FIXME: all the concatenations are terrible
        orig_payload_len = len(payload)
        if self._enable_crc:
            crc = calc_crc(payload)
            payload = np.concatenate((payload, np.array(crc, dtype=np.uint8)))
        sym_num = calc_sym_num(
            self._has_header, orig_payload_len,
            4, self._enable_crc, self._spreading_factor,
            self._proc.low_data_rate_optimization
        )
        # Filling all symbols needs nibble_num nibbles
        nibble_num = self._spreading_factor - 2
        nibble_num += (sym_num - 8) \
            * (self._spreading_factor-2*self._proc.low_data_rate_optimization) \
            // (self._coding_rate + 4)
        additional = 255 * np.ones(
            math.ceil((nibble_num - len(payload) * 2) / 2), dtype=np.uint8)
        payload = np.concatenate((payload, additional))
        # This is whiten, but using the same function
        dewhiten(payload[:orig_payload_len])
        data_nibbles = np.zeros(nibble_num, dtype=np.uint8)
        for i in range(nibble_num//2):
            data_nibbles[i*2] = payload[i] & 0xf
            data_nibbles[i*2+1] = payload[i] >> 4
        if self._has_header:
            header_nibbles = self._gen_header(
                orig_payload_len, self._coding_rate, self._enable_crc)
        else:
            header_nibbles = np.empty(0, dtype=np.uint8)
        nibbles = np.concatenate((header_nibbles, data_nibbles))
        codewords = self._proc.hamming_encode(nibbles, self._coding_rate)
        # Interleave
        # First SF-2 symbols use CR 4/8 (original comment wrong)
        symbols_i = diag_interleave(
            codewords[:self._spreading_factor - 2], 4 + 4)
        ppm = self._spreading_factor - 2 * self._proc.low_data_rate_optimization
        rdd = self._coding_rate + 4
        for i in range(self._spreading_factor - 2, len(codewords) - ppm + 1, ppm):
            symbols_i = np.concatenate(
                (symbols_i, diag_interleave(codewords[i:i + ppm], rdd)))
        symbols = self._proc.gray_decoding(symbols_i)
        return symbols

    @classmethod
    def _gen_header(cls, payload_len: int, cr: int, crc: bool) -> NDArray[np.uint8]:
        """Generate a valid LoRa header.

        Parameters
        ----------
        payload_len : int
            Payload length.
        cr : int
            Coding rate.
        crc : bool
            Whether CRC is enabled.

        Returns
        -------
        NDArray[np.uint8]
            The header in nibbles.

        Examples
        --------
        >>> LoRaTransmitter._gen_header(254, 2, True)
        array([15, 14,  5,  0,  8], dtype=uint8)
        """
        header_nibbles = np.empty(5, dtype=np.uint8)
        header_nibbles[0] = payload_len >> 4
        header_nibbles[1] = payload_len & 0xf
        header_nibbles[2] = (cr << 1) | int(crc)
        # Calculate checksum
        data = np.unpackbits(
            header_nibbles[:3].reshape(-1, 1), axis=1)[:, -4:].flatten()
        csum = calc_checksum(data)
        header_nibbles[3] = csum[0]
        header_nibbles[4] = csum[1] << 3 | csum[2] << 2 | csum[3] << 1 | csum[4]
        return header_nibbles

    def time_in_air(self, payload_len: int) -> float:
        """Calculate the time on air for a LoRa packet.

        Parameters
        ----------
        payload_len : int
            The payload length.

        Returns
        -------
        float
            The time on air in milliseconds.

        Examples
        --------
        >>> LoRaTransmitter(8, 125e3, 250e3).time_in_air(10)
        86.528
        """
        sym_num = calc_sym_num(
            self._has_header, payload_len,
            self._coding_rate, self._enable_crc,
            self._spreading_factor, self._proc.low_data_rate_optimization
        )
        tmp = (self._preamble_len + 4.25 + sym_num) * \
            1e3 * (1 << self._spreading_factor)
        return tmp / self._bandwidth


def xorbits8(data: NDArray[np.uint8], mask: int) -> NDArray[np.uint8]:
    """XOR bits in an 8-bit integer with a mask.

    See `xorbits16` for more details.
    """
    new = (data & mask).astype(np.uint8)
    bits = np.unpackbits(new).reshape(-1, 8)
    result: NDArray[np.uint8] = np.bitwise_xor.reduce(bits, axis=1)
    return result


def diag_interleave(codewords: NDArray[np.uint16], rdd: int) -> NDArray[np.uint16]:
    """Diagonal interleaving.

    Parameters
    ----------
    codewords : NDArray[np.uint16]
        Data in nibbles.
    rdd : int
        Number of redundant bits (see `LoRaPHY.decode`).

    Returns
    -------
    symbols : NDArray[np.uint16]
        Symbols after diagonal interleaving.

    Examples
    --------
    >>> diag_interleave(np.arange(10, dtype=np.uint16), 5)
    array([682, 102,  60,  96,   0], dtype=uint16)
    """
    # This is another piece of MATLAB magic, but largely similar to
    # `diag_deinterleave`
    # `tmp` is a matrix of `rdd` columns; each row contains the bits of
    # the corresponding element of `codewords` 'right-msb'
    # tmp = de2bi(codewords, rdd, 'right-msb')
    # The arrayfun takes the `x`th column, circular downshift by (1-x)
    # `x` is `x-1` in C-style indexing, so we upshift by the index
    # @(x) circshift(tmp(:,x), 1-x)
    # This is again repeated for all columns and transposed
    # cell2mat(arrayfun(_, 1:rdd, 'un', 0))'
    # Since now we need to muddle between the bits of different elements,
    # we actually have to do this the MATLAB way
    # Since the maximum `rdd` is 8, we can change the type to uint8
    # to allow getting a 'right-msb' unpacking with `bitorder="little"`
    if np.any(codewords >= 1 << rdd):
        raise InvalidInputError("Codewords contain more than rdd bits")
    codewords_trimmed = codewords.astype(np.uint8)
    bits = np.unpackbits(
        codewords_trimmed, bitorder="little").reshape(-1, 8)
    # circular upshift by column index from right
    for col in range(rdd):
        bits[:, col] = np.roll(bits[:, col], -col)
    # Now transpose and pack the bits back, discarding unused trailing
    # columns (now rows)
    bits = bits.transpose()[:rdd]
    bitweights = 1 << np.arange(len(codewords), dtype=np.uint16)
    symbols: NDArray[np.uint16] = bits.dot(bitweights)
    return symbols


class TxProcessing:
    """Various data processing functions for LoRaTransmitter."""

    def __init__(
        self,
        spreading_factor: int,
        low_data_rate_optimization: bool,
    ):
        self.spreading_factor = spreading_factor
        self.low_data_rate_optimization = low_data_rate_optimization

    def gray_decoding(self, symbols: NDArray[np.uint16]) -> NDArray[np.uint16]:
        """Gray decoding (used in the encoding process).

        Parameters
        ----------
        symbols : NDArray[np.uint16]
            Interleaved symbols.

        Returns
        -------
        NDArray[np.uint16]
            Symbols after gray decoding to be modulated.

        Examples
        --------
        >>> proc = TxProcessing(7, False)
        >>> proc.gray_decoding(np.arange(0, 256, 19, dtype=np.uint16))
        array([  1, 117, 109,  57,  93,  41, 113, 101, 112,  78,  85,  31,  57,
                38], dtype=uint16)
        """
        result = np.empty_like(symbols, dtype=np.uint16)
        for i, v in enumerate(symbols):
            mask = v >> 1
            while mask:
                v ^= mask
                mask >>= 1
            if i < 8 or self.low_data_rate_optimization:
                result[i] = ((v << 2) + 1) & ((1 << self.spreading_factor) - 1)
            else:
                result[i] = (v + 1) & ((1 << self.spreading_factor) - 1)
        return result

    def hamming_encode(self, nibbles: NDArray[np.uint8], cr: int) -> NDArray[np.uint16]:
        """Hamming encoding.

        Parameters
        ----------
        nibbles : NDArray[np.uint8]
            Nibbles to encode.
        cr : int
            Coding rate (See `LoRaPHY`).

        Returns
        -------
        codewords : NDArray[np.uint16]
            Encoded codewords.

        Examples
        --------
        >>> proc = TxProcessing(9, False)
        >>> proc.hamming_encode(np.arange(10, dtype=np.uint8), 2)
        array([  0, 209, 114, 163, 180, 101, 198,  23,  40,  57], dtype=uint16)
        """
        # The original MATLAB code uses a function `word_reduce`.
        # It is just a normal reduce operation.
        # I am precomputing the multiplied values for readability
        p1 = xorbits8(nibbles, 0b00001101) << 7  # 1,3,4
        p2 = xorbits8(nibbles, 0b00001011) << 6  # 1,2,4
        p3 = xorbits8(nibbles, 0b00000111) << 4  # 1,2,3
        p4 = xorbits8(nibbles, 0b00001111) << 4  # 1,2,3,4
        p5 = xorbits8(nibbles, 0b00001110) << 5  # 2,3,4
        codewords = np.zeros(len(nibbles), dtype=np.uint16)
        for i, nibble in enumerate(nibbles):
            # The first SF-2 nibbles use CR=4/8
            crnow = 4 if i < self.spreading_factor - 2 else cr
            if crnow == 1:
                codewords[i] = nibble | p4[i]
            elif crnow == 2:
                codewords[i] = nibble | p3[i] | p5[i]
            elif crnow == 3:
                codewords[i] = nibble | p2[i] | p3[i] | p5[i]
            elif crnow == 4:
                codewords[i] = nibble | p1[i] | p2[i] | p3[i] | p5[i]
            else:
                raise InvalidCodingRateError()
        return codewords
