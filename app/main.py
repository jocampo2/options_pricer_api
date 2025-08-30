from fastapi import FastAPI
from .routes import router
import uvicorn

app = FastAPI(
    title="Black-Scholes Option Pricing API",
    description="Compute option prices using the Black-Scholes model (vectorized).",
    version="1.0.0",
    docs_url="/",       
    redoc_url=None      
)

app.include_router(router, prefix="/api", tags=["options"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)