from prisma.models import Product, ProductVariant

Product.create_partial('ProductData', exclude=['product_id'])

ProductVariant.create_partial('ProductVariantData', exclude=['variant_id', 'product_id'])

