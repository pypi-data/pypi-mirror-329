import socket

def vigenere_encrypt(plaintext, key):
    encrypted_text = []
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_text.append(encrypted_char)
            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def client_program():
    host = '127.0.0.1'  # Server IP
    port = 12345         # Port to bind to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            # Choose encryption or decryption or quit
            choice = input("Enter 1 for encryption, 2 for decryption, 3 to quit: ")
            client_socket.send(choice.encode())

            if choice == '1':
                # Encrypt message
                plaintext = input("Enter the plaintext message to encrypt: ")
                key = input("Enter the key for encryption: ")

                # Encrypt the message
                encrypted_message = vigenere_encrypt(plaintext, key)
                print(f"Encrypted message: {encrypted_message}")

                # Send encrypted message to the server
                client_socket.send(encrypted_message.encode())

            elif choice == '2':
                # Decrypt message
                encrypted_message = input("Enter the encrypted message to decrypt: ")
                key = input("Enter the key for decryption: ")

                # Send the encrypted message and key to the server
                client_socket.send(encrypted_message.encode())
                client_socket.send(key.encode())

                # Receive decrypted message from the server
                decrypted_message = client_socket.recv(1024).decode()
                print(f"Decrypted message: {decrypted_message}")

            elif choice == '3':
                # Close the connection
                print("Closing connection...")
                client_socket.close()
                break
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

if __name__ == "__main__":
    client_program()
