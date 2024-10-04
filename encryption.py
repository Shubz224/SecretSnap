import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_message(image_path, key, message):
    # Ensure key is 16 bytes long
    key = key.ljust(16)[:16].encode('utf-8')
    
    # Generate a random IV
    iv = os.urandom(16)
    
    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the message
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)

    # Save the IV and encrypted message (this is just an example)
    with open(image_path, 'wb') as file:
        # Write the IV and encrypted message to the image
        file.write(iv + encrypted_message)

    # Return path of the modified image
    return image_path

def decrypt_message(image_path, key):
    # Ensure key is 16 bytes long
    key = key.ljust(16)[:16].encode('utf-8')

    # Read the image file which contains the IV and encrypted message
    with open(image_path, 'rb') as file:
        iv = file.read(16)  # First 16 bytes are the IV
        encrypted_message = file.read()  # Remaining bytes are the encrypted message

    # Create cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the message
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)

    return decrypted_message.decode('utf-8')
