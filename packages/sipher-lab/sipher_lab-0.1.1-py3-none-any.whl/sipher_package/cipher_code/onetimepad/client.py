import socket
import os

def generate_key(length):
    """Generate a random key of the given length."""
    return os.urandom(length)

def otp_encrypt(plaintext):
    """Encrypt plaintext using a one-time pad."""
    plaintext_bytes = plaintext.encode()
    key = generate_key(len(plaintext_bytes))
    ciphertext = bytes([p ^ k for p, k in zip(plaintext_bytes, key)])
    return key, ciphertext

def client_menu():
    """Menu-driven client interface."""
    host = '127.0.0.1'  # Server address
    port = 65432        # Port to connect to

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        while True:
            print("\nClient Menu:")
            print("1. Encrypt a Message")
            print("2. Decrypt a Message")
            print("3. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":  # Encrypt a message
                plaintext = input("Enter the plaintext to encrypt: ")
                key, ciphertext = otp_encrypt(plaintext)

                print("\n--- Encryption Result ---")
                print(f"Plaintext: {plaintext}")
                print(f"Generated Key (hex): {key.hex()}")
                print(f"Ciphertext (hex): {ciphertext.hex()}")

            elif choice == "2":  # Decrypt a message
                print("\nEnter the key and ciphertext for decryption:")
                key_hex = input("Enter the key (hex format): ")
                ciphertext_hex = input("Enter the ciphertext (hex format): ")

                # Convert inputs from hex to bytes
                key = bytes.fromhex(key_hex)
                ciphertext = bytes.fromhex(ciphertext_hex)

                # Send the request to the server
                client_socket.sendall("DECRYPT".encode())
                client_socket.recv(1024)  # Acknowledge

                client_socket.sendall(key)
                client_socket.sendall(ciphertext)

                # Receive and display the result
                plaintext = client_socket.recv(1024).decode()
                print(f"\n--- Decryption Result ---")
                print(f"Decrypted Plaintext: {plaintext}")

            elif choice == "3":  # Quit
                client_socket.sendall("QUIT".encode())
                print("Connection closed. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    client_menu()
