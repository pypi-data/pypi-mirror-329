import socket
import json

PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER_ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

def decrypt(ciphertext):
    """
    Decrypts the given ciphertext using the monoalphabetic cipher.
    Each letter in the ciphertext is replaced by its corresponding letter 
    in the plain alphabet.
    """
    ciphertext = ciphertext.upper()  # Convert to uppercase for uniformity
    return ''.join(
        PLAIN_ALPHABET[CIPHER_ALPHABET.index(char)] if char in CIPHER_ALPHABET else char
        for char in ciphertext
    )

def handle_client_request(data):
    """
    Processes client requests and returns the appropriate response.
    Handles decryption and quit tasks.
    """
    try:
        # Parse the incoming JSON data
        request = json.loads(data)
        task = request.get("task")  # Task: decrypt or quit
        message = request.get("message")  # Message to process

        if task == "decrypt":
            # Decrypt the message
            return {"status": "success", "result": decrypt(message)}
        elif task == "quit":
            # Handle quit command
            return {"status": "quit", "result": "Connection closed by client request."}
        else:
            # Invalid task error
            return {"status": "error", "message": "Invalid task."}
    except Exception as e:
        # Handle unexpected errors
        return {"status": "error", "message": str(e)}

def start_server():
    """
    Starts the server to listen for client connections.
    Processes client requests in a loop until the client sends a quit command.
    """
    host = '127.0.0.1'  # Localhost
    port = 65432        # Port number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind the server to the host and port
    server_socket.listen(5)  # Allow up to 5 pending connections
    print("Server started. Waiting for clients...")

    while True:
        # Accept client connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            print("No data received. Closing connection.")
            client_socket.close()
            continue

        # Process the client request
        response = handle_client_request(data)

        # Handle quit command
        if response.get("status") == "quit":
            client_socket.send(json.dumps(response).encode('utf-8'))
            print(response.get("result"))  # Print quit confirmation
            client_socket.close()
            break

        # Send the response back to the client
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()

    # Shut down the server after handling quit
    print("Shutting down the server.")
    server_socket.close()

if __name__ == "__main__":
    start_server()
