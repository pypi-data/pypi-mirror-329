# client.py 
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1",12345))
print("Client connected")



while True:
    message = input("Client: ")
    client_socket.sendall(message.encode())
    
    if message.lower() == "exit":
        break
    
    data = client_socket.recv(1024).decode()
    print("Received data: ", data)

client_socket.close()


# server.py
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1",12345))
server_socket.listen(1)
print("Server is listening")

conn, addr = server_socket.accept()
print("Connection from: ", addr)

def encryptMessage(data):
    encrypted_message = ""
    key_value = 3
    for char in data:
        if char.isalpha():
            # Preserve case for letters
            if char.isupper():
                encrypted_message += chr((ord(char) - ord('A') + key_value) % 26 + ord('A'))
            else:
                encrypted_message += chr((ord(char) - ord('a') + key_value) % 26 + ord('a'))
        else:
            encrypted_message += char
    return encrypted_message

def decryptMessage(encrypt_message):
    decrypted_message = ""
    key_value = 3
    for char in encrypt_message:
        if char.isalpha():
            if char.isupper():
                decrypted_message += chr((ord(char) - ord('A') - key_value) % 26 + ord('A'))
            else:
                decrypted_message += chr((ord(char) - ord('a') - key_value) % 26 + ord('a'))
        else:
            decrypted_message += char
    return decrypted_message


while True:
    data = conn.recv(1024).decode()
    if not data or data.lower() == "exit":
        break
    print("Received data: ", data)
    
    encrypt_message = encryptMessage(data)
    print("Encrypted message: ", encrypt_message)
    decrypt_message = decryptMessage(encrypt_message)
    print("Decrypted message: ", decrypt_message)
    message = input("Server: ")
    conn.sendall(message.encode())
    
conn.close()
server_socket.close()


