import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_website(url):
    """
    Scrapes the website at the given URL.
    Saves the full HTML, visible text, CSS (inline and external), and JavaScript (inline and external)
    into separate text files.
    Returns a tuple with the filenames: (html_filename, css_filename, js_filename, text_filename).
    """
    # Create a domain-based prefix for file names
    parsed = urlparse(url)
    domain_prefix = parsed.netloc.replace(".", "_")
    
    # Fetch the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    # Save full HTML content
    html_content = response.text
    html_filename = f"{domain_prefix}_html.txt"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Saved HTML file:", html_filename)
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract and save visible text
    text_content = soup.get_text(separator="\n")
    text_filename = f"{domain_prefix}_text.txt"
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(text_content)
    print("Saved text file:", text_filename)
    
    # Extract and save CSS code (inline + external)
    css_code = ""
    # Inline CSS from <style> tags
    for style in soup.find_all("style"):
        css_code += style.get_text() + "\n"
    # External CSS from <link rel="stylesheet"> tags
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href:
            css_url = urljoin(url, href)
            try:
                css_resp = requests.get(css_url)
                if css_resp.status_code == 200:
                    css_code += css_resp.text + "\n"
                else:
                    print("Failed to retrieve CSS from", css_url)
            except Exception as e:
                print("Error retrieving CSS from", css_url, ":", e)
    css_filename = f"{domain_prefix}_css.txt"
    with open(css_filename, "w", encoding="utf-8") as f:
        f.write(css_code)
    print("Saved CSS file:", css_filename)
    
    # Extract and save JavaScript code (inline + external)
    js_code = ""
    for script in soup.find_all("script"):
        # Inline JavaScript
        if not script.get("src"):
            js_code += script.get_text() + "\n"
        else:
            src = script.get("src")
            js_url = urljoin(url, src)
            try:
                js_resp = requests.get(js_url)
                if js_resp.status_code == 200:
                    js_code += js_resp.text + "\n"
                else:
                    print("Failed to retrieve JS from", js_url)
            except Exception as e:
                print("Error retrieving JS from", js_url, ":", e)
    js_filename = f"{domain_prefix}_js.txt"
    with open(js_filename, "w", encoding="utf-8") as f:
        f.write(js_code)
    print("Saved JS file:", js_filename)
    
    return html_filename, css_filename, js_filename, text_filename

def main():
    # Read URL from userlink.txt
    try:
        with open("userlink.txt", "r", encoding="utf-8") as f:
            url = f.readline().strip()
    except Exception as e:
        print("Error reading userlink.txt:", e)
        return
    
    if not url:
        print("No URL found in userlink.txt")
        return
    
    print("Scraping URL:", url)
    result = scrape_website(url)
    if result is None:
        return
    print("Scraping completed.")

if __name__ == "__main__":
    main()
