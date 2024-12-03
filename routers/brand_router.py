from flask import Blueprint
from controllers.brand_controller import brand, get_brands, add_brand, update_brand, delete_brand

brand_router = Blueprint('brand_router', __name__)

@brand_router.route('/brand')
def brand_route():
    return brand()

@brand_router.route('/getBrands', methods=['GET'])
def brands_route():
    return get_brands()

@brand_router.route('/addBrand', methods=['POST'])
def add_brand_route():
    return add_brand()

@brand_router.route('/updateBrand/<int:brand_id>', methods=['PUT'])
def update_brand_route(brand_id):
    return update_brand(brand_id)

@brand_router.route('/deleteBrand/<int:brand_id>', methods=['DELETE'])
def delete_brand_route(brand_id):
    return delete_brand(brand_id)
