import os
from urllib.parse import urlparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# Example 32-byte key for AES-256. In production, generate and store this key securely.
key = b"0123456789abcdef0123456789abcdef"

def encrypt_file(input_file, output_file, key):
    """
    Encrypts the entire content of the input_file using AES-256 in CBC mode.
    A random 16-byte IV is generated and prepended to the ciphertext.
    The result is written in binary mode to output_file.
    """
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Generate a random IV (16 bytes for AES)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data so its length is a multiple of the block size (16 bytes)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    
    # Write the IV and ciphertext to the output file
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)
    print(f"Encrypted file saved as {output_file}")

def main():
    # Read the URL from userlink.txt
    try:
        with open("userlink.txt", "r", encoding="utf-8") as f:
            url = f.readline().strip()
    except Exception as e:
        print("Error reading userlink.txt:", e)
        return
    
    if not url:
        print("No URL found in userlink.txt")
        return

    # Generate a domain-based prefix (e.g. "en_wikipedia_org")
    parsed = urlparse(url)
    domain_prefix = parsed.netloc.replace(".", "_")
    
    # Expected scraped file names (created by webscrape.py)
    html_file = f"{domain_prefix}_html.txt"
    css_file = f"{domain_prefix}_css.txt"
    js_file = f"{domain_prefix}_js.txt"
    text_file = f"{domain_prefix}_text.txt"
    
    # Create an output folder for encrypted files
    output_folder = "encrypted"
    os.makedirs(output_folder, exist_ok=True)
    
    # Encrypt each file and store the output in the "encrypted" folder
    encrypt_file(html_file, os.path.join(output_folder, f"{domain_prefix}_html_encrypted.bin"), key)
    encrypt_file(css_file, os.path.join(output_folder, f"{domain_prefix}_css_encrypted.bin"), key)
    encrypt_file(js_file, os.path.join(output_folder, f"{domain_prefix}_js_encrypted.bin"), key)
    #encrypt_file(text_file, os.path.join(output_folder, f"{domain_prefix}_text_encrypted.bin"), key)

if __name__ == "__main__":
    main()
