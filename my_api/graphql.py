import time
import strawberry

from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        time.sleep(1)
        return "Hello World"


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
