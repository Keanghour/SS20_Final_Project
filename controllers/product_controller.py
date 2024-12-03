from flask import Blueprint, render_template, jsonify, request, current_app
from sqlalchemy.orm import Session
from db.database import Session as DBSession
from db.product import Product
import logging
import os
import time
import base64

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

product_router = Blueprint("product", __name__)

# Define the image directory
IMAGE_DIR = 'static/uploaded_images'
os.makedirs(IMAGE_DIR, exist_ok=True)  # Ensure the directory exists

@product_router.route("/product")
def product():
    return render_template("pages/product.html", module="product")

@product_router.route("/getProducts", methods=["GET"])
def get_products():
    try:
        with DBSession() as session:
            products = session.query(Product).all()

            product_list = [
                {
                    "id": product.id,
                    "name": product.name,
                    "cost": product.cost,
                    "price": product.price,
                    "category_name": product.category.name if product.category else None,
                    "unit_name": product.unit.name if product.unit else None,
                    "brand_name": product.brand.name if product.brand else None,
                    "tag_name": product.tag.name if product.tag else None,
                    "description": product.description,
                    "image": product.image,
                }
                for product in products
            ]

            return jsonify({"data": product_list})

    except Exception as e:
        logger.error("Error retrieving products: %s", e)
        return jsonify({"error": "Unable to retrieve products.", "details": str(e)}), 500

@product_router.route("/addProduct", methods=["POST"])
def add_product():
    try:
        data = request.json
        image_data = data.get("image")

        # Generate a unique image name
        image_name = f"{time.time()}.png"
        image_path = os.path.join(IMAGE_DIR, image_name)

        # Save the image if a base64 string is provided
        if image_data:
            try:
                with open(image_path, 'wb') as img_file:
                    img_file.write(base64.b64decode(image_data.split(',')[1]))
            except Exception as file_error:
                logger.error("File saving error: %s", file_error)
                return jsonify({"error": "Failed to save image"}), 500
        else:
            image_name = 'default.png'  # Fallback to default image if not provided

        # Add product to the database
        with DBSession() as session:
            new_product = Product(
                name=data['name'],
                cost=data['cost'],
                price=data['price'],
                category_id=data.get('category_id'),
                unit_id=data.get('unit_id'),
                brand_id=data.get('brand_id'),
                tag_id=data.get('tag_id'),
                description=data.get('description'),
                image=f"/static/uploaded_images/{image_name}"
            )
            session.add(new_product)
            session.commit()

        return jsonify({"message": "Product added successfully."}), 201

    except Exception as e:
        logger.error("Error adding product: %s", e)
        return jsonify({"error": "Unable to add product.", "details": str(e)}), 500

@product_router.route("/updateProduct/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        data = request.json
        with DBSession() as session:
            # Check if the product exists
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({"error": "Product not found."}), 404

            # Update product details
            for key, value in data.items():
                setattr(product, key, value)
            
            session.commit()

        return jsonify({"message": "Product updated successfully."}), 200

    except Exception as e:
        logger.error("Error updating product: %s", e)
        return jsonify({"error": "Unable to update product.", "details": str(e)}), 500

@product_router.route("/deleteProduct/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        with DBSession() as session:
            # Check if the product exists before trying to delete
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return jsonify({"error": "Product not found."}), 404

            session.delete(product)
            session.commit()

        return jsonify({"message": "Product deleted successfully."}), 200

    except Exception as e:
        logger.error("Error deleting product: %s", e)
        return jsonify({"error": "Unable to delete product."}), 500
    



@product_router.route("/getProduct/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        with DBSession() as session:
            # Retrieve the product by its ID
            product = session.query(Product).filter_by(id=product_id).first()
            
            if not product:
                return jsonify({"error": "Product not found."}), 404

            # Format the product details into a dictionary
            product_details = {
                "id": product.id,
                "name": product.name,
                "cost": product.cost,
                "price": product.price,
                "category_name": product.category.name if product.category else None,
                "unit_name": product.unit.name if product.unit else None,
                "brand_name": product.brand.name if product.brand else None,
                "tag_name": product.tag.name if product.tag else None,
                "description": product.description,
                "image": product.image,
            }

            return jsonify({"data": product_details})

    except Exception as e:
        logger.error("Error retrieving product by ID: %s", e)
        return jsonify({"error": "Unable to retrieve product.", "details": str(e)}), 500
