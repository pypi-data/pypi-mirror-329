import socket

# -----------------------------
# RSA Helper Functions
# -----------------------------
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

def rsa_decrypt(ciphertext_list, d, n):
    """
    Decrypts a list of ciphertext integers using RSA decryption.
    **Mapping:** After computing m = c^d mod n, add 32 (the offset) to recover
    the original ASCII code.
    """
    offset = 32
    plaintext = ""
    for c in ciphertext_list:
        m = modexp(c, d, n)
        plaintext += chr(m + offset)
    return plaintext

# -----------------------------
# Server Main Routine
# -----------------------------
def main():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("Server listening on {}:{}".format(host, port))
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            # Receive the entire message sent by the client.
            data = conn.recv(1024)
            if not data:
                print("No data received!")
                return
            full_message = data.decode('utf-8')
            
            # Expected message format:
            # "PRIVATE_KEY:d,n;CIPHERTEXT:c1 c2 c3 ..."
            try:
                key_part, ctxt_part = full_message.split(";")
                key_label, key_values = key_part.split(":")
                ctxt_label, ctxt_values = ctxt_part.split(":")

                if key_label.strip() != "PRIVATE_KEY" or ctxt_label.strip() != "CIPHERTEXT":
                    raise ValueError("Message labels incorrect.")

                # Extract private key values: d and n
                d_str, n_str = key_values.split(",")
                d = int(d_str.strip())
                n = int(n_str.strip())
                
                # Extract ciphertext: list of integers.
                ciphertext_list = list(map(int, ctxt_values.strip().split()))
                print("Ciphertext received: " + ctxt_values)
            except Exception as e:
                print("Error parsing message:", e)
                return
            
            # Decrypt the ciphertext using the received private key.
            decrypted_message = rsa_decrypt(ciphertext_list, d, n)
            print("Decrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
