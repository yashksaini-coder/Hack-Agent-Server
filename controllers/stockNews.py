import os
import httpx
import json
import re
from bs4 import BeautifulSoup
from typing import Dict, Any
from dotenv import load_dotenv

# AI assistant imports
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")

def scrape_url(url: str) -> str:
    """Scrape the content of a given URL and return the text.
    Use this to get more detail about a specific news story after finding it via search.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        return text[:3000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# Instructions for JSON output
json_instructions = [
    "Search for the latest and most relevant news articles related to stocks and financial markets.",
    "For the most promising articles, you can use the `scrape_url` tool to get more depth.",
    "Analyze the news to determine the sentiment (Positive, Negative, or Neutral).",
    "You MUST format your response as a valid JSON object with an 'articles' key containing a list of objects.",
    "Each article object MUST have: 'title', 'url', 'source', 'summary', 'sentiment', and 'published_date'.",
    "Do not include any text before or after the JSON object.",
    "Example format:",
    '{"articles": [{"title": "...", "url": "...", "source": "...", "summary": "...", "sentiment": "...", "published_date": "..."}]}'
]

# News agent using Groq without formal response_model to avoid conflict with tools
news_agent = Agent(
    name="Stock News Agent",
    role="Expert financial news researcher and analyst",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),
    tools=[
        DuckDuckGoTools(search=True, news=True),
        WikipediaTools(),
        scrape_url
    ],
    instructions=json_instructions,
)

def extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON from the agent's response."""
    try:
        # Try to find JSON block
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(text)
    except Exception:
        return {"articles": []}

def fetch_news():
    """Fetch and present latest news articles related to stocks and financial markets"""
    try:
        response = news_agent.run("Latest news articles related to stocks and financial markets")
        
        content = ""
        if hasattr(response, 'content'):
            content = response.content
            
        result = extract_json(content)
        return result
    except Exception as e:
        raise RuntimeError(f"Error fetching news: {str(e)}")
