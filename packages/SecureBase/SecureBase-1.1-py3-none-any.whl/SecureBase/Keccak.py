class Keccak:
    _KECCAK_ROUNDS = 24
    _ROUND_CONSTANTS = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    _RHO_OFFSETS = [
        0, 1, 62, 28, 27,
        36, 44, 6, 55, 20,
        3, 10, 43, 25, 39,
        41, 45, 15, 21, 8,
        18, 2, 61, 56, 14
    ]

    def __init__(self):
        self._disposed = False
        self._state = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    def hash(self, input_data, output_length_bits):
        """
        Keccak hash fonksiyonu

        Args:
            input_data (bytes): Hashlenecek veri
            output_length_bits (int): Çıktı uzunluğu (bit olarak)

        Returns:
            bytes: Hash değeri
        """
        if self._disposed:
            raise ValueError("Object is disposed")

        self._initialize_state()

        rate_in_bytes = (1600 - 2 * output_length_bits) // 8
        padded_message = self._pad(input_data, rate_in_bytes)
        self._absorb(padded_message, rate_in_bytes)
        return self._squeeze(output_length_bits // 8)

    def _initialize_state(self):
        self._state = [0] * 25

    def _absorb(self, message, rate_in_bytes):
        block_size = rate_in_bytes
        for offset in range(0, len(message), block_size):
            for i in range(block_size // 8):
                if offset + (i + 1) * 8 <= len(message):
                    # Python'da int.from_bytes kullanarak byte'ları 64-bit tamsayıya dönüştürme
                    value = int.from_bytes(message[offset + i * 8:offset + (i + 1) * 8], byteorder='little')
                    self._state[i] ^= value
            self._keccak_f()

    def _squeeze(self, output_length):
        output = bytearray()
        remaining = output_length

        while remaining > 0:
            bytes_to_output = min(remaining, 200)

            # State'den byte'lara dönüştürme
            for i in range((bytes_to_output + 7) // 8):
                if i < len(self._state):
                    value = self._state[i]
                    for j in range(min(8, bytes_to_output - i * 8)):
                        if i * 8 + j < bytes_to_output:
                            output.append((value >> (j * 8)) & 0xFF)

            remaining -= bytes_to_output

            if remaining > 0:
                self._keccak_f()

        return bytes(output[:output_length])

    def _keccak_f(self):
        for round_idx in range(self._KECCAK_ROUNDS):
            # Theta step
            C = [0] * 5
            for i in range(5):
                C[i] = self._state[i] ^ self._state[i + 5] ^ self._state[i + 10] ^ self._state[i + 15] ^ self._state[
                    i + 20]

            D = [0] * 5
            for i in range(5):
                D[i] = C[(i + 4) % 5] ^ self._rol(C[(i + 1) % 5], 1)

            for i in range(0, 25, 5):
                for j in range(5):
                    self._state[i + j] ^= D[j]

            # Rho and Pi steps
            B = [0] * 25
            for i in range(25):
                B[i] = self._rol(self._state[i], self._RHO_OFFSETS[i])

            # Chi step
            for i in range(0, 25, 5):
                for j in range(5):
                    self._state[i + j] = B[i + j] ^ (~B[i + ((j + 1) % 5)] & B[i + ((j + 2) % 5)])

            # Iota step
            self._state[0] ^= self._ROUND_CONSTANTS[round_idx]

    @staticmethod
    def _rol(x, n):
        """64-bit rotasyonu (sola döndürme)"""
        # Python'da 64-bit sınır kontrolü
        x &= 0xFFFFFFFFFFFFFFFF
        return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

    @staticmethod
    def _pad(input_data, rate_in_bytes):
        """Keccak padding"""
        input_len = len(input_data)
        padding_len = rate_in_bytes - (input_len % rate_in_bytes)

        # Padding oluşturma
        padded = bytearray(input_data)
        padded.append(0x06)  # ilk padding byte'ı
        padded.extend([0x00] * (padding_len - 2))  # orta kısım
        padded.append(0x80)  # son padding byte'ı

        return bytes(padded)

    def dispose(self):
        """Kaynakları temizle"""
        if not self._disposed:
            self._state = None
            self._disposed = True

# Kullanım örneği:
# with Keccak() as keccak:
#     hash_value = keccak.hash(b"Test message", 256)
#     print(hash_value.hex())