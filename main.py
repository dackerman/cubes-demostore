from fastapi import FastAPI, HTTPException
from typing import List, TypedDict
from prisma import Prisma
from prisma.partials import ProductVariantData, ProductData
from prisma.models import Product, ProductVariant
from contextlib import asynccontextmanager
import uuid


class Success(TypedDict):
    success: bool


prisma = Prisma()

@asynccontextmanager
async def startup_prisma(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

app = FastAPI(lifespan=startup_prisma)

@app.get("/products")
async def read_products() -> List[Product]:
    return await prisma.product.find_many()


@app.get("/products/{product_id}")
async def read_product(product_id: str) -> Product:
    product = await prisma.product.find_unique(where={"product_id": product_id})

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/products")
async def create_product(create_product: ProductData) -> Product:
    product = await prisma.product.create(data={
        "product_id": str(uuid.uuid4()),
        "name": create_product.name,
        "description": create_product.description,
        "image_url": create_product.image_url,
        "price": create_product.price,
    })
    return product


@app.put("/products/{product_id}")
async def update_product(product_id: str, update_product: ProductData) -> Product:
    product = await prisma.product.update(where={"product_id": product_id}, data={
        "name": update_product.name,
        "description": update_product.description,
        "image_url": update_product.image_url,
        "price": update_product.price,
    })
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: str) -> Success:
    await prisma.product.delete(where={"product_id": product_id})
    return Success(success=True)


@app.get("/products/{product_id}/variants")
async def read_product_variants(product_id: str) -> List[ProductVariant]:
    return await prisma.productvariant.find_many(where={"product_id": product_id})

@app.get("/products/{product_id}/variants/{variant_id}")
async def read_product_variant(product_id: str, variant_id: str) -> ProductVariant:
    variant = await prisma.productvariant.find_unique(where={"variant_id": variant_id})

    if variant is None:
        raise HTTPException(status_code=404, detail="Variant not found")

    return variant

@app.post("/products/{product_id}/variants")
async def create_product_variant(product_id: str, create_variant: ProductVariantData) -> ProductVariant:
    variant = await prisma.productvariant.create(data={
        "product_id": product_id,
        "variant_id": str(uuid.uuid4()),
        "name": create_variant.name,
        "price": create_variant.price,
        "image_url": create_variant.image_url,
    })
    return variant

@app.put("/products/{product_id}/variants/{variant_id}")
async def update_product_variant(product_id: str, variant_id: str, update_variant: ProductVariantData) -> ProductVariant:
    variant = await prisma.productvariant.update(
        where={"variant_id": variant_id}, 
        data={
            "name": update_variant.name,
            "price": update_variant.price,
            "image_url": update_variant.image_url
        }
    )
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

@app.delete("/products/{product_id}/variants/{variant_id}")
async def delete_product_variant(product_id: str, variant_id: str) -> Success:
    await prisma.productvariant.delete(where={"variant_id": variant_id})
    return Success(success=True)
