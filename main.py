from fastapi import FastAPI
from typing import List, TypedDict
from pydantic import BaseModel
import json


class Product(BaseModel):
    id: str
    name: str
    description: str
    image_url: str
    price: float


class ProductVariant(BaseModel):
    id: str
    product_id: str
    name: str
    price: float


class DB(TypedDict):
    products: List[Product]
    variants: List[ProductVariant]


db: DB= {
    "products": [],
    "variants": []
}

app = FastAPI()

@app.get("products")
async def read_products() -> List[Product]:
    return db["products"]


@app.get("/products/{product_id}")
async def read_product(product_id):
    return {"product_id": product_id}


@app.post("/products")
async def create_product(product: Product):
    return product


@app.put("/products/{product_id}")
async def update_product(product_id, product: Product):
    return {"product_id": product_id, "product": product}


@app.get("/products/{product_id}/variants")
async def read_product_variants(product_id):
    return []

@app.get("/products/{product_id}/variants/{variant_id}")
async def read_product_variant(product_id, variant_id):
    return {"product_id": product_id, "variant_id": variant_id}

@app.post("/products/{product_id}/variants")
async def create_product_variant(product_id, variant: ProductVariant):
    return {"product_id": product_id, "variant": variant}

@app.put("/products/{product_id}/variants/{variant_id}")
async def update_product_variant(product_id, variant_id, variant: ProductVariant):
    return {"product_id": product_id, "variant_id": variant_id, "variant": variant}


def load():
    global db
    try:
        with open("db.json", "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}

def save():
    global db
    with open("db.json", "w") as f:
        json.dump(db, f)