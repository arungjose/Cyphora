import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import socks
import socket
from urllib.parse import urljoin
import os
import re

def set_proxy():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    print("[🔥] TOR Proxy Activated")

def scrape_website(url, output_dir="scraped_resources"):
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    try:
        set_proxy()
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            print("[✅] Website Accessible!")
            soup = BeautifulSoup(response.text, "html.parser")
        else:
            print(f"[❌] Failed with Status Code: {response.status_code}")
            return None
    except Exception as e:
        print("[⚠️] Proxy Error:", e)
        return None

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save HTML
    html_filename = os.path.join(output_dir, "index.html")
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    print("Saved HTML file:", html_filename)

    # Extract and save CSS code (inline + external)
    css_code = ""
    for style in soup.find_all("style"):
        css_code += style.get_text() + "\n"
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
    css_filename = os.path.join(output_dir, "style.css")
    with open(css_filename, "w", encoding="utf-8") as f:
        f.write(css_code)
    print("Saved CSS file:", css_filename)

    # Extract and save JavaScript code (inline + external)
    js_code = ""
    js_urls = [] #store js urls
    for script in soup.find_all("script"):
        if not script.get("src"):
            js_code += script.get_text() + "\n"
        else:
            src = script.get("src")
            js_url = urljoin(url, src)
            js_urls.append(js_url) #add to list
            try:
                js_resp = requests.get(js_url)
                if js_resp.status_code == 200:
                    js_code += js_resp.text + "\n"
                else:
                    print("Failed to retrieve JS from", js_url)
            except Exception as e:
                print("Error retrieving JS from", js_url, ":", e)
    js_filename = os.path.join(output_dir, "script.js")
    with open(js_filename, "w", encoding="utf-8") as f:
        f.write(js_code)
    print("Saved JS file:", js_filename)
    #check js files for window.location.href
    for js_url in js_urls:
        try:
            js_resp = requests.get(js_url)
            if js_resp.status_code == 200:
                js_content = js_resp.text
                matches = re.findall(r"window\.location\.href\s*=\s*['\"](.*?)['\"]", js_content)
                for match in matches:
                    redirect_url = urljoin(url, match)
                    print(f"Found redirect URL: {redirect_url}")
                    scrape_website(redirect_url, output_dir) #recursively scrape
        except Exception as e:
            print(f"Error checking JS redirects from {js_url}: {e}")

    return html_filename, css_filename, js_filename

def main():
    try:
        with open("user_links.txt", "r", encoding="utf-8") as f:
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