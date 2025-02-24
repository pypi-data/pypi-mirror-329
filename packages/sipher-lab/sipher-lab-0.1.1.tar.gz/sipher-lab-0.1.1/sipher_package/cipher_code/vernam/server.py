import socket
import json

def vernam_encrypt(plaintext, key):
    # Convert both plaintext and key to uppercase.
    plaintext = plaintext.upper()
    key = key.upper()
    if len(key) < len(plaintext):
        raise ValueError("Key length must be at least as long as plaintext.")
    ciphertext = ""
    for p, k in zip(plaintext, key):
        if not p.isalpha() or not k.isalpha():
            raise ValueError("Both plaintext and key must contain only letters.")
        c = chr(((ord(p) - ord('A') + (ord(k) - ord('A'))) % 26) + ord('A'))
        ciphertext += c
    return ciphertext

def vernam_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ""
    for c, k in zip(ciphertext, key):
        if not c.isalpha() or not k.isalpha():
            raise ValueError("Both ciphertext and key must contain only letters.")
        p = chr(((ord(c) - ord('A') - (ord(k) - ord('A'))) % 26) + ord('A'))
        plaintext += p
    return plaintext

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    print("Connected by", addr)

    while True:
        # Receive client's JSON message
        data = conn.recv(4096).decode()
        if not data:
            print("Connection closed by client.")
            break

        try:
            received = json.loads(data)
            encrypted_message = received['encrypted']
            key = received['key']
            decrypted_message = vernam_decrypt(encrypted_message, key)
            print("Client sent (encrypted):", encrypted_message)
            print("Client sent (decrypted):", decrypted_message)
        except Exception as e:
            print("Error processing received data:", e)
            break

        # If client sent quit, exit the loop.
        if decrypted_message.upper() == "QUIT":
            print("Quit command received from client. Ending session.")
            # Optionally send a quit confirmation.
            quit_cipher = vernam_encrypt("QUIT", "QUIT")
            response_obj = {"encrypted": quit_cipher, "key": "QUIT"}
            conn.sendall(json.dumps(response_obj).encode())
            break

        # Prompt for response message.
        response = input("Enter response message to send (or 'QUIT' to quit): ")
        if response.upper() == "QUIT":
            # Send quit message without asking for a key.
            response_obj = {"encrypted": "QUIT", "key": "QUIT"}
            conn.sendall(json.dumps(response_obj).encode())
            print("Quit command sent by server. Ending session.")
            break

        response_key = input("Enter key for encrypting response: ")
        try:
            encrypted_response = vernam_encrypt(response, response_key)
        except Exception as e:
            print("Error encrypting response:", e)
            break

        response_obj = {"encrypted": encrypted_response, "key": response_key}
        conn.sendall(json.dumps(response_obj).encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()





################################### FIXED KEY #################################
'''
import socket
import json

FIXED_KEY = "RANCHOBABA"

def vernam_encrypt(plaintext):
    plaintext = plaintext.upper()
    key = FIXED_KEY[:len(plaintext)]
    if len(key) < len(plaintext):
        raise ValueError("Fixed key is not long enough for the plaintext.")
    ciphertext = ""
    for p, k in zip(plaintext, key):
        if not p.isalpha() or not k.isalpha():
            raise ValueError("Plaintext must contain only letters.")
        c = chr(((ord(p) - ord('A') + (ord(k) - ord('A'))) % 26) + ord('A'))
        ciphertext += c
    return ciphertext

def vernam_decrypt(ciphertext):
    ciphertext = ciphertext.upper()
    key = FIXED_KEY[:len(ciphertext)]
    plaintext = ""
    for c, k in zip(ciphertext, key):
        if not c.isalpha() or not k.isalpha():
            raise ValueError("Ciphertext must contain only letters.")
        p = chr(((ord(c) - ord('A') - (ord(k) - ord('A'))) % 26) + ord('A'))
        plaintext += p
    return plaintext

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Fixed Key Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    print("Connected by", addr)

    while True:
        data = conn.recv(4096).decode()
        if not data:
            print("Connection closed by client.")
            break

        try:
            received = json.loads(data)
            encrypted_message = received['encrypted']
            decrypted_message = vernam_decrypt(encrypted_message)
            print("Client sent (encrypted):", encrypted_message)
            print("Client sent (decrypted):", decrypted_message)
        except Exception as e:
            print("Error processing received data:", e)
            break

        if decrypted_message.upper() == "QUIT":
            print("Quit command received from client. Ending session.")
            response_obj = {"encrypted": vernam_encrypt("QUIT")}
            conn.sendall(json.dumps(response_obj).encode())
            break

        response = input("Enter response message to send (or 'QUIT' to quit): ")
        if response.upper() == "QUIT":
            response_obj = {"encrypted": vernam_encrypt("QUIT")}
            conn.sendall(json.dumps(response_obj).encode())
            print("Quit command sent by server. Ending session.")
            break

        try:
            encrypted_response = vernam_encrypt(response)
        except Exception as e:
            print("Error encrypting response:", e)
            break

        response_obj = {"encrypted": encrypted_response}
        conn.sendall(json.dumps(response_obj).encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()



'''