import socket

# -----------------------------
# RSA Helper Functions
# -----------------------------
def egcd(a, b):
    """Extended Euclidean Algorithm.
       Returns (gcd, x, y) such that: a*x + b*y = gcd."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modular inverse: finds x such that (a*x) mod m = 1."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % m

def modexp(base, exponent, modulus):
    """Efficient modular exponentiation: computes (base^exponent) mod modulus."""
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent //= 2
        base = (base * base) % modulus
    return result

def generate_keys():
    """
    Generates RSA keys using larger primes.
    For example, using:
      p = 17, q = 19  → n = 323, φ(n) = 288.
      Choose e = 7 (since gcd(7, 288) = 1).
      Then d = modinv(e, 288) = 247.
    Returns:
       public key (e, n) and private key (d, n)
    """
    p = 17
    q = 19
    n = p * q          # 323
    phi = (p - 1) * (q - 1)  # 16 * 18 = 288
    e = 7
    d = modinv(e, phi) # 247 in this case
    return (e, d, n)

def rsa_encrypt(plaintext, e, n):
    """
    Encrypts the plaintext string character-by-character.
    **Mapping:** Subtract 32 from each character's ASCII code so that
    the number falls in the range [0, 94].
    """
    offset = 32
    ciphertext_list = []
    for char in plaintext:
        m = ord(char) - offset  # map to [0, ...]
        c = modexp(m, e, n)
        ciphertext_list.append(c)
    return ciphertext_list

# -----------------------------
# Client Main Routine
# -----------------------------
def main():
    # Generate RSA keys on the client side.
    e, d, n = generate_keys()

    
    # Get plaintext input from the user.
    plaintext = input("Enter plaintext message: ")
    print("Generated Public Key: (e={}, n={})".format(e, n))
    print("Generated Private Key: (d={}, n={})".format(d, n))
    # Encrypt the plaintext using the public key.
    ciphertext_list = rsa_encrypt(plaintext, e, n)
    # Convert ciphertext list to space-separated string.
    ciphertext_str = " ".join(str(num) for num in ciphertext_list)
    print("Ciphertext Sent:", ciphertext_str)
    
    # Prepare the full message to send.
    # Format: "PRIVATE_KEY:d,n;CIPHERTEXT:c1 c2 c3 ..."
    full_message = "PRIVATE_KEY:{},{};CIPHERTEXT:{}".format(d, n, ciphertext_str)
    
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(full_message.encode('utf-8'))
        print("Message sent to server!")

if __name__ == "__main__":
    main()
