from bs4 import BeautifulSoup
import re

def clean_query(query: str) -> str:
    """
    Cleans and formats the customer support query before sending it to Gemini.

    Args:
        query (str): The original customer support query.

    Returns:
        str: The cleaned and formatted query.
    """
    # Remove leading and trailing whitespace
    cleaned_query = query.strip()

    # Optionally, add more processing steps here (e.g., removing special characters)

    return cleaned_query

def strip_html(text: str) -> str:
    """
    Strip HTML tags and decode HTML entities from text.

    Args:
        text (str): Text that may contain HTML

    Returns:
        str: Clean text without HTML
    """
    if not text:
        return ""

    # Parse with BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')

    # Get text content
    text = soup.get_text(separator=' ', strip=True)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()