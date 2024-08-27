import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from PIL import Image
import io
import pyperclip

def read_image_from_path(path):
    with open(path, 'rb') as f:
        return f.read()

def read_image_from_clipboard():
    image_data = pyperclip.paste()
    return image_data

def encrypt_image(image_data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(image_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def save_encrypted_image(encrypted_data, output_path):
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)

def main():
    # Đọc hình ảnh từ đường dẫn hoặc clipboard
    path = 'img/cat.jpg'
    image_data = read_image_from_path(path)
    # Hoặc đọc từ clipboard
    # image_data = read_image_from_clipboard()

    # Khóa mã hóa (16, 24 hoặc 32 bytes)
    key = b'Sixteen byte key'

    # Mã hóa hình ảnh
    encrypted_data = encrypt_image(image_data, key)

    # Lưu hình ảnh đã mã hóa
    output_path = 'img/encrypted_image.bin'
    save_encrypted_image(encrypted_data, output_path)

if __name__ == "__main__":
    main()
