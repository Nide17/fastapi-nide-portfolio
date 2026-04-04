from fastapi import FastAPI
from app.api.endpoints import projects
from app.api.endpoints import messages
from app.api.endpoints import downloads

app = FastAPI(
    title="FastAPI Nide Portfolio",
    description="Parmenide Portfolio API.",
    version="0.0.1",
)

@app.get("/health")
async def health_check():
    return {"status": "Online", "version": "0.0.1"}

# Include routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(downloads.router, prefix="/downloads", tags=["Downloads"])

@app.get("/")
async def root():
    return {"status": "Welcome to the FastAPI Nide Portfolio API!"}
