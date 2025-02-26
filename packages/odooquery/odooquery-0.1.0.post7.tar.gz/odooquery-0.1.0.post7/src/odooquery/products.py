from typing import List
from .types import Product, ProductVariant, ProductStock
from pprint import pprint

def search_product_ids_by_code(self, codes: List[str]) -> List[int]:
    """Search for sellable product IDs by their reference codes."""
    return self.connection.env['product.template'].search([
        ('sale_ok', '=', True),
        '|',
        ('default_code', 'in', codes),
        ('product_variant_ids.default_code', 'in', codes)
    ])

def search_product_ids_by_name(self, names: List[str]) -> List[int]:
    """Search for sellable product IDs by names."""
    return self.connection.env['product.template'].search([
        ('sale_ok', '=', True),
        ('name', 'ilike', names)
    ])

def search_location_ids_by_usage(self, usage: str) -> List[int]:
    """Search for locations by usage."""
    return self.connection.env['stock.location'].search([
        ('usage', '=', usage)
    ])

def search_variant_ids_by_code(self, codes: List[str]) -> List[int]:
    """Search for variant IDs of sellable products by their reference codes."""
    return self.connection.env['product.product'].search([
        ('product_tmpl_id.sale_ok', '=', True),
        ('default_code', 'in', codes)
    ])

def search_variant_ids_by_product_name(self, names: List[str]) -> List[int]:
    """Search for variant IDs of sellable products by product names."""
    return self.connection.env['product.product'].search([
        ('product_tmpl_id.sale_ok', '=', True),
        ('product_tmpl_id.name', 'ilike', names)
    ])

def search_variant_ids_by_product_id(self, product_ids: List[int]) -> List[int]:
    """Search for variant IDs of sellable products by product IDs."""
    return self.connection.env['product.product'].search([
        ('product_tmpl_id.sale_ok', '=', True),
        ('product_tmpl_id', 'in', product_ids)
    ])

def fetch_stock_quants_by_variant_id_and_location_id(self, variant_ids: List[int], location_ids: List[int]) -> List[ProductStock]:
    """Fetch stock quants for variants in specific locations, grouped by product variant and location ids."""
    return [{
        'product_id': quant['product_id'][0] if isinstance(quant['product_id'], (list, tuple)) else quant['product_id'],
        'location_id': quant['location_id'][0] if isinstance(quant['location_id'], (list, tuple)) else quant['location_id'],
        'location_name': quant['location_id'][1] if isinstance(quant['location_id'], (list, tuple)) else '',
        'quantity': quant['quantity'],
        'reserved_quantity': quant['reserved_quantity'],
        'available_quantity': quant['quantity'] - quant['reserved_quantity']
    } for quant in self.connection.env['stock.quant'].read_group(
        [
            ('product_id', 'in', variant_ids),
            ('location_id', 'in', location_ids)
        ],
        ['product_id', 'location_id', 'quantity', 'reserved_quantity'],
        ['product_id', 'location_id'],
        lazy=False
    )]

def fetch_stock_levels_by_variant_id(self, variant_ids: List[int]) -> List[ProductStock]:
    """Fetch stock levels for variants in internal locations only, grouped by product variant and location ids."""

    return self.fetch_stock_quants_by_variant_id_and_location_id(
        variant_ids,
        search_location_ids_by_usage(self, 'internal')
    )

def fetch_variants_by_id(self, variant_ids: List[int]) -> List[ProductVariant]:
    """Fetch detailed variant information including stock levels."""
    variants = []
    for variant in self.connection.env['product.product'].read(variant_ids,
            ['id', 'display_name', 'default_code', 'barcode', 'list_price', 'standard_price']):

        variants.append({
            'id': variant['id'],
            'name': variant['display_name'],
            'default_code': variant['default_code'],
            'barcode': variant['barcode'],
            'list_price': variant['list_price'],
            'standard_price': variant['standard_price']
        })
    return variants

def fetch_products_by_id(self, product_ids: List[int]) -> List[Product]:
    """Fetch detailed product information including variants and stock levels."""
    products = self.connection.env['product.template'].read(product_ids, ['id', 'name', 'default_code', 'description', 'categ_id', 'product_variant_ids'])

    return [{
        'id': product['id'],
        'name': product['name'],
        'default_code': product['default_code'],
        'description': product['description'],
        'category_id': product['categ_id'][0] if isinstance(product['categ_id'], (list, tuple)) else product['categ_id'],
        'category_name': product['categ_id'][1] if isinstance(product['categ_id'], (list, tuple)) else '',
        'variant_ids': product['product_variant_ids'],
    } for product in products]

# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_stock_levels_by_product_id(self, product_ids: List[int]) -> List[ProductStock]:
    """Fetch stock levels for products in internal locations only, grouped by product variant and location ids."""
    return self.fetch_stock_levels_by_variant_id(self.search_variant_ids_by_product_id(product_ids))

def fetch_stock_levels_by_product_name(self, names: List[str]) -> List[ProductStock]:
    """Fetch stock levels for products in internal locations only, grouped by product variant and location ids."""
    return self.fetch_stock_levels_by_variant_id(self.search_variant_ids_by_product_name(names))

def fetch_stock_levels_by_variant_code(self, codes: List[str]) -> List[ProductStock]:
    """Fetch stock levels for variants in internal locations only, grouped by product variant and location ids."""
    return self.fetch_stock_levels_by_variant_id(self.search_variant_ids_by_code(codes))

def fetch_variants_by_product_id(self, product_ids: List[int]) -> List[ProductVariant]:
    """Fetch detailed variant information for products."""
    return self.fetch_variants_by_id(self.search_variant_ids_by_product_id(product_ids))

def fetch_variants_by_product_name(self, names: List[str]) -> List[ProductVariant]:
    """Fetch detailed variant information for products."""
    return self.fetch_variants_by_id(self.search_variant_ids_by_product_name(names))

def fetch_variants_by_product_code(self, codes: List[str]) -> List[ProductVariant]:
    """Fetch detailed variant information for products."""
    return self.fetch_variants_by_id(self.search_variant_ids_by_code(codes))

def fetch_products_by_code(self, codes: List[str]) -> List[Product]:
    """Fetch detailed product information including variants and stock levels."""
    return self.fetch_products_by_id(self.search_product_ids_by_code(codes))

def fetch_products_by_name(self, names: List[str]) -> List[Product]:
    """Fetch detailed product information including variants and stock levels."""
    return self.fetch_products_by_id(self.search_product_ids_by_name(names))

