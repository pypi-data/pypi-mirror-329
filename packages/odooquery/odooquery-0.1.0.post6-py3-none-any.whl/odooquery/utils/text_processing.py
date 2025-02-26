from bs4 import BeautifulSoup

def strip_html(text: str) -> str:
    """Remove HTML tags from text while preserving structure."""
    if not text:
        return ""

    soup = BeautifulSoup(text, 'html.parser')

    # Replace <br> and </p> with newlines
    for br in soup.find_all(['br', 'p']):
        br.replace_with('\n' + br.text)

    return soup.get_text().strip()
