from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os


def encrypt_text(plaintext, password):
    # Generate a random 16-byte salt
    salt = os.urandom(16)

    # Derive a 32-byte key using PBKDF2 HMAC with SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of the block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    # Encrypt the plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Combine salt, iv, and ciphertext into one message
    encrypted_message = urlsafe_b64encode(salt + iv + ciphertext).decode('utf-8')
    return encrypted_message


def decrypt_text(encrypted_message, password):
    # Decode the encrypted message
    encrypted_data = urlsafe_b64decode(encrypted_message)

    # Extract salt, iv, and ciphertext
    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    # Derive the key using the provided password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode('utf-8')


# Example usage
password = "PASSWORDS"
plaintext = input("TEXT : ")

encrypted = encrypt_text(plaintext, password)
print(f"Encrypted: {encrypted}")

decrypted = decrypt_text(encrypted, password)
print(f"Decrypted: {decrypted}")
