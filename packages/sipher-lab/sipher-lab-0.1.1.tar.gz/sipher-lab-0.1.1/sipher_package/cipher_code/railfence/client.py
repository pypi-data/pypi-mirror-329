import socket


class RailFenceCipher:
    @staticmethod
    def encrypt(plaintext, rails):
        if rails <= 1:
            return plaintext

        rail_matrix = [['' for _ in range(len(plaintext))] for _ in range(rails)]
        direction_down = False
        row, col = 0, 0

        for char in plaintext:
            rail_matrix[row][col] = char
            col += 1

            if row == 0 or row == rails - 1:
                direction_down = not direction_down

            row += 1 if direction_down else -1

        return ''.join(''.join(row) for row in rail_matrix)

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


def client_program():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    while True:
        print("\n1. Encrypt and send message")
        print("2. Decrypt received message")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            plaintext = input("Enter the plaintext message: ")
            rails = int(input("Enter the number of rails: "))

            encrypted_message = RailFenceCipher.encrypt(plaintext, rails)
            print(f"Encrypted message: {encrypted_message}")

            client_socket.send("ENCRYPT".encode())
            client_socket.send(encrypted_message.encode())
            client_socket.send(str(rails).encode())

            print("Encrypted message sent to server.")

        elif choice == '2':
            encrypted_message = input("Enter the encrypted message: ")
            rails = int(input("Enter the number of rails: "))

            client_socket.send("DECRYPT".encode())
            client_socket.send(encrypted_message.encode())
            client_socket.send(str(rails).encode())

            decrypted_message = client_socket.recv(1024).decode()
            print(f"Decrypted message received from server: {decrypted_message}")

        elif choice == '3':
            client_socket.send("QUIT".encode())
            print("Closing connection...")
            break

        else:
            print("Invalid choice. Please try again.")

    client_socket.close()


if __name__ == "__main__":
    client_program()
