#!/usr/bin/env python3

import os
import re
import requests
import urllib3
import certifi
from bs4 import BeautifulSoup
import time
import argparse
from urllib3.util.ssl_ import create_urllib3_context
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import ssl

# Disable warnings for unverified HTTPS requests (optional, not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to perform a Google search and return the HTML content of the search results
def google_search(query, start=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}&start={start}"
    
    # SSL verification using certifi's CA bundle
    response = requests.get(url, headers=headers, verify=certifi.where())
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve Google search results (Status Code: {response.status_code})")
        return None

# Function to download and save pages based on URLs found
def download_pages(query, max_results=10, output_folder='downloaded_pages'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    downloaded_files = []
    visited_urls = set()
    results_per_page = 10  # Google shows 10 results per page
    start = 0

    while len(downloaded_files) < max_results:
        search_html = google_search(query, start)
        if not search_html:
            break

        soup = BeautifulSoup(search_html, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            url = link['href']
            if url.startswith('/url?q='):
                url = url.split('/url?q=')[1].split('&')[0]

            if url.startswith('http') and url not in visited_urls:
                visited_urls.add(url)
                try:
                    # SSL verification using certifi's CA bundle
                    response = requests.get(url, verify=certifi.where())
                    if response.status_code == 200:
                        file_name = f"page_{len(downloaded_files) + 1}.html"
                        file_path = os.path.join(output_folder, file_name)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        downloaded_files.append(file_path)
                        print(f"Downloaded: {url}")
                        # Extract links and download them
                        extract_and_download_links(response.text, visited_urls, output_folder)
                    else:
                        print(f"Failed to download {url} (Status Code: {response.status_code})")
                except Exception as e:
                    print(f"Error downloading {url}: {e}")

            if len(downloaded_files) >= max_results:
                break

        # Move to the next page of Google search results
        start += results_per_page
        time.sleep(2)  # Add a delay to avoid being blocked by Google

    return downloaded_files

# Function to extract links and download them
def extract_and_download_links(html_content, visited_urls, output_folder):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    for link in links:
        url = link['href']
        if url.startswith('http') and url not in visited_urls:
            visited_urls.add(url)
            try:
                # SSL verification using certifi's CA bundle
                response = requests.get(url, verify=certifi.where())
                if response.status_code == 200:
                    file_name = f"page_{len(visited_urls)}.html"
                    file_path = os.path.join(output_folder, file_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"Downloaded linked page: {url}")
                else:
                    print(f"Failed to download {url} (Status Code: {response.status_code})")
            except Exception as e:
                print(f"Error downloading {url}: {e}")

# Function to extract emails from downloaded pages
def extract_emails_from_pages(files, domain_suffix):
    emails = set()
    email_pattern = re.compile(rf'\b[A-Za-z0-9._%+-]+@{domain_suffix}\b')

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()
            found_emails = re.findall(email_pattern, text)
            emails.update(found_emails)

    return emails

# Function to verify SSL certificate and check against the pinned fingerprint
def verify_pinned_certificate(cert_der_bytes, pinned_fingerprint):
    # Parse the certificate
    cert = x509.load_der_x509_certificate(cert_der_bytes, default_backend())
    
    # Extract the public key bytes
    public_key_bytes = cert.public_key().public_bytes(
        encoding=ssl.Encoding.DER,
        format=ssl.PublicFormat.SubjectPublicKeyInfo
    )

    # Calculate the hash (fingerprint) of the public key
    cert_fingerprint = hashes.Hash(hashes.SHA256(), backend=default_backend())
    cert_fingerprint.update(public_key_bytes)
    cert_fingerprint_hex = cert_fingerprint.finalize().hex()

    # Compare the fingerprint with your pinned fingerprint
    if cert_fingerprint_hex != pinned_fingerprint:
        raise ssl.SSLError("Certificate pinning validation failed!")
    print("Certificate pinning validation successful.")

# Create a custom HTTPSConnection that performs pinning
class PinnedHTTPSConnection(urllib3.connection.HTTPSConnection):
    def connect(self):
        # Establish connection using normal SSL handshake
        super().connect()

        # Extract the peer certificate
        peer_cert = self.sock.getpeercert(binary_form=True)
        
        # Verify the certificate using the pinned fingerprint
        verify_pinned_certificate(peer_cert, CERTIFICATE_FINGERPRINT)

# Create a custom PoolManager that uses the PinnedHTTPSConnection
class PinnedHTTPAdapter(urllib3.PoolManager):
    def __init__(self, *args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1_2  # Ensure latest SSL/TLS
        super().__init__(*args, **kwargs)
        # Override the connection_cls to use the PinnedHTTPSConnection
        self.connection_cls = PinnedHTTPSConnection

# Function to extract server certificate and generate its fingerprint
def get_certificate_fingerprint(domain):
    conn = urllib3.connection_from_url(f'https://{domain}')
    conn.connect()

    # Extract the certificate
    cert = conn.sock.getpeercert(binary_form=True)

    # Parse and calculate the fingerprint of the certificate
    public_key = x509.load_der_x509_certificate(cert, default_backend()).public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=ssl.Encoding.DER,
        format=ssl.PublicFormat.SubjectPublicKeyInfo
    )

    sha256_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256_hash.update(public_key_bytes)
    fingerprint = sha256_hash.finalize().hex()

    print(f"Extracted Certificate Fingerprint: {fingerprint}")
    return fingerprint

# Main function to orchestrate the process
def main():
    parser = argparse.ArgumentParser(description="Google Dork Email Extractor Tool")
    parser.add_argument('-d', '--domain', type=str, required=True, help='Domain suffix to search for (e.g., nitj.ac.in)')
    parser.add_argument('-m', '--max_results', type=int, default=30, help='Number of Google search results to process (default: 30)')
    parser.add_argument('-o', '--output_folder', type=str, default='downloaded_pages', help='Folder to save downloaded pages (default: downloaded_pages)')

    args = parser.parse_args()

    global CERTIFICATE_FINGERPRINT
    CERTIFICATE_FINGERPRINT = get_certificate_fingerprint(args.domain)

    dork = f'site:{args.domain} intext:"@{args.domain}"'
    print(f"Using dork: {dork}")
    downloaded_files = download_pages(dork, args.max_results, args.output_folder)

    print("\nExtracting emails...")
    emails = extract_emails_from_pages(downloaded_files, args.domain)

    print(f"\nFound {len(emails)} emails:")
    for email in sorted(emails):
        print(email)

if __name__ == '__main__':
    main()
