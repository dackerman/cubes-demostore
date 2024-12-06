from fastapi import FastAPI, HTTPException
from typing import Dict, List, TypedDict
from prisma import Prisma
from prisma.types import ProductCreateInput, ProductUpdateInput, ProductVariantCreateInput, ProductVariantUpdateInput
from prisma.partials import ProductVariantData, ProductData
from prisma.models import Product, ProductVariant
from contextlib import asynccontextmanager


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
async def read_product(product_id: int) -> Product:
    product = await prisma.product.find_unique(where={"id": product_id})

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/products")
async def create_product(create_product: ProductData) -> Product:
    product = await prisma.product.create(data={
        "name": create_product.name,
        "description": create_product.description,
        "image_url": create_product.image_url,
        "price": create_product.price,
    })
    return product


@app.put("/products/{product_id}")
async def update_product(product_id: int, update_product: ProductData) -> Product:
    product = await prisma.product.update(where={"id": product_id}, data={
        "name": update_product.name,
        "description": update_product.description,
        "image_url": update_product.image_url,
        "price": update_product.price,
    })
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int) -> Success:
    await prisma.product.delete(where={"id": product_id})
    return Success(success=True)


@app.get("/products/{product_id}/variants")
async def read_product_variants(product_id: int) -> List[ProductVariant]:
    variants = await prisma.productvariant.find_many()
    return list(filter(lambda variant: variant.product_id == product_id, variants))

@app.get("/products/{product_id}/variants/{variant_id}")
async def read_product_variant(product_id: int, variant_id: int) -> ProductVariant:
    variant = await prisma.productvariant.find_unique(where={"id": variant_id})

    if variant is None:
        raise HTTPException(status_code=404, detail="Variant not found")

    return variant

@app.post("/products/{product_id}/variants")
async def create_product_variant(product_id: str, create_variant: ProductVariantData) -> ProductVariant:
    variant = await prisma.productvariant.create(data={
        "product_id": product_id,
        "name": create_variant.name,
        "addl_price": create_variant.addl_price,
        "image_url": create_variant.image_url,
    })
    return variant

@app.put("/products/{product_id}/variants/{variant_id}")
async def update_product_variant(product_id: int, variant_id: int, update_variant: ProductVariantData) -> ProductVariant:
    variant = await prisma.productvariant.update(
        where={"id": variant_id}, 
        data={
            "name": update_variant.name,
            "addl_price": update_variant.addl_price,
            "image_url": update_variant.image_url
        }
    )
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

@app.delete("/products/{product_id}/variants/{variant_id}")
async def delete_product_variant(product_id: int, variant_id: int) -> Success:
    await prisma.productvariant.delete(where={"id": variant_id})
    return Success(success=True)
