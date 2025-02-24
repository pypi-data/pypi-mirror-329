import os
import pkg_resources
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Export cipher code")
    parser.add_argument("--output_dir", 
                       default="./cipher_exports",
                       help="Output directory (default: ./cipher_exports)")
    args = parser.parse_args()
    
    ciphers = ['aes','caesar','des','monoalphabetic','onetimepad','rsa','sha','vigenere', 'playfair', 'hill', 'railfence']  # Update with your cipher names

    for cipher in ciphers:
        # Create cipher directory
        cipher_dir = os.path.join(args.output_dir, cipher)
        os.makedirs(cipher_dir, exist_ok=True)

        # Export server.py
        server_path = f'cipher_code/{cipher}/server.py'
        server_content = pkg_resources.resource_string('cipher_package', server_path).decode('utf-8')
        with open(os.path.join(cipher_dir, 'server.txt'), 'w', encoding='utf-8') as f:  # ← Add encoding here
            f.write(server_content)

        # Export client.py
        client_path = f'cipher_code/{cipher}/client.py'
        client_content = pkg_resources.resource_string('cipher_package', client_path).decode('utf-8')
        with open(os.path.join(cipher_dir, 'client.txt'), 'w', encoding='utf-8') as f:  # ← Add encoding here
            f.write(client_content)

    print(f"Exported all cipher code to {args.output_dir}")

if __name__ == "__main__":
    main()