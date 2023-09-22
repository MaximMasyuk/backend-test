from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import api_v1_router

app = FastAPI(title="Python services")

app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
def add_process_time_header(request: Request, call_next):
    response = call_next(request)
    return response
