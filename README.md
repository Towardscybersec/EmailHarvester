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

## TODO: Enhancements and Best Practices

This section provides suggestions to enhance the tool's capabilities, making it a more powerful email harvester:

1. **Advanced SSL Bypassing**:
    - Implement SSL certificate pinning techniques or use libraries like `urllib3` to better handle SSL certificate verification bypassing.

2. **Handling CAPTCHA Challenges**:
    - Integrate CAPTCHA solving services (e.g., 2Captcha) to automatically bypass Google's CAPTCHA challenges.
    - Use headless browsers like Selenium with anti-detection techniques to reduce the chances of triggering CAPTCHA.

3. **User-Agent Rotation**:
    - Implement random User-Agent rotation or use libraries like `fake_useragent` to mimic different browsers and reduce detection risk.
    - Introduce random delays and request intervals to simulate human browsing behavior.

4. **Proxies and Tor Network**:
    - Use rotating proxies or the Tor network to anonymize requests and avoid IP blocking.
    - Consider implementing a proxy pool to distribute requests across multiple IPs.

5. **Advanced Parsing**:
    - Improve the email extraction process by using advanced regular expressions or natural language processing (NLP) techniques to better identify and extract emails.
    - Add functionality to extract additional data like phone numbers or social media handles.

6. **Multi-Threading**:
    - Implement multi-threading or asynchronous processing to speed up page downloading and email extraction, especially when dealing with a large number of results.

7. **Error Handling and Logging**:
    - Enhance error handling to manage network issues, timeouts, and unexpected server responses more gracefully.
    - Introduce detailed logging for monitoring the tool's performance and diagnosing issues.

8. **Browser Emulation**:
    - Integrate browser emulation using tools like Playwright or Puppeteer to render JavaScript-heavy pages and scrape dynamically loaded content.

9. **Rate Limiting**:
    - Introduce rate-limiting to avoid triggering anti-bot mechanisms and ensure compliance with Google's terms of service.

10. **Extensive Testing**:
    - Conduct thorough testing across different domains and search environments to ensure the tool's robustness and effectiveness.

## Disclaimer

This tool is intended for educational purposes only. The author is not responsible for any misuse of the tool. Always ensure you have permission before scraping or downloading content from any website.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
