![High Level Overview](images/thumbnail.png)
# Google Dork Email Extractor Tool

## Overview

This repository contains a Python-based tool designed to automate the process of searching for and extracting emails from web pages using Google dorks. The tool performs a Google search for a specific domain, downloads the resulting pages, and extracts emails matching the domain suffix.

## Features

- **Google Search Automation**: Automatically performs Google searches for a specified domain using a custom dork.
- **Page Downloading**: Downloads and saves HTML content from search results.
- **Email Extraction**: Parses the downloaded pages to extract email addresses matching the specified domain.
- **Recursive Link Downloading**: Extracts and downloads pages linked from the initial search results to find additional emails.

## Requirements

- Python 3.x
- `requests`, `beautifulsoup4`, and `argparse` libraries

You can install the required packages using the following command:

```bash
pip install requests beautifulsoup4 argparse
```

## Usage

To run the tool, follow these steps:

1. **Make the script executable**:
   ```bash
   chmod +x emailharvester.py
   ```

2. **Run the script**:
   ```bash
   ./emailharvester.py --domain <domain_suffix> --max_results <number_of_results> --output_folder <folder_name>
   ```

### Arguments

- `--domain (-d)`: The domain suffix to search for (e.g., `nitj.ac.in`).
- `--max_results (-m)`: The number of Google search results to process (default: 30).
- `--output_folder (-o)`: The folder to save downloaded pages (default: `downloaded_pages`).

### Example

```bash
./emailharvester.py -d example.com -m 50 -o my_downloads
```

## Enhancements and Best Practices


The tool now includes several improvements to enhance scraping reliability:

1. **SSL Pinning** – verifies the server certificate against a pinned fingerprint.
2. **User-Agent Rotation** – requests use a random User-Agent string.
3. **Proxy Support** – provide a file of proxies to rotate source IPs.
4. **Rate Limiting** – random delays help mimic human browsing.
5. **Logging** – all actions are written to `emailharvester.log`.

For more demanding scenarios, consider adding CAPTCHA solving, browser automation or multi-threading for better performance.

## Disclaimer

This tool is intended for educational purposes only. The author is not responsible for any misuse of the tool. Always ensure you have permission before scraping or downloading content from any website.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
