import asyncio
from functools import wraps
import time
import strawberry
from starlette.concurrency import run_in_threadpool

from strawberry.fastapi import GraphQLRouter

# credit: https://stackoverflow.com/a/50450553
def make_async(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        print(f"async, calling {f.__name__}")
        return await run_in_threadpool(f, *args, **kwargs)
    return wrapper


def hello_sync() -> str:
    time.sleep(1)
    return "Hello World"

@strawberry.type
class Query:

    @strawberry.field
    # @make_async
    def hello(self) -> str:
        time.sleep(1)
        return "Hello World"

    @strawberry.field
    async def hello_async(self) -> str:
        await asyncio.sleep(1)
        return "Hello World"

    @strawberry.field
    async def hello_sync(self) -> str:
        # TODO: the threadpool seems unbounded, compare
        # https://stackoverflow.com/a/70929141 for a bounded threadpool
        return await run_in_threadpool(hello_sync)

schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
