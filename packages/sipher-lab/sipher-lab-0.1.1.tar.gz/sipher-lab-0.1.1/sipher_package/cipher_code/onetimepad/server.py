import socket

def otp_decrypt(key, ciphertext):
    """Decrypt ciphertext using the one-time pad key."""
    plaintext_bytes = bytes([c ^ k for c, k in zip(ciphertext, key)])
    return plaintext_bytes.decode()

def server_listen():
    """Set up the server to listen for client requests."""
    host = '127.0.0.1'  # localhost
    port = 65432        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server is ready. Waiting for a connection...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                action = conn.recv(1024).decode()
                
                if action == "DECRYPT":
                    conn.sendall("ACK".encode())  # Acknowledge

                    key = conn.recv(1024)
                    ciphertext = conn.recv(1024)

                    print("\n--- Decrypting Message ---")
                    plaintext = otp_decrypt(key, ciphertext)
                    print(f"Decrypted Plaintext: {plaintext}")

                    conn.sendall(plaintext.encode())

                elif action == "QUIT":
                    print("Client requested to close the connection.")
                    break

                else:
                    print("Invalid action received.")

if __name__ == "__main__":
    server_listen()
