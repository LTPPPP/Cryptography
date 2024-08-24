import hashlib

# Prompt the user for input
data = input("INPUT : ").encode('utf-8')

# Create a new SHA-3 hash object
hash_obj = hashlib.sha3_256()

# Update the hash object with the data
hash_obj.update(data)

# Get the hexadecimal representation of the hash
hash_hex = hash_obj.hexdigest()

print("SHA-3 Hash:", hash_hex)
