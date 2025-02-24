import struct
import time

### SHA-1 Implementation ###
def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha1(message):
    h0, h1, h2, h3, h4 = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
    
    original_byte_len = len(message)
    message += b'\x80'
    
    while (len(message) + 8) % 64 != 0:
        message += b'\x00'
    
    message += struct.pack('>Q', original_byte_len * 8)

    for i in range(0, len(message), 64):
        w = list(struct.unpack('>16L', message[i:i+64]))
        for j in range(16, 80):
            w.append(left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1))
        
        a, b, c, d, e = h0, h1, h2, h3, h4

        for j in range(80):
            if j < 20:
                f, k = (b & c) | (~b & d), 0x5A827999
            elif j < 40:
                f, k = b ^ c ^ d, 0x6ED9EBA1
            elif j < 60:
                f, k = (b & c) | (b & d) | (c & d), 0x8F1BBCDC
            else:
                f, k = b ^ c ^ d, 0xCA62C1D6

            temp = left_rotate(a, 5) + f + e + k + w[j] & 0xffffffff
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp
        
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def right_rotate(x, n):
    return (x >> n) | (x << (32 - n)) & 0xffffffff

# --- SHA-256 Implementation (Corrected) ---
def sha256(message):
    # Initial hash values for SHA-256
    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # SHA-256 Constants (64 values)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    # Pre-processing: Padding
    original_bit_length = len(message) * 8
    message = bytearray(message)
    message.append(0x80)
    while (len(message) * 8) % 512 != 448:
        message.append(0)
    message += original_bit_length.to_bytes(8, 'big')
    
    # Process the message in successive 512-bit chunks:
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        
        # Prepare the message schedule (64 words)
        w = [0] * 64
        for i in range(16):
            w[i] = int.from_bytes(chunk[i * 4:(i + 1) * 4], 'big')
        for i in range(16, 64):
            s0 = right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffff
        
        # Initialize working variables with current hash value
        a, b, c, d, e, f, g, h_temp = H
        
        # Compression function main loop:
        for i in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h_temp + S1 + ch + K[i] + w[i]) & 0xffffffff
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff
            
            h_temp = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff
        
        # Add the compressed chunk to the current hash value:
        H = [
            (H[0] + a) & 0xffffffff,
            (H[1] + b) & 0xffffffff,
            (H[2] + c) & 0xffffffff,
            (H[3] + d) & 0xffffffff,
            (H[4] + e) & 0xffffffff,
            (H[5] + f) & 0xffffffff,
            (H[6] + g) & 0xffffffff,
            (H[7] + h_temp) & 0xffffffff,
        ]
    
    # Produce the final hash value (big-endian) as a hex string
    return ''.join(f'{value:08x}' for value in H)


### HMAC Implementation ###
def hmac_sha1(key, message):
    block_size = 64
    if len(key) > block_size:
        key = bytes.fromhex(sha1(key))
    key = key.ljust(block_size, b'\x00')
    
    o_key_pad = bytes(x ^ 0x5c for x in key)
    i_key_pad = bytes(x ^ 0x36 for x in key)
    
    return sha1(o_key_pad + bytes.fromhex(sha1(i_key_pad + message)))

def hmac_sha256(key, message):
    block_size = 64
    if len(key) > block_size:
        key = bytes.fromhex(sha256(key))
    key = key.ljust(block_size, b'\x00')
    
    o_key_pad = bytes(x ^ 0x5c for x in key)
    i_key_pad = bytes(x ^ 0x36 for x in key)
    
    return sha256(o_key_pad + bytes.fromhex(sha256(i_key_pad + message)))

### Measure Execution Time ###
def measure_time(key, message_sizes):
    for size in message_sizes:
        message = b"A" * size
        
        start_sha1 = time.time()
        hmac_sha1(key, message)
        end_sha1 = time.time()
        
        start_sha256 = time.time()
        hmac_sha256(key, message)
        end_sha256 = time.time()
        
        print(f"Message Size: {size} bytes")
        print(f"SHA-1 HMAC Time: {end_sha1 - start_sha1:.6f} seconds")
        print(f"SHA-256 HMAC Time: {end_sha256 - start_sha256:.6f} seconds")
        print("-" * 40)

# Test with different message sizes
key = b"supersecretkey"
message_sizes = [10, 100, 1000, 10000, 100000]

measure_time(key, message_sizes)
