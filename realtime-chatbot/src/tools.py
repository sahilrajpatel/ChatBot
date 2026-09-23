import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# free search tool, no API key needed
search = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the internet for real-time / current information like news,
    prices, weather, scores, latest updates etc. Use this when the question
    needs up-to-date info that you don't already know."""
    return search.run(query)


@tool
def read_website(url: str) -> str:
    """Fetch and read the text content of a specific website URL the user
    gives you. Use this when the user shares a link or asks about a
    particular website."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove script/style tags so we don't get junk text
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]  # keep it short so it doesn't blow up the context

    except Exception as e:
        return f"Could not fetch the website. Error: {e}"


TOOLS = [web_search, read_website]
