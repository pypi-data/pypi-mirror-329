import enum

from SecureBase.Keccak import Keccak


class SBEncoding(enum.Enum):
    UNICODE = 1
    UTF8 = 2


class SecureBase:
    _DEF_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#&'()*,-.:;<>?@[]\\^_{}|~/+="
    _BASE64_STANDART = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def __init__(self, encoding, secret_key=None):
        self._global_charset = ""
        self._padding = ''
        self._disposed = False
        self._g_encoding = encoding

        if secret_key is None:
            self._global_charset = self._BASE64_STANDART
            self._padding = '='
        else:
            self.set_secret_key(secret_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    def set_secret_key(self, secret_key):
        if len(secret_key) != 0:
            self._global_charset = self._DEF_CHARSET
            self._pr_suffle_charset(secret_key)
            self._padding = self._global_charset[64]
            self._global_charset = self._global_charset[:64]
        else:
            self._global_charset = self._BASE64_STANDART
            self._padding = '='

    def encode(self, input_str):
        if self._g_encoding == SBEncoding.UNICODE:
            input_bytes = input_str.encode('utf-16-le')
            encoded_bytes = self._process_encoding(input_bytes)
            return encoded_bytes.decode('utf-16-le')
        else:
            input_bytes = input_str.encode('utf-8')
            encoded_bytes = self._process_encoding(input_bytes)
            return encoded_bytes.decode('utf-8')

    def decode(self, input_str):
        if self._g_encoding == SBEncoding.UNICODE:
            decoded_bytes = self._process_decoding(input_str)
            return decoded_bytes.decode('utf-16-le')
        else:
            decoded_bytes = self._process_decoding(input_str)
            return decoded_bytes.decode('utf-8')

    def _process_encoding(self, input_bytes):
        try:
            base_array = list(self._global_charset)
            pdata = input_bytes
            encoded_data = []

            if len(pdata) > 0:
                length = len(pdata)
                length_div3 = length // 3
                remainder = length % 3
                encoded_length = (length_div3 * 4) + (0 if remainder == 0 else 4)
                encoded_data = [''] * encoded_length

                data_index = 0
                encoded_index = 0

                for i in range(length_div3):
                    chunk = (pdata[data_index] << 16) | (pdata[data_index + 1] << 8) | pdata[data_index + 2]
                    data_index += 3

                    encoded_data[encoded_index] = base_array[(chunk >> 18) & 63]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[(chunk >> 12) & 63]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[(chunk >> 6) & 63]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[chunk & 63]
                    encoded_index += 1

                if remainder == 1:
                    last_byte = pdata[data_index]
                    encoded_data[encoded_index] = base_array[last_byte >> 2]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[((last_byte & 3) << 4)]
                    encoded_index += 1
                    encoded_data[encoded_index] = self._padding
                    encoded_index += 1
                    encoded_data[encoded_index] = self._padding
                elif remainder == 2:
                    second_last_byte = pdata[data_index]
                    data_index += 1
                    last_byte = pdata[data_index]

                    encoded_data[encoded_index] = base_array[second_last_byte >> 2]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[((second_last_byte & 3) << 4) | (last_byte >> 4)]
                    encoded_index += 1
                    encoded_data[encoded_index] = base_array[(last_byte & 15) << 2]
                    encoded_index += 1
                    encoded_data[encoded_index] = self._padding

            encoded_str = ''.join(encoded_data)
            if self._g_encoding == SBEncoding.UNICODE:
                return encoded_str.encode('utf-16-le')
            else:
                return encoded_str.encode('utf-8')

        except Exception as e:
            raise Exception("Invalid data or secret key!")

    def _process_decoding(self, input_str):
        try:
            base_array = list(self._global_charset)
            decoded_data = bytearray()

            if len(input_str) > 0:
                base64_values = [0] * 256
                for i in range(64):
                    base64_values[ord(base_array[i])] = i

                length = len(input_str)
                padding_count = 0

                if length > 0 and input_str[length - 1] == self._padding:
                    padding_count += 1
                if length > 1 and input_str[length - 2] == self._padding:
                    padding_count += 1

                decoded_length = (length * 3) // 4 - padding_count
                decoded_data = bytearray(decoded_length)

                encoded_index = 0
                decoded_index = 0

                while encoded_index < length:
                    chunk = (base64_values[ord(input_str[encoded_index])] << 18) | \
                            (base64_values[ord(input_str[encoded_index + 1])] << 12) | \
                            (base64_values[ord(input_str[encoded_index + 2])] << 6) | \
                            base64_values[ord(input_str[encoded_index + 3])]
                    encoded_index += 4
                    decoded_data[decoded_index] = (chunk >> 16) & 255
                    decoded_index += 1

                    if decoded_index < decoded_length:
                        decoded_data[decoded_index] = (chunk >> 8) & 255
                        decoded_index += 1

                    if decoded_index < decoded_length:
                        decoded_data[decoded_index] = chunk & 255
                        decoded_index += 1

            return bytes(decoded_data)

        except Exception as ex:
            raise Exception(str(ex))

    def _pr_suffle_charset(self, secret_key):
        self._compute_hash(secret_key, 256)
        secret_hash = self._compute_hash(secret_key, 512)
        self._global_charset = self._fn_suffle_charset(
            self._global_charset,
            self._fn_character_set_secret_key(secret_hash)
        )

    def _compute_hash(self, s, key):
        with Keccak() as keccak:
            input_bytes = s.encode('utf-8')
            hash_value = keccak.hash(input_bytes, key)
            hex_hash = hash_value.hex()

        return hex_hash

    def _fn_suffle_charset(self, data, keys):
        karakterler = list(data)
        key_len = len(keys)
        for j in range(key_len - 1):
            for i in range(len(karakterler) - 1, 0, -1):
                x = (i * keys[j]) % len(karakterler)
                temp = karakterler[i]
                karakterler[i] = karakterler[x]
                karakterler[x] = temp

        return ''.join(karakterler)

    def _fn_character_set_secret_key(self, anahtar):
        arr = [0] * len(anahtar)

        for i in range(len(anahtar) - 1):
            c = anahtar[i]
            hs = 0
            hs = (hs * 31 + ord(c)) % (2 ** 31 - 1)  # int.MaxValue Python'da 2**31-1
            arr[i] = hs

        return arr

    def dispose(self):
        if not self._disposed:
            self._disposed = True