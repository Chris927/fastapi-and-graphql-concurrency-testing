import asyncio
from fastapi import FastAPI

from .graphql import graphql_app

app = FastAPI()

@app.get("/hello")
async def hello():
    await asyncio.sleep(1)
    return {"message": "Hello World"}

app.include_router(graphql_app, prefix="/graphql")
