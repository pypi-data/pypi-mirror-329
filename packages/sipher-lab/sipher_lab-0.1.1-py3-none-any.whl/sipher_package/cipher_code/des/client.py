import socket
import math

# DES Helper Functions

# Permutation function
def permute(block, table):
    return [block[i - 1] for i in table]

# XOR function
def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]

# Left shift function
def shift_left(block, shifts):
    return block[shifts:] + block[:shifts]

# S-Box substitution function
def sbox_substitution(block):
    # S-Boxes used in DES
    s_boxes = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        # S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    result = []
    for i in range(0, len(block), 6):
        chunk = block[i:i + 6]
        row = (chunk[0] << 1) + chunk[5]
        col = int(''.join(map(str, chunk[1:5])), 2)
        value = s_boxes[i // 6][row][col]
        result.extend(map(int, f"{value:04b}"))
    return result

# Round function
def round_function(right, subkey):
    expansion_table = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
                       8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                       16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
                       24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

    perm_table = [16, 7, 20, 21, 29, 12, 28, 17,
                  1, 15, 23, 26, 5, 18, 31, 10,
                  2, 8, 24, 14, 32, 27, 3, 9,
                  19, 13, 30, 6, 22, 11, 4, 25]

    expanded = permute(right, expansion_table)
    xor_result = xor(expanded, subkey)
    substituted = sbox_substitution(xor_result)
    return permute(substituted, perm_table)

# Key schedule function
def key_schedule(key):
    pc1 = [57, 49, 41, 33, 25, 17, 9, 1,
           58, 50, 42, 34, 26, 18, 10, 2,
           59, 51, 43, 35, 27, 19, 11, 3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15, 7, 62, 54, 46, 38,
           30, 22, 14, 6, 61, 53, 45, 37,
           29, 21, 13, 5, 28, 20, 12, 4]

    pc2 = [14, 17, 11, 24, 1, 5, 3, 28,
           15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]

    shifts = [1, 1, 2, 2, 2, 2, 2, 2,
              1, 2, 2, 2, 2, 2, 2, 1]

    permuted_key = permute(key, pc1)
    left, right = permuted_key[:28], permuted_key[28:]
    round_keys = []

    for shift in shifts:
        left = shift_left(left, shift)
        right = shift_left(right, shift)
        round_keys.append(permute(left + right, pc2))

    return round_keys

# DES encryption function for a single block
def des_encrypt_block(block, round_keys):
    ip = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    fp = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

    permuted_block = permute(block, ip)
    left, right = permuted_block[:32], permuted_block[32:]

    for key in round_keys:
        new_right = xor(left, round_function(right, key))
        left, right = right, new_right

    pre_output = right + left
    return permute(pre_output, fp)

# DES decryption function for a single block
def des_decrypt_block(block, round_keys):
    return des_encrypt_block(block, round_keys[::-1])

# Padding function for messages
def pad_message(message, block_size=8):
    padding_length = block_size - (len(message) % block_size)
    return message + bytes([padding_length] * padding_length)

# Unpadding function for messages
def unpad_message(padded_message):
    padding_length = padded_message[-1]
    return padded_message[:-padding_length]

# DES encryption function for a message
def des_encrypt(message, key):
    message = pad_message(message)
    binary_key = [int(bit) for bit in f"{int.from_bytes(key, 'big'):064b}"]
    round_keys = key_schedule(binary_key)

    ciphertext = b""
    for i in range(0, len(message), 8):
        block = message[i:i + 8]
        binary_block = [int(bit) for bit in f"{int.from_bytes(block, 'big'):064b}"]
        encrypted_block = des_encrypt_block(binary_block, round_keys)
        ciphertext += int("".join(map(str, encrypted_block)), 2).to_bytes(8, "big")

    return ciphertext

# DES decryption function for a message
def des_decrypt(ciphertext, key):
    binary_key = [int(bit) for bit in f"{int.from_bytes(key, 'big'):064b}"]
    round_keys = key_schedule(binary_key)

    plaintext = b""
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i + 8]
        binary_block = [int(bit) for bit in f"{int.from_bytes(block, 'big'):064b}"]
        decrypted_block = des_decrypt_block(binary_block, round_keys)
        plaintext += int("".join(map(str, decrypted_block)), 2).to_bytes(8, "big")

    return unpad_message(plaintext)

# Pre-shared key
KEY = b"12345678"

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        plaintext = input("Enter message to send: ")
        if plaintext.lower() == 'exit':
            break

        ciphertext = des_encrypt(plaintext.encode(), KEY)
        print(f"Encrypted message to send: {ciphertext.hex()}")
        client_socket.send(ciphertext)
        print("Message sent to server.")

        encrypted_response = client_socket.recv(1024)
        print(f"Encrypted response received: {encrypted_response.hex()}")
        decrypted_response = des_decrypt(encrypted_response, KEY)
        print(f"Server response: {decrypted_response.decode()}")

    client_socket.close()

if __name__ == "__main__":
    main()