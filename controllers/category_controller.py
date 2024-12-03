from flask import Blueprint, render_template, jsonify, request
from db.database import Session
from db.category import Category
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

category_router = Blueprint('category', __name__)

@category_router.route('/category')
def category():
    return render_template('pages/category.html', module='category')

@category_router.route('/getCategories', methods=['GET'])
def get_categories():
    try:
        with Session() as session:
            categories = session.query(Category).all()

            category_list = [
                {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                }
                for category in categories
            ]

            return jsonify({"data": category_list})

    except Exception as e:
        logger.error("Error retrieving categories: %s", e)
        return jsonify({"error": "Unable to retrieve categories."}), 500

@category_router.route('/addCategory', methods=['POST'])
def add_category():
    data = request.json
    if 'name' not in data or 'description' not in data:
        return jsonify({"error": "Name and description are required."}), 400

    try:
        with Session() as session:
            new_category = Category(
                name=data['name'],
                description=data['description']
            )
            session.add(new_category)
            session.commit()

        return jsonify({"message": "Category added successfully."}), 201
    except Exception as e:
        logger.error("Error adding category: %s", e)
        return jsonify({"error": "Unable to add category.", "details": str(e)}), 500

@category_router.route('/updateCategory/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        data = request.json
        with Session() as session:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                return jsonify({"error": "Category not found."}), 404

            category.name = data.get('name', category.name)
            category.description = data.get('description', category.description)
            
            session.commit()

        return jsonify({"message": "Category updated successfully.", "data": data}), 200

    except Exception as e:
        logger.error("Error updating category: %s", e)
        return jsonify({"error": "Unable to update category."}), 500

@category_router.route('/deleteCategory/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        with Session() as session:
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                return jsonify({"error": "Category not found."}), 404

            session.delete(category)
            session.commit()

        return jsonify({"message": "Category deleted successfully."}), 200

    except Exception as e:
        logger.error("Error deleting category: %s", e)
        return jsonify({"error": "Unable to delete category."}), 500
