from fastapi import FastAPI, HTTPException
from typing import Dict, List, TypedDict
from pydantic import BaseModel
import json
import random
import string


class Product(BaseModel):
    id: str
    name: str
    description: str
    image_url: str
    price: float

class CreateProduct(BaseModel):
    name: str
    description: str
    image_url: str
    price: float

class UpdateProduct(BaseModel):
    name: str
    description: str
    image_url: str
    price: float


class ProductVariantFields(BaseModel):
    name: str
    addl_price: float
    image_url: str

class ProductVariant(ProductVariantFields):
    id: str
    product_id: str


class DB(TypedDict):
    products: Dict[str, Product]
    variants: Dict[str, ProductVariant]

class Success(TypedDict):
    success: bool


db: DB= {
    "products": {},
    "variants": {}
}

app = FastAPI()

@app.get("/products")
async def read_products() -> List[Product]:
    return list(db["products"].values())


@app.get("/products/{product_id}")
async def read_product(product_id: str) -> Product:
    product = db["products"][product_id]
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products")
async def create_product(create_product: CreateProduct) -> Product:
    newid = generate_id()
    product = Product(id=newid, **create_product.model_dump())
    db["products"][product.id] = product
    return product


@app.put("/products/{product_id}")
async def update_product(product_id: str, update_product: UpdateProduct) -> Product:
    if product_id not in db["products"]:
        raise HTTPException(status_code=404, detail="Product not found")
    product = db["products"][product_id].model_copy(update=update_product.model_dump())
    db["products"][product_id] = product
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: str) -> Success:
    if product_id not in db["products"]:
        raise HTTPException(status_code=404, detail="Product not found")
    del db["products"][product_id]
    return Success(success=True)


@app.get("/products/{product_id}/variants")
async def read_product_variants(product_id: str) -> List[ProductVariant]:
    return list(filter(lambda variant: variant.product_id == product_id, db["variants"].values()))

@app.get("/products/{product_id}/variants/{variant_id}")
async def read_product_variant(product_id: str, variant_id: str) -> ProductVariant:
    variant = db["variants"].get(variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

@app.post("/products/{product_id}/variants")
async def create_product_variant(product_id: str, create_variant: ProductVariantFields) -> ProductVariant:
    newid = generate_id()
    variant = ProductVariant(product_id=product_id, id=newid, **create_variant.model_dump())
    db["variants"][variant.id] = variant
    return variant

@app.put("/products/{product_id}/variants/{variant_id}")
async def update_product_variant(product_id: str, variant_id: str, update_variant: ProductVariantFields) -> ProductVariant:
    if variant_id not in db["variants"]:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant = db["variants"][variant_id].model_copy(update=update_variant.model_dump())
    db["variants"][variant_id] = variant
    return variant

@app.delete("/products/{product_id}/variants/{variant_id}")
async def delete_product_variant(product_id: str, variant_id: str) -> Success:
    if variant_id not in db["variants"]:
        raise HTTPException(status_code=404, detail="Variant not found")
    del db["variants"][variant_id]
    return Success(success=True)


def load():
    global db
    try:
        with open("db.json", "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        pass

def save():
    global db
    with open("db.json", "w") as f:
        json.dump(db, f)


def generate_id(length: int=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))