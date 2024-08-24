import hashlib

def generate_sha256(data):
    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()

    # If the input data is a string, encode it to bytes
    if isinstance(data, str):
        data = data.encode('utf-8')

    # Update the hash object with the bytes-like object
    sha256_hash.update(data)

    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

# Example usage
data = input("TEXT : ")
hash_value = generate_sha256(data)
print(f"SHA-256 hash of '{data}' : {hash_value}")
