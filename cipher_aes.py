from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import asymmetric, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import hexlify
#hexlify(bytes(multiplication_matrix_element)).decode(UTF_8)


print(hex(10000))
# aes_key = [0x41, 0x45, 0x49, 0x4d, 0x42, 0x46, 0x4a, 0x4e, 0x43, 0x47, 0x4b, 0x4f, 0x44, 0x48, 0x4c, 0x50 ]
# print(aes_key)
# aes_key = bytearray(aes_key)
# print(aes_key)

# encrypted_text = [232 ,150 ,57 , 254 ,80 ,33 , 176 ,25 ,14 ,55 ,117 ,231 ,123 ,106 ,47 ,122]
# encrypted_text = bytearray(encrypted_text)
# print(encrypted_text)

# aes_decryptor = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=default_backend()).decryptor()
# plain_text = aes_decryptor.update(encrypted_text) + aes_decryptor.finalize()

# unpadder = padding.PKCS7(128).unpadder()
# padded_data = unpadder.update(plain_text)
# padded_data += unpadder.finalize()


# print(padded_data)