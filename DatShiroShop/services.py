import os

from api.drive_api import downloadFile

from sys import argv


class EncodeWAV:

    def __init__(self):
        self.header_offset = 44
        self.DELIMITER = '$'
        self.error_msg = ""
        self.encoded_file = ''
        self.processing_byte_ord = self.header_offset

    def encode_file(self, file_path, msg):
        origin_file = open(file_path, 'rb').read()
        origin_file = bytearray(origin_file)
        self.encoded_file = origin_file

        if b"WAV" in origin_file[8:11]:
            msg_len_str = str(len(msg))
            self.hide(msg_len_str + self.DELIMITER)     # Insert Len of Msg
            self.hide(msg)                              # Insert Msg
        else:
            self.error_msg += "Invalid WAV File\n"
            return None
        return self.encoded_file

    def hide(self, msg):
        for c in msg:
            c_in_binary = '{0:08b}'.format(ord(c))
            for b in c_in_binary:
                new_value = self.encoded_file[self.processing_byte_ord] + self.encoded_file[self.processing_byte_ord] % 2 + int(b)
                self.encoded_file[self.processing_byte_ord] = new_value%256
                self.processing_byte_ord += 1


class DecodeWAV:

    def __init__(self):
        self.msg=''
        self.header_offset = 44
        self.DELIMITER = '$'
        self.error_msg = ""
        self.len_hidden_msg = ""
        self.processing_byte_ord = self.header_offset

    def decode_file(self, file_path):
        encoded_file = open(file_path, 'rb').read()
        encoded_file = bytearray(encoded_file)
        processing_byte_ord = self.header_offset
        if b"WAV" in encoded_file[8:11]:
            # get msg length
            temp_byte = []
            while True:
                temp_byte.append(b % 2 for b in encoded_file[processing_byte_ord:processing_byte_ord+8])
                decrypted_char = chr(int(temp_byte, 2))
                self.msg += decrypted_char
                temp_byte = []
                processing_byte_ord += 8
                if decrypted_char == '$':
                    self.len_hidden_msg = int(self.msg[:-1])         # Ignore '$' char at the end
                    self.msg = ""
                    break
            for i in range(0, self.len_hidden_msg):
                temp_byte.append(b % 2 for b in encoded_file[processing_byte_ord:processing_byte_ord + 8])
                decrypted_char = chr(int(temp_byte, 2))
                self.msg += decrypted_char
                temp_byte = []
                processing_byte_ord += 8
            return self.msg


def convertBinaryToMessage(array_bin_msg):
    s = ''.join(str(i) for i in array_bin_msg)
    return chr(int(s, base=2))


def decode_file(img):
    byte = bytearray(img)
    decrypted_message = ""
    decrypted_char = ""
    if "BM" in byte[:20]:
        header_offset = 54
    else:
        print("Can't decrypt not BMP file")
        return None
    temp_byte = []
    while True:
        temp_byte.append(byte[header_offset] % 2)
        header_offset += 1
        if len(temp_byte) == 8:
            decrypted_char = convertBinaryToMessage(temp_byte)
            temp_byte = []
        if decrypted_char is not '\x00' and not None:
            decrypted_message += decrypted_char
            decrypted_char = ""
        else:
            break
    return decrypted_message


if __name__ == "__main__":
    data = open(argv[1], 'rb').read()
    decrypted_message = decryptImage(data)
    if decrypted_message is not None:
        print("Hidden Message: " + decrypted_message)
    else:
        print("Failed to decrypt")


def convertDecToBinary(number):
    bin_array = []
    while number != 0:
        bin_array.insert(0,number % 2)
        number /= 2
    for i in range(0,8 - len(bin_array)):
        bin_array.insert(0,0)
    return bin_array

def convertMessageToBinary(msg):
    byte_msg = bytearray(msg)
    bin_msg = []
    for byte in byte_msg:
        bin_msg += convertDecToBinary(byte)
    return bin_msg


