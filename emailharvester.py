#!/usr/bin/env python3

import os
import re
import requests
from bs4 import BeautifulSoup
import time
import argparse

# Function to perform a Google search and return the HTML content of the search results
def google_search(query, start=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query}&start={start}"
    response = requests.get(url, headers=headers, verify=False)
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
                    # Bypassing SSL certificate verification
                    response = requests.get(url, verify=False)
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
                # Bypassing SSL certificate verification
                response = requests.get(url, verify=False)
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

# Function to parse downloaded pages and extract emails
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

# Main function to orchestrate the process
def main():
    parser = argparse.ArgumentParser(description="Google Dork Email Extractor Tool")
    parser.add_argument('-d', '--domain', type=str, required=True, help='Domain suffix to search for (e.g., nitj.ac.in)')
    parser.add_argument('-m', '--max_results', type=int, default=30, help='Number of Google search results to process (default: 30)')
    parser.add_argument('-o', '--output_folder', type=str, default='downloaded_pages', help='Folder to save downloaded pages (default: downloaded_pages)')

    args = parser.parse_args()

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
