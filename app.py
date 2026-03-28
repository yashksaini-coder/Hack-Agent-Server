from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import datetime
from routes.stockRoutes import router as stock_router
from routes.agentRoutes import router as agent_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 405:  # Method Not Allowed
        path = request.url.path
        current_year = datetime.datetime.now().year
        return templates.TemplateResponse(
            "post.html",
            {
                "request": request,
                "route_path": path,
                "full_path": str(request.url),
                "description": "This endpoint requires a different HTTP method than the one used.",
                "current_year": current_year,
                "example_query": "{}"
            },
            status_code=405
        )
    # For other HTTP exceptions, return a JSON response or the default behavior
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "message": str(exc)},
    )

app.include_router(stock_router)
app.include_router(agent_router)



