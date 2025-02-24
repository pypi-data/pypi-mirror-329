import socket
import threading

def caesar_cipher_decrypt(ciphertext, shift):
    """Decrypts ciphertext using Caesar cipher."""
    result = ""
    for char in ciphertext:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            result += char
    return result

def handle_client(client_socket):
    """Handles client requests."""
    while True:
        data = client_socket.recv(1024).decode()
        if not data or data == "quit":
            print("Client disconnected.")
            break

        # Parse the request
        operation, text, key = data.split('|')
        key = int(key)

        if operation == 'decrypt':
            decrypted_text = caesar_cipher_decrypt(text, key)
            client_socket.send(decrypted_text.encode())
        else:
            client_socket.send("Invalid operation.".encode())

    client_socket.close()

def main():
    """Sets up the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server is running and waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection established with {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
