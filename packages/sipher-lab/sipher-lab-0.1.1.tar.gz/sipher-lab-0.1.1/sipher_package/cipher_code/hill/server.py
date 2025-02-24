import socket
import json
import numpy as np

# Predefined 2x2 key matrix
KEY_MATRIX = [[3, 3], [2, 5]]


def hill_decrypt(message, key):
    """Decrypts a message using the Hill cipher."""
    key_matrix = np.array(key).reshape(2, 2)
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)  # Modular inverse of determinant

    adj_matrix = np.array([[key_matrix[1, 1], -key_matrix[0, 1]],
                           [-key_matrix[1, 0], key_matrix[0, 0]]]) % 26
    inverse_key = (det_inv * adj_matrix) % 26

    message_vector = [ord(char) - ord('A') for char in message]
    message_matrix = np.array(message_vector).reshape(-1, 2)

    decrypted_matrix = (np.dot(message_matrix, inverse_key) % 26).astype(int)
    decrypted_text = ''.join([chr(num + ord('A')) for row in decrypted_matrix for num in row])

    return decrypted_text.strip("X")

def handle_request(request):
    """Handles client requests."""
    task = request.get("task")

    if task == "decrypt_hill":
        encrypted_message = input("Enter the encrypted message to decrypt: ").upper().replace(" ", "")
        return hill_decrypt(encrypted_message, KEY_MATRIX)
    elif task == "quit":
        return "Connection closed."
    else:
        return "Invalid task."

def start_server():
    """Starts the server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(5)
    print("Server is running...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        request_data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(request_data)

        response = handle_request(request)
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    start_server()
