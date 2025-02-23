from fastapi import FastAPI

app = FastAPI(title="QuantGPT Local Runner")

@app.get("/")
async def root():
    return {"message": "Hello from QuantGPT Local Runner"}