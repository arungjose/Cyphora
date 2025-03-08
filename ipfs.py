import os
import ipfsapi
from urllib.parse import urlparse

# Monkey-patch ipfsapi's version method to return a fake version in the supported range.
def patched_version(self):
    # Return a version dictionary with a Version that lies between 0.4.3 and 0.5.0.
    return {"Version": "0.4.4", "Commit": "patched", "System": "patched"}

# Apply the patch.
ipfsapi.client.Client.version = patched_version

def upload_folder_to_ipfs(folder_path, folder_name):
    """
    Connects to the local IPFS node and uploads the folder at folder_path as a single folder.
    Returns the CID of the folder if successful.
    """
    try:
        # Connect to your local IPFS node (make sure 'ipfs daemon' is running)
        client = ipfsapi.connect('127.0.0.1', 5001)
        # Call our patched version method.
        ver = client.version()
        print("Patched IPFS daemon version:", ver)

        # Add files to IPFS and wrap them into a directory
        result = client.add(folder_path, recursive=True, wrap_with_directory=True)
        
        # Find the CID of the wrapped directory
        for item in result:
            if item['Name'] == folder_name:
                cid = item['Hash']
                print(f"Uploaded folder {folder_name} with CID: {cid}")
                return cid
        print("Folder CID not found in the result.")
        return None
    except Exception as e:
        print(f"Error uploading folder {folder_name}: {e}")
        return None

def main():
    # Read the URL from userlink.txt to determine the domain prefix.
    try:
        with open("userlink.txt", "r", encoding="utf-8") as f:
            url = f.readline().strip()
    except Exception as e:
        print("Error reading userlink.txt:", e)
        return

    if not url:
        print("No URL found in userlink.txt")
        return

    # Generate a domain-based prefix (e.g., "en_wikipedia_org")
    parsed = urlparse(url)
    domain_prefix = parsed.netloc.replace(".", "_")

    # Define the folder and file paths for the scraped resources
    scraped_folder = "scraped_resources"
    scraped_html_file = os.path.join(scraped_folder, "index.html")
    scraped_js_file  = os.path.join(scraped_folder, "script.js")
    scraped_css_file = os.path.join(scraped_folder, "style.css")

    # Ensure the scraped folder exists
    if not os.path.exists(scraped_folder):
        print(f"Folder {scraped_folder} does not exist.")
        return

    # Ensure the files exist
    if not os.path.exists(scraped_html_file):
        print(f"File {scraped_html_file} does not exist.")
        return
    if not os.path.exists(scraped_js_file):
        print(f"File {scraped_js_file} does not exist.")
        return
    if not os.path.exists(scraped_css_file):
        print(f"File {scraped_css_file} does not exist.")
        return

    # Upload the entire folder to IPFS as a single folder
    folder_cid = upload_folder_to_ipfs(scraped_folder, scraped_folder)

    # Print out the IPFS gateway URL for the folder
    if folder_cid:
        print(f"Scraped folder IPFS URL: https://ipfs.io/ipfs/{folder_cid}")
        print(f"Scraped HTML file URL: https://ipfs.io/ipfs/{folder_cid}/index.html")
        print(f"Scraped JS file URL: https://ipfs.io/ipfs/{folder_cid}/script.js")
        print(f"Scraped CSS file URL: https://ipfs.io/ipfs/{folder_cid}/style.css")

    f=open("mirror.txt","w")
    mirror="https:ipfs.io/ipfs/"+folder_cid
    f.write(mirror)
    f.close()
if __name__ == "__main__":
    main()