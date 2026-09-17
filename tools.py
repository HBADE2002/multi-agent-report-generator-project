from langchain.tools import tool
import requests 
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os

from rich import print
load_dotenv()

#tool 1 - fetch data from tavily

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str):
    """
    search the web for recent and realible info on a topic. returns titles, urls, snippets 

    """
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:800]}\n"
        )
    return "\n----\n".join(out)


#tool 2 - goto the url that is recieved from 
# tavily and fetch the content of the page and 
# return it as a string using beautifulsoup

@tool
def scrape_url(url: str):
    """
    Scrape and return clean text content from the given url for deeper thinking.
    Returns a string starting with 'SCRAPE_FAILED' if the page couldn't be fetched
    or didn't have enough usable content — try a different URL in that case.
    """
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code != 200:
            return f"SCRAPE_FAILED status={resp.status_code} for {url}"
        soup = BeautifulSoup(resp.content, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        if len(text) < 200:
            return f"SCRAPE_FAILED insufficient content for {url}"
        return text[:5000]
    except Exception as e:
        return f"SCRAPE_FAILED error={e} for {url}"