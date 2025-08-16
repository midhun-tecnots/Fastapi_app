import strawberry
from typing import List
from strawberry.fastapi import GraphQLRouter

from app.db.session import get_db
from app.db import models


@strawberry.type
class ProductType:
    id: int
    name: str
    description: str
    price: float


@strawberry.type
class Query:
    @strawberry.field
    def products(self, info) -> List[ProductType]:
        db = next(get_db())
        items = db.query(models.Product).all()
        return [ProductType(id=i.id, name=i.name, description=i.description, price=float(i.price)) for i in items]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def noop(self) -> bool:
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)
