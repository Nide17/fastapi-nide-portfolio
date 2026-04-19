from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import projects, messages, downloads, visits, users
import logging
import traceback
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from fastapi import Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="FastAPI Nide Portfolio",
    description="Parmenide Portfolio API.",
    version="0.0.1",
)


# Configure CORS to allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "Online", "version": "0.0.1"}

# Include routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(downloads.router, prefix="/downloads", tags=["Downloads"])
app.include_router(visits.router, prefix="/visits", tags=["Visits"])
app.include_router(users.router, prefix="/users", tags=["Users"])


# Global exception handlers
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logging.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed. Please try again."}
    )


@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, exc: OperationalError):
    logging.error(f"Database connection issue: {exc}")
    return JSONResponse(
        status_code=503,
        content={"detail": "Database temporarily unavailable. Try later."}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Data not processed."}
    )


@app.get("/")
async def root():
    return {"status": "Welcome to the FastAPI Nide Portfolio API!"}
