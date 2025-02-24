import socket


class RailFenceCipher:
    @staticmethod
    def decrypt(ciphertext, rails):
        if rails <= 1:
            return ciphertext

        rail_matrix = [['' for _ in range(len(ciphertext))] for _ in range(rails)]
        index, direction_down = 0, False
        row, col = 0, 0

        for _ in range(len(ciphertext)):
            rail_matrix[row][col] = '*'
            col += 1

            if row == 0 or row == rails - 1:
                direction_down = not direction_down

            row += 1 if direction_down else -1

        for i in range(rails):
            for j in range(len(ciphertext)):
                if rail_matrix[i][j] == '*' and index < len(ciphertext):
                    rail_matrix[i][j] = ciphertext[index]
                    index += 1

        result = []
        row, col, direction_down = 0, 0, False

        for _ in range(len(ciphertext)):
            result.append(rail_matrix[row][col])
            col += 1

            if row == 0 or row == rails - 1:
                direction_down = not direction_down

            row += 1 if direction_down else -1

        return ''.join(result)


def server_program():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening...")

    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    while True:
        command = conn.recv(1024).decode()

        if command == "QUIT":
            print("Client has disconnected.")
            break

        if command == "ENCRYPT":
            encrypted_message = conn.recv(1024).decode()
            rails = int(conn.recv(1024).decode())
            print(f"Encrypted Message Received: {encrypted_message}, Rails: {rails}")

        elif command == "DECRYPT":
            encrypted_message = conn.recv(1024).decode()
            rails = int(conn.recv(1024).decode())
            print(f"Decrypting Message: {encrypted_message}, Rails: {rails}")

            decrypted_message = RailFenceCipher.decrypt(encrypted_message, rails)
            print(f"Decrypted Message: {decrypted_message}")

            conn.send(decrypted_message.encode())

    conn.close()


if __name__ == "__main__":
    server_program()
