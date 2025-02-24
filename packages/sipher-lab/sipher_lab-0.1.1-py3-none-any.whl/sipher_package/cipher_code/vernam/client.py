import socket
import json

def vernam_encrypt(plaintext, key):
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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        # Prompt for message first.
        plaintext = input("Enter the message to send to the server (or 'QUIT' to quit): ")
        if plaintext.upper() == "QUIT":
            # Send quit command without asking for key.
            msg_obj = {"encrypted": "QUIT", "key": "QUIT"}
            client_socket.sendall(json.dumps(msg_obj).encode())
            print("Quit command sent. Ending session.")
            break

        key = input("Enter key for encryption: ")
        try:
            encrypted_message = vernam_encrypt(plaintext, key)
        except Exception as e:
            print("Error during encryption:", e)
            break

        msg_obj = {"encrypted": encrypted_message, "key": key}
        client_socket.sendall(json.dumps(msg_obj).encode())

        data = client_socket.recv(4096).decode()
        if not data:
            print("Connection closed by server.")
            break

        try:
            response_obj = json.loads(data)
            encrypted_response = response_obj['encrypted']
            response_key = response_obj['key']
            decrypted_response = vernam_decrypt(encrypted_response, response_key)
            print("Server sent (encrypted):", encrypted_response)
            print("Server sent (decrypted):", decrypted_response)
        except Exception as e:
            print("Error processing server response:", e)
            break

        if decrypted_response.upper() == "QUIT":
            print("Quit command received from server. Ending session.")
            break

    client_socket.close()

if __name__ == "__main__":
    main()




############################## FIXED KEY ###############################
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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        plaintext = input("Enter the message to send to the server (or 'QUIT' to quit): ")
        if plaintext.upper() == "QUIT":
            msg_obj = {"encrypted": vernam_encrypt("QUIT")}
            client_socket.sendall(json.dumps(msg_obj).encode())
            print("Quit command sent. Ending session.")
            break

        try:
            encrypted_message = vernam_encrypt(plaintext)
        except Exception as e:
            print("Error during encryption:", e)
            break

        msg_obj = {"encrypted": encrypted_message}
        client_socket.sendall(json.dumps(msg_obj).encode())

        data = client_socket.recv(4096).decode()
        if not data:
            print("Connection closed by server.")
            break

        try:
            response_obj = json.loads(data)
            encrypted_response = response_obj['encrypted']
            decrypted_response = vernam_decrypt(encrypted_response)
            print("Server sent (encrypted):", encrypted_response)
            print("Server sent (decrypted):", decrypted_response)
        except Exception as e:
            print("Error processing server response:", e)
            break

        if decrypted_response.upper() == "QUIT":
            print("Quit command received from server. Ending session.")
            break

    client_socket.close()

if __name__ == "__main__":
    main()


'''