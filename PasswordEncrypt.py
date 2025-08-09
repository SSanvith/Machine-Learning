from pyDes import des, CBC, PAD_PKCS5
import base64

# Function to encrypt message using DES
def encrypt_message(message, key):
    cipher = des(key, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    encrypted = cipher.encrypt(message)
    return base64.b64encode(encrypted).decode()

# Input from user
key = input("Enter an 8-character key: ")
while len(key) != 8:
    key = input("Key must be exactly 8 characters. Try again: ")

message = input("Enter the message to encrypt: ")

# Encrypt and display
encrypted_message = encrypt_message(message, key)
print("Encrypted message:", encrypted_message)
