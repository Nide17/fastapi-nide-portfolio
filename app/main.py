from fastapi import FastAPI
from app.api.endpoints import projects
from app.api.endpoints import messages

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

@app.get("/")
async def root():
    return {"status": "Welcome to the FastAPI Nide Portfolio API!"}
