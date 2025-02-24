import socket

def caesar_cipher_encrypt(plaintext, shift):
    """Encrypts plaintext using Caesar cipher."""
    result = ""
    for char in plaintext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def main():
    """Client program for Caesar cipher."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))

    while True:
        operation = input("Choose an operation (encrypt, decrypt, quit): ").strip().lower()
        if operation not in ['encrypt', 'decrypt', 'quit']:
            print("Invalid operation. Please choose 'encrypt', 'decrypt', or 'quit'.")
            continue

        if operation == 'quit':
            client.send("quit".encode())
            print("Closing connection.")
            break

        if operation == 'encrypt':
            # Perform encryption on the client side
            text = input("Enter the text: ").strip()
            try:
                key = int(input("Enter the shift value: ").strip())
            except ValueError:
                print("Invalid shift value. Please enter an integer.")
                continue

            encrypted_text = caesar_cipher_encrypt(text, key)
            print(f"Encrypted Text (Client-Side): {encrypted_text}")

        elif operation == 'decrypt':
            # Send the decryption request to the server
            text = input("Enter the encrypted text: ").strip()
            try:
                key = int(input("Enter the shift value: ").strip())
            except ValueError:
                print("Invalid shift value. Please enter an integer.")
                continue

            request = f"decrypt|{text}|{key}"
            client.send(request.encode())
            decrypted_text = client.recv(1024).decode()
            print(f"Decrypted Text (From Server): {decrypted_text}")

    client.close()

if __name__ == "__main__":
    main()
