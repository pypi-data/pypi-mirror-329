import socket

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

def server_program():
    host = '127.0.0.1'  # Localhost IP
    port = 12345         # Port to bind to

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening...")

    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    try:
        while True:
            # Receive the choice from the client (encrypt, decrypt, quit)
            choice = conn.recv(1024).decode()

            if choice == '1':
                # Client wants to encrypt a message (Server just listens and responds)
                encrypted_message = conn.recv(1024).decode()
                print(f"Encrypted message received: {encrypted_message}")

            elif choice == '2':
                # Client wants to decrypt a message
                encrypted_message = conn.recv(1024).decode()
                key = conn.recv(1024).decode()

                print(f"Encrypted message: {encrypted_message}")
                print(f"Key for decryption: {key}")

                # Decrypt the message
                decrypted_message = vigenere_decrypt(encrypted_message, key)
                print(f"Decrypted message: {decrypted_message}")

                # Send the decrypted message back to the client
                conn.send(decrypted_message.encode())

            elif choice == '3':
                # Close the connection
                print("Closing connection...")
                conn.close()
                break
    except ConnectionResetError:
        print("Connection was closed by the client.")
    finally:
        conn.close()

if __name__ == "__main__":
    server_program()
