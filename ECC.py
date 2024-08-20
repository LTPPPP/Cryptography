from ecdsa import SigningKey, SECP256k1, VerifyingKey
from hashlib import sha256
import base64
import os

# Tạo khóa
def generate_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

# Ký thông điệp bằng ECC
def sign_message(private_key, message):
    message_hash = sha256(message.encode('utf-8')).digest()
    signature = private_key.sign(message_hash)
    return base64.b64encode(signature).decode('utf-8')

# Xác minh chữ ký
def verify_signature(public_key, message, signature):
    message_hash = sha256(message.encode('utf-8')).digest()
    signature = base64.b64decode(signature)
    return public_key.verify(signature, message_hash)

# Mã hóa thông điệp (giả lập bằng cách xor với khóa công khai)
def encrypt_message(public_key, message):
    message_bytes = message.encode('utf-8')
    encrypted_message = bytes([mb ^ pb for mb, pb in zip(message_bytes, public_key.to_string())])
    return base64.b64encode(encrypted_message).decode('utf-8')

# Giải mã thông điệp (giả lập)
def decrypt_message(private_key, encrypted_message):
    public_key = private_key.get_verifying_key()
    encrypted_message = base64.b64decode(encrypted_message)
    decrypted_message = bytes([eb ^ pb for eb, pb in zip(encrypted_message, public_key.to_string())])
    return decrypted_message.decode('utf-8')

# Chương trình chính
if __name__ == "__main__":
    message = input("TEXT: ")

    # Tạo khóa
    private_key, public_key = generate_keys()

    # In ra khóa riêng tư và khóa công khai
    print("Private Key (hex):", private_key.to_string().hex())
    print("Public Key (hex):", public_key.to_string().hex())

    # Ký thông điệp
    signature = sign_message(private_key, message)
    print(f"Signature: {signature}")

    # Xác minh chữ ký
    if verify_signature(public_key, message, signature):
        print("The signature is valid.")
    else:
        print("The signature is invalid.")

    # Mã hóa
    encrypted_message = encrypt_message(public_key, message)
    print(f"encrypted_message: {encrypted_message}")

    # Giải mã
    decrypted_message = decrypt_message(private_key, encrypted_message)
    print(f"decrypted_message: {decrypted_message}")
