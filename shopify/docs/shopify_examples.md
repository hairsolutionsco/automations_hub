# Shopify Configuration Examples

## Product Templates

### Hair Care Product
```json
{
  "product": {
    "title": "Premium Hair Serum",
    "body_html": "<p>Nourishing serum for all hair types</p>",
    "vendor": "Hair Solutions Co",
    "product_type": "Hair Care",
    "tags": ["serum", "hair-care", "premium"],
    "status": "active",
    "variants": [
      {
        "option1": "50ml",
        "price": "29.99",
        "sku": "HSC-SERUM-50",
        "inventory_quantity": 100
      }
    ],
    "options": [
      {
        "name": "Size",
        "values": ["50ml", "100ml"]
      }
    ]
  }
}
```

## Collection Templates

### Hair Type Collection
```json
{
  "smart_collection": {
    "title": "Products for Curly Hair",
    "body_html": "<p>Specially formulated for curly hair types</p>",
    "rules": [
      {
        "column": "tag",
        "relation": "equals",
        "condition": "curly-hair"
      }
    ]
  }
}
```

## Theme Components

### Product Card Component
```liquid
<div class="product-card">
  <div class="product-image">
    <img src="{{ product.featured_image | img_url: '300x300' }}" alt="{{ product.title }}">
  </div>
  <div class="product-info">
    <h3>{{ product.title }}</h3>
    <p class="price">{{ product.price | money }}</p>
    <button class="add-to-cart" data-product-id="{{ product.id }}">
      Add to Cart
    </button>
  </div>
</div>
```

## Metafield Configurations

### Hair Profile Metafields
```json
{
  "metafield": {
    "namespace": "hair_profile",
    "key": "hair_type",
    "value": "curly",
    "type": "single_line_text_field"
  }
}
```
