import os
from dotenv import load_dotenv
from textwrap import dedent

# AI assistant imports
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")

# Build the tools list: use Tavily for web search when available, else DuckDuckGo
_search_tools = []
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY:
    from agno.tools.tavily import TavilyTools

    _search_tools.append(
        TavilyTools(
            api_key=TAVILY_API_KEY,
            search=True,
            max_tokens=8000,
            search_depth="advanced",
            format="markdown",
        )
    )
else:
    _search_tools.append(DuckDuckGoTools())

# Initialize the financial analysis agent
multi_agent = Agent(
    name="Financial Analysis Agent",
    role="Analyze financial metrics and provide insights.",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    tools=[YFinanceTools(enable_all=True), *_search_tools],
    instructions=dedent("""\
        You are a financial analyst. Your task is to retrieve and analyze financial data about stocks.
        Search for the most relevant and recent information when needed.
        Present the data in a structured format, including key metrics and insights.
    """),
    markdown=True,
)
