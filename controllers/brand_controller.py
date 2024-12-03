from flask import Blueprint, render_template, jsonify, request
from db.database import Session
from db.brand import Brand
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

brand_router = Blueprint('brand', __name__)

@brand_router.route('/brand')
def brand():
    return render_template('pages/brand.html', module='brand')

@brand_router.route('/getBrands', methods=['GET'])
def get_brands():
    try:
        with Session() as session:
            brands = session.query(Brand).all()

            brand_list = [
                {
                    "id": brand.id,
                    "name": brand.name,
                    "description": brand.description,
                }
                for brand in brands
            ]

            return jsonify({"data": brand_list})

    except Exception as e:
        logger.error("Error retrieving brands: %s", e)
        return jsonify({"error": "Unable to retrieve brands."}), 500

@brand_router.route('/addBrand', methods=['POST'])
def add_brand():
    data = request.json
    logger.info("Received data: %s", data)

    # Validate data
    if 'name' not in data or not data['name']:
        return jsonify({"error": "Name is required."}), 400

    try:
        with Session() as session:
            new_brand = Brand(
                name=data['name'],
                description=data.get('description')
            )
            session.add(new_brand)
            session.commit()

        return jsonify({"message": "Brand added successfully."}), 201
    except Exception as e:
        logger.error("Error adding brand: %s", e)
        return jsonify({"error": "Unable to add brand.", "details": str(e)}), 500

@brand_router.route('/updateBrand/<int:brand_id>', methods=['PUT'])
def update_brand(brand_id):
    try:
        data = request.json
        with Session() as session:
            brand = session.query(Brand).filter_by(id=brand_id).first()
            if not brand:
                return jsonify({"error": "Brand not found."}), 404

            # Update the brand fields
            brand.name = data.get('name', brand.name)
            brand.description = data.get('description', brand.description)

            session.commit()

        return jsonify({"message": "Brand updated successfully.", "data": data}), 200

    except Exception as e:
        logger.error("Error updating brand: %s", e)
        return jsonify({"error": "Unable to update brand."}), 500

@brand_router.route('/deleteBrand/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    try:
        with Session() as session:
            brand = session.query(Brand).filter_by(id=brand_id).first()
            if not brand:
                return jsonify({"error": "Brand not found."}), 404

            session.delete(brand)
            session.commit()

        return jsonify({"message": "Brand deleted successfully."}), 200

    except Exception as e:
        logger.error("Error deleting brand: %s", e)
        return jsonify({"error": "Unable to delete brand."}), 500
