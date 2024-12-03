from venv import logger
from flask import Blueprint, jsonify, render_template
from controllers.product_controller import get_product_by_id, product, get_products, add_product, update_product, delete_product
from db.product import Product

product_router = Blueprint('product_router', __name__)

@product_router.route('/product')
def product_route():
    return product()

@product_router.route('/getProducts', methods=['GET'])
def get_products_route():
    return get_products()

@product_router.route('/addProduct', methods=['POST'])
def add_product_route():
    return add_product()

@product_router.route('/updateProduct/<int:product_id>', methods=['PUT'])
def update_product_route(product_id):
    return update_product(product_id)

@product_router.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    return delete_product(product_id)


@product_router.route('/getProduct/<int:product_id>', methods=['GET'])
def get_product_by_id_route(product_id):
    return get_product_by_id(product_id)

# from db.database import DBSession 

# @product_router.route("/getProduct/<int:product_id>", methods=["GET"])
# def get_product_by_id(product_id):
#     try:
#         logger.info(f"Fetching product with ID: {product_id}")
#         with DBSession() as session:
#             # Retrieve the product by its ID
#             product = session.query(Product).filter_by(id=product_id).first()
            
#             if not product:
#                 logger.warning(f"Product with ID {product_id} not found.")
#                 return jsonify({"error": "Product not found."}), 404

#             logger.info(f"Product with ID {product_id} found: {product.name}")
            
#             # Render the product details template with the product data
#             return render_template("views/product_detail.html", product=product)

#     except Exception as e:
#         logger.error("Error retrieving product by ID: %s", e, exc_info=True)
#         return jsonify({"error": "Unable to retrieve product.", "details": str(e)}), 500


