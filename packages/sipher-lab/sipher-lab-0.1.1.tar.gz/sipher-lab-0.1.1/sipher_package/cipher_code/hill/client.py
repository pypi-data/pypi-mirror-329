import socket
import json
import numpy as np

# Predefined 2x2 key matrix
KEY_MATRIX = [[3, 3], [2, 5]]


def hill_encrypt(message, key):
    """Encrypts a message using the Hill cipher."""
    message = message.upper().replace(" ", "")  # Prepare the message
    key_matrix = np.array(key).reshape(2, 2)
    while len(message) % 2 != 0:  # Pad if necessary
        message += "X"

    message_vector = [ord(char) - ord('A') for char in message]
    message_matrix = np.array(message_vector).reshape(-1, 2)

    encrypted_matrix = (np.dot(message_matrix, key_matrix) % 26).astype(int)
    encrypted_text = ''.join([chr(num + ord('A')) for row in encrypted_matrix for num in row])

    return encrypted_text

def send_request(task, message=None):
    """Sends a request to the server and receives the response."""
    request = {"task": task, "message": message}
    
    # Establish the socket connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    
    # Send request to server
    client_socket.send(json.dumps(request).encode())
    
    # Receive the response from the server
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    
    return response

def main():
    while True:
        print("\nHill Cipher Client")
        print("1. Encrypt Message")
        print("2. Decrypt Message")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            message = input("Enter the message to encrypt: ")
            encrypted_message = hill_encrypt(message, KEY_MATRIX)
            print(f"Encrypted Message: {encrypted_message}")

        elif choice == '2':
            response = send_request("decrypt_hill")
            print(f"Decrypted Message (from server): {response}")

        elif choice == '3':
            response = send_request("quit")
            print(response)
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
