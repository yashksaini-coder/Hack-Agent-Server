import os
import datetime
import json
import requests
from fastapi import APIRouter, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agno.agent import RunResponse
from controllers.agent import multi_agent
import dotenv
import groq

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str

router = APIRouter()
templates = Jinja2Templates(directory="templates")

dotenv.load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
groq_client = groq.Client(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("Please provide a GROQ API key")

start_time = datetime.datetime.now(datetime.timezone.utc)

@router.get("/health", response_class=HTMLResponse)
async def health_check(request: Request):
    """Health check endpoint to verify the API server status and connections."""
    uptime = (datetime.datetime.now(datetime.timezone.utc) - start_time).total_seconds()
    try:
        response_data = {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "uptime": "OK",
            "uptime_seconds": uptime,
            "api": {
                "groq_api": "connected" if GROQ_API_KEY else "not configured",
                "gemini_api":"connected" if GEMINI_API_KEY else "not configured",
            },
            "ip": requests.get('https://api.ipify.org').text,

        }

        # Check if request is from a browser or format is explicitly set to html
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            current_year = datetime.datetime.now().year
            return templates.TemplateResponse(
                "route.html",
                {
                    "request": request,
                    "route_path": "/health",
                    "method": "GET",
                    "full_path": str(request.url).split("?")[0],
                    "description": "Health check endpoint to verify the API server status and connections.",
                    "parameters": [
                        {"name": "format", "type": "string", "description": "Response format (html or json)"}
                    ],
                    "example_query": "",
                    "example_response": json.dumps(response_data, indent=2),
                    "current_year": current_year
                }
            )

        return JSONResponse(content=response_data)

    except Exception as e:
        error_response = {
            "status": "unhealthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": str(e)
        }

        # Check if request is from a browser or format is explicitly set to html
        accept_header = request.headers.get("accept", "")
        if "text/html" in accept_header:
            current_year = datetime.datetime.now().year
            return templates.TemplateResponse(
                "route.html",
                {
                    "request": request,
                    "route_path": "/health",
                    "method": "GET",
                    "full_path": str(request.url).split("?")[0],
                    "description": "Health check endpoint to verify the API server status and connections.",
                    "parameters": [
                        {"name": "format", "type": "string", "description": "Response format (html or json)"}
                    ],
                    "example_query": "",
                    "example_response": json.dumps(error_response, indent=2),
                    "current_year": current_year
                }
            )

        return JSONResponse(content=error_response)

@router.post("/agent", response_class=HTMLResponse, name="agent")
async def agent(request: Request, payload: QueryRequest = Body(...)):
    """
    API endpoint to handle user investment-related questions via POST request body
    and return AI-generated insights.
    """
    query = payload.query
     # Check if request is from a browser or format is explicitly set to html
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        current_year = datetime.datetime.now().year
        example_response = {
            "question": "Should I invest in index funds?",
            "answer": "Index funds are often a good choice for passive investors looking for broad market exposure with low fees. They offer diversification and typically outperform actively managed funds in the long term. However, the suitability depends on your investment goals, time horizon, and risk tolerance."
        }
        example_request_body = {"query": "Should I invest in index funds?"}

        return templates.TemplateResponse(
            "route.html",
            {
                "request": request,
                "route_path": "/agent",
                "method": "POST",
                "full_path": str(request.url).split("?")[0],
                "description": "Agent endpoint that uses a multi-AI system to provide sophisticated investment advice. Accepts a JSON body with a 'query' field.",
                "parameters": [
                    {"name": "Request Body", "type": "JSON", "description": "JSON object containing the 'query' field."},
                    {"name": "format", "type": "string", "description": "Response format (html or json)"}
                ],
                "example_query": json.dumps(example_request_body, indent=2), # Show example request body
                "example_response": json.dumps(example_response, indent=2),
                "current_year": current_year
            }
        )

    if not query:
        # This check might be redundant if QueryRequest enforces the field, but kept for clarity
        return JSONResponse(content={"error": "Query field in request body is required"}, status_code=400)

    try:
        response: RunResponse = multi_agent.run(query)
        answer = response.content
        return JSONResponse(content={"question": query, "answer": answer})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, payload: QueryRequest = Body(...)):
    """
    API endpoint to handle user investment-related questions via POST request body
    and return AI-generated insights using Groq's LLaMa model.
    """
    query = payload.query
    # Check if request is from a browser or format is explicitly set to html
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        current_year = datetime.datetime.now().year
        example_response = {
            "question": "What are good tech stocks to invest in?",
            "answer": "Some popular tech stocks to consider include Apple (AAPL), Microsoft (MSFT), Google (GOOGL), and Amazon (AMZN). However, you should always do your own research and consider your investment goals and risk tolerance before investing."
        }
        example_request_body = {"query": "What are good tech stocks to invest in?"}

        return templates.TemplateResponse(
            "route.html",
            {
                "request": request,
                "route_path": "/chat",
                "method": "GET",  # Changed to GET since we're just displaying info
                "full_path": str(request.url).split("?")[0],
                "description": "Chat endpoint that uses Groq's LLaMa model to answer investment questions. For actual queries, use POST with a JSON body containing a 'query' field.",
                "parameters": [
                    {"name": "format", "type": "string", "description": "Response format (html or json)"}
                ],
                "example_query": "Using POST: " + json.dumps(example_request_body, indent=2),
                "example_response": json.dumps(example_response, indent=2),
                "current_year": current_year
            }
        )

    # Handle regular API calls
    if not query:
        # This check might be redundant if QueryRequest enforces the field, but kept for clarity
        return JSONResponse(content={"error": "Query field in request body is required"}, status_code=400)

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are an AI investment assistant."},
                      {"role": "user", "content": query}]
        )

        answer = response.choices[0].message.content
        return JSONResponse(content={"question": query, "answer": answer})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
