import requests
from bs4 import BeautifulSoup
import io
import fitz  # PyMuPDF

def get_page_urls(base_url):
    try:
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = [link['href'] for link in soup.find_all('a') if link['href'].startswith(base_url)]
        links.append(base_url)  # Include the base URL itself
        return set(links)
    except Exception as e:
        print(f"Error fetching URLs from {base_url}: {e}")
        return set()

def get_url_content(url):
    try:
        response = requests.get(url)
        if url.endswith('.pdf'):
            pdf = io.BytesIO(response.content)
            doc = fitz.open(stream=pdf, filetype="pdf")
            text = ''
            for page in doc:
                text += page.get_text()
            return (url, text)
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join(soup.stripped_strings)  # Extract text and remove extra whitespace
            return (url, text)
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return (url, "Error fetching content.")
