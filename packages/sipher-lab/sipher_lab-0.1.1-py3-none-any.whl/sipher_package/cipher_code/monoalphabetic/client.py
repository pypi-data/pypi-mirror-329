import socket
import json

PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER_ALPHABET = "QWERTYUIOPASDFGHJKLZXCVBNM"

def encrypt(plaintext):
    """
    Encrypts the given plaintext using the monoalphabetic cipher.
    Each letter in the plaintext is replaced by its corresponding letter 
    in the cipher alphabet.
    """
    plaintext = plaintext.upper()  # Convert to uppercase for uniformity
    return ''.join(
        CIPHER_ALPHABET[PLAIN_ALPHABET.index(char)] if char in PLAIN_ALPHABET else char
        for char in plaintext
    )

def send_request(task, message=""):
    """
    Sends a request to the server with the specified task and message.
    """
    host = '127.0.0.1'  # Server's IP address
    port = 65432        # Server's port

    try:
        # Create a socket connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            # Prepare the request in JSON format
            request = {"task": task, "message": message}
            client_socket.send(json.dumps(request).encode('utf-8'))

            # Receive and decode the server's response
            response = client_socket.recv(1024).decode('utf-8')
            return json.loads(response)
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    """
    Main function for interacting with the server.
    Provides a menu for encryption, decryption, and quitting.
    """
    while True:
        print("\nMonoalphabetic Cipher Client")
        print("1. Encrypt a message (Client-Side)")
        print("2. Decrypt a message (Server-Side)")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # Encrypt locally on the client
            message = input("Enter the plaintext to encrypt: ")
            encrypted_message = encrypt(message)
            print(f"Encrypted message: {encrypted_message}")

        elif choice == "2":
            # Send the encrypted message to the server for decryption
            message = input("Enter the ciphertext to decrypt: ")
            response = send_request("decrypt", message)
            if response.get("status") == "success":
                print(f"Decrypted message: {response.get('result')}")
            else:
                print(f"Error: {response.get('message')}")

        elif choice == "3":
            # Send a quit request to the server
            response = send_request("quit")
            print(response.get("result", "Exiting..."))
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
