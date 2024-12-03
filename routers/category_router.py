# routers/category_router.py

from flask import Blueprint
from controllers.category_controller import category, get_categories, add_category, update_category, delete_category

category_router = Blueprint('category_router', __name__)

@category_router.route('/category')
def category_route():
    return category()

@category_router.route('/getCategories', methods=['GET'])
def categories_route():
    return get_categories()

@category_router.route('/addCategory', methods=['POST'])
def add_category_route():
    return add_category()

@category_router.route('/updateCategory/<int:category_id>', methods=['PUT'])
def update_category_route(category_id):
    return update_category(category_id)

@category_router.route('/deleteCategory/<int:category_id>', methods=['DELETE'])
def delete_category_route(category_id):
    return delete_category(category_id)
