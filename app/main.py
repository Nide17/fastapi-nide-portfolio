from fastapi import FastAPI
from app.api.endpoints import projects, messages, downloads, visits, users

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
app.include_router(visits.router, prefix="/visits", tags=["Visits"])
app.include_router(users.router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {"status": "Welcome to the FastAPI Nide Portfolio API!"}
