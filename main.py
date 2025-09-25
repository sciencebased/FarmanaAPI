from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import items

# Create FastAPI app instance
app = FastAPI(
    title="My FastAPI App",
    description="A simple FastAPI app with CORS enabled",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI App with CORS enabled!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

@app.get("/info")
async def app_info():
    return {
        "app_name": "My FastAPI App",
        "version": "1.0.0",
        "cors_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)