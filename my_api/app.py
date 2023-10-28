import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def hello():
    await asyncio.sleep(1)
    return {"message": "Hello World"}


