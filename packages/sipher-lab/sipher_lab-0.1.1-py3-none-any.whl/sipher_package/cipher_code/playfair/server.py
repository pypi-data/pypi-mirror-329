import socket
import json

def create_matrix(keyword):
    """Creates a Playfair cipher matrix based on the keyword."""
    keyword = ''.join(sorted(set(keyword), key=keyword.index))  # Remove duplicates
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 'J' is usually omitted
    matrix = [char for char in keyword if char in alphabet]  # Add keyword characters
    matrix += [char for char in alphabet if char not in matrix]  # Add remaining letters
    return matrix

def digraphs(message):
    """Converts the message into digraphs, padding with 'X' if needed."""
    message = message.upper().replace("J", "I")  # Replace J with I
    digraphs = []
    i = 0
    while i < len(message):
        if i + 1 < len(message) and message[i] != message[i + 1]:
            digraphs.append(message[i:i + 2])
            i += 2
        else:
            digraphs.append(message[i] + ("X" if message[i] != "X" else "Z"))
            i += 1
    return digraphs

def encrypt(message, keyword):
    """Encrypts the message using Playfair cipher."""
    matrix = create_matrix(keyword)
    digraph_list = digraphs(message)
    encrypted_text = []
    for digraph in digraph_list:
        row1, col1 = divmod(matrix.index(digraph[0]), 5)
        row2, col2 = divmod(matrix.index(digraph[1]), 5)
        if row1 == row2:
            encrypted_text.append(matrix[row1 * 5 + (col1 + 1) % 5])
            encrypted_text.append(matrix[row2 * 5 + (col2 + 1) % 5])
        elif col1 == col2:
            encrypted_text.append(matrix[((row1 + 1) % 5) * 5 + col1])
            encrypted_text.append(matrix[((row2 + 1) % 5) * 5 + col2])
        else:
            encrypted_text.append(matrix[row1 * 5 + col2])
            encrypted_text.append(matrix[row2 * 5 + col1])
    return ''.join(encrypted_text)

def decrypt(message, keyword):
    """Decrypts the message using Playfair cipher."""
    matrix = create_matrix(keyword)
    digraph_list = digraphs(message)
    decrypted_text = []
    for digraph in digraph_list:
        row1, col1 = divmod(matrix.index(digraph[0]), 5)
        row2, col2 = divmod(matrix.index(digraph[1]), 5)
        if row1 == row2:
            decrypted_text.append(matrix[row1 * 5 + (col1 - 1) % 5])
            decrypted_text.append(matrix[row2 * 5 + (col2 - 1) % 5])
        elif col1 == col2:
            decrypted_text.append(matrix[((row1 - 1) % 5) * 5 + col1])
            decrypted_text.append(matrix[((row2 - 1) % 5) * 5 + col2])
        else:
            decrypted_text.append(matrix[row1 * 5 + col2])
            decrypted_text.append(matrix[row2 * 5 + col1])
    return ''.join(decrypted_text).rstrip("XZ")  # Remove 'X'/'Z' padding

def handle_client(client_socket):
    """Handles a single client connection."""
    data = client_socket.recv(1024).decode()
    request = json.loads(data)
    task = request["task"]
    message = request["message"]
    keyword = request["keyword"]
    if task == "encrypt":
        response = encrypt(message, keyword)
    elif task == "decrypt":
        response = decrypt(message, keyword)
    else:
        response = "Invalid task."
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(5)
    print("Playfair Cipher Server is running...")
    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)

if __name__ == "__main__":
    main()
