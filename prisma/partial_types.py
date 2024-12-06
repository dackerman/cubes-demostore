from prisma.models import Product, ProductVariant

Product.create_partial('ProductData', exclude=['id'])

ProductVariant.create_partial('ProductVariantData', exclude=['id', 'product_id'])

