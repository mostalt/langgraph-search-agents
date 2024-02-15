import requests

from langchain.tools import tool
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup


@tool("internet_search", return_direct=False)
def internet_search(query: str) -> str:

  """Searches the internet using DuckDuckGo."""

  with DDGS() as ddgs:
    results = [r for r in ddgs.text(query, max_results=5)]
    return results if results else "No results found."

@tool("process_content", return_direct=False)
def process_content(url: str) -> str:

    """Processes content from a webpage."""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def get_tools():
  return [internet_search, process_content]