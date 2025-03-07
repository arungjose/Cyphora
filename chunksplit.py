import os
from urllib.parse import urlparse

def split_file(file_path, chunk_size, output_folder, output_prefix):
    """
    Splits the given text file into chunks of approximately 'chunk_size' characters.
    Each chunk is saved in the specified output folder with names based on the output_prefix.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    with open(file_path, 'r', encoding='utf-8') as infile:
        chunk_number = 1
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break  # No more data to read
            output_filename = os.path.join(output_folder, f"{output_prefix}_chunk_{chunk_number}.txt")
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                outfile.write(chunk)
            print("Created chunk:", output_filename)
            chunk_number += 1

def main():
    # Read URL from userlink.txt to determine the domain prefix
    try:
        with open("userlink.txt", "r", encoding="utf-8") as f:
            url = f.readline().strip()
    except Exception as e:
        print("Error reading userlink.txt:", e)
        return

    if not url:
        print("No URL found in userlink.txt")
        return

    # Create a domain-based prefix
    parsed = urlparse(url)
    domain_prefix = parsed.netloc.replace(".", "_")
    
    # File names based on the domain prefix
    html_file = f"{domain_prefix}_html.txt"
    css_file = f"{domain_prefix}_css.txt"
    js_file = f"{domain_prefix}_js.txt"
    text_file = f"{domain_prefix}_text.txt"
    
    # Set chunk size to approximately 256KB (256 * 1024 * characters)
    chunk_size = 256 * 1024
    
    # Split the files into chunks and store them in respective folders
    split_file(html_file, chunk_size, "html", f"{domain_prefix}_html")
    split_file(css_file, chunk_size, "css", f"{domain_prefix}_css")
    split_file(js_file, chunk_size, "js", f"{domain_prefix}_js")
    split_file(text_file, chunk_size, "text", f"{domain_prefix}_text")

if __name__ == "__main__":
    main()
