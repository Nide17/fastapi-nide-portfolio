from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Nide Portfolio",
    description="Parmenide Portfolio API.",
    version="0.0.1",
)

@app.get("/health")
async def health_check():
    return {"status": "Online", "version": "0.0.1"}
