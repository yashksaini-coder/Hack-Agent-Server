from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from controllers.topStocks import get_top_stocks, get_stock
from controllers.stockNews import fetch_news
from controllers.stockAgent import stock_analyzer_agent, extract_json_from_response, create_default_stock_data, merge_stock_data
from fastapi.templating import Jinja2Templates
import datetime
import json

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/")
@router.head("/")
async def read_root(request: Request):
    """Root endpoint returning API server information"""
    return templates.TemplateResponse("base.html", {
        "request": request, 
        "text": "Hack AI agent Server"
    })

@router.get("/top-stocks")
async def read_top_stocks(request: Request):
    """Get top stocks in the market"""
    try:
        top_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA', 'META', 'NVDA']
        result = get_top_stocks(" ".join(top_stocks))
        
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse("route.html", {
                "request": request,
                "route_path": "/top-stocks",
                "method": "GET",
                "full_path": f"{request.url.scheme}://{request.url.netloc}/top-stocks",
                "description": "Returns information about top stocks in the market",
                "parameters": [],
                "example_response": json.dumps(result, indent=2),
                "current_year": datetime.datetime.now().year
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock-news")
async def stock_news(request: Request):
    """Get latest stock market news"""
    try:
        result = fetch_news()
        
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse("route.html", {
                "request": request,
                "route_path": "/stock-news",
                "method": "GET",
                "full_path": f"{request.url.scheme}://{request.url.netloc}/stock-news",
                "description": "Returns latest news articles related to stocks and financial markets",
                "parameters": [],
                "example_response": json.dumps(result, indent=2),
                "current_year": datetime.datetime.now().year
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock/{name}")
async def read_stock(request: Request, name: str):
    """Get detailed information for a specific stock"""
    try:
        result = get_stock(name)
        
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse("route.html", {
                "request": request,
                "route_path": f"/stock/{{{name}}}",
                "method": "GET",
                "full_path": f"{request.url.scheme}://{request.url.netloc}/stock/{name}",
                "description": "Returns detailed information about a specific stock",
                "parameters": [
                    {"name": "name", "type": "string", "description": "Stock symbol (e.g., AAPL, MSFT)"}
                ],
                "example_response": json.dumps(result, indent=2),
                "current_year": datetime.datetime.now().year
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stock-analysis/{symbol}")
async def get_stock_analysis(request: Request, symbol: str):
    """Get AI-powered analysis for a given stock symbol"""
    try:
        prompt = f"Analyze the stock {symbol} and provide detailed financial information following the specified JSON format."
        response = stock_analyzer_agent.run(prompt)
        
        result = create_default_stock_data(symbol)
        if hasattr(response, 'content'):
            json_data = extract_json_from_response(response.content)
            if json_data:
                result = merge_stock_data(result, json_data)
        
        if "text/html" in request.headers.get("accept", ""):
            return templates.TemplateResponse("route.html", {
                "request": request,
                "route_path": f"/stock-analysis/{{{symbol}}}",
                "method": "GET",
                "full_path": f"{request.url.scheme}://{request.url.netloc}/stock-analysis/{symbol}",
                "description": "Provides detailed AI-powered analysis of a stock",
                "parameters": [
                    {"name": "symbol", "type": "string", "description": "Stock symbol to analyze"}
                ],
                "example_response": json.dumps(result, indent=2),
                "current_year": datetime.datetime.now().year
            })
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
