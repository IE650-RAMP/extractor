import os
import time
import requests
from bs4 import BeautifulSoup

# Set up headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

QUERY = 'Modulkatalog OR "Module Catalog" filetype:pdf site:uni-mannheim.de'
DOWNLOAD_DIR = './downloads'
BASE_URL = 'https://www.google.com/search?q='
PDF_LINKS = []
START_PAGE = 25
END_PAGE = 35


def get_google_search_results(query, start):
    """Fetch Google search results starting from the given result index."""
    query = query.replace(' ', '+')
    url = f'{BASE_URL}{query}&start={start}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to retrieve Google results: {response.status_code}")
        return None
    return response.text


def parse_search_results(html):
    """Parse search results and extract PDF links."""
    soup = BeautifulSoup(html, 'lxml')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        print(href)
        # Google wraps actual URLs like "/url?q=https://..."
        if ".pdf" in href:
            # Extract the actual link after "/url?q="
            print(href)
            link = href
            links.append(link)
    return links


def download_pdf(pdf_url, download_dir):
    """Download a single PDF from the URL."""
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            filename = os.path.join(download_dir, pdf_url.split("/")[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {pdf_url}")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")


def crawl_and_download_pdfs(query, max_pages, download_dir):
    """Crawl Google search results and download PDFs."""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    start_index = 0
    for page in range(START_PAGE, END_PAGE):
        print(f"Crawling page {page + 1}...")

        # Fetch the search results for the current page
        html = get_google_search_results(query, start_index)
        if not html:
            break

        # Parse the search results to extract PDF links
        pdf_links = parse_search_results(html)
        if not pdf_links:
            print("No more PDF links found.")
            break

        PDF_LINKS.extend(pdf_links)

        # Download each PDF found
        for pdf_link in pdf_links:
            print(f"Found PDF: {pdf_link}")
            download_pdf(pdf_link, download_dir)

        # Wait to avoid being blocked by Google
        time.sleep(10)

        # Update the start index for the next page of results
        start_index += 10


if __name__ == "__main__":
    crawl_and_download_pdfs(QUERY, END_PAGE, DOWNLOAD_DIR)
