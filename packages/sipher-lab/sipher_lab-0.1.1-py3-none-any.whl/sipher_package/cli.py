import os
import pkg_resources
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Export cipher code")
    parser.add_argument("--output_dir", default="./sipher_exports")  # Changed directory
    args = parser.parse_args()
    
    # Added vernam to the list
    ciphers = ['aes','caesar','des','monoalphabetic','onetimepad','rsa','sha',
              'vigenere', 'playfair', 'hill', 'railfence', 'vernam','something']
    
    for cipher in ciphers:
        cipher_dir = os.path.join(args.output_dir, cipher)
        os.makedirs(cipher_dir, exist_ok=True)
        
        # Server file
        server_path = f'cipher_code/{cipher}/server.py'
        server_content = pkg_resources.resource_string('sipher_package', server_path).decode('utf-8')
        with open(os.path.join(cipher_dir, 'server.txt'), 'w', encoding='utf-8') as f:
            f.write(server_content)
            
        # Client file
        client_path = f'cipher_code/{cipher}/client.py'
        client_content = pkg_resources.resource_string('sipher_package', client_path).decode('utf-8')
        with open(os.path.join(cipher_dir, 'client.txt'), 'w', encoding='utf-8') as f:
            f.write(client_content)
            
    print(f"Exported cipher code to {args.output_dir}")

if __name__ == "__main__":
    main()