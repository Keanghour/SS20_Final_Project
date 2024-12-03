from flask import render_template, jsonify, request
from db.database import Session
from db.tag import Tag
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def tag():
    return render_template('pages/tag.html', module='tag')

def get_tags():
    try:
        with Session() as session:
            tags = session.query(Tag).all()

            tag_list = [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "description": tag.description,
                }
                for tag in tags
            ]

            return jsonify({"data": tag_list})

    except Exception as e:
        logger.error("Error retrieving tags: %s", e)
        return jsonify({"error": "Unable to retrieve tags."}), 500

def add_tag():
    data = request.json
    if 'name' not in data or 'description' not in data:
        return jsonify({"error": "Name and description are required."}), 400

    try:
        with Session() as session:
            new_tag = Tag(
                name=data['name'],
                description=data['description']
            )
            session.add(new_tag)
            session.commit()
        
        return jsonify({"message": "Tag added successfully."}), 201
    except Exception as e:
        logger.error("Error adding tag: %s", e)
        return jsonify({"error": "Unable to add tag.", "details": str(e)}), 500

def update_tag(tag_id):
    try:
        data = request.json
        with Session() as session:
            tag = session.query(Tag).filter_by(id=tag_id).first()
            if not tag:
                return jsonify({"error": "Tag not found."}), 404

            tag.name = data.get('name', tag.name)
            tag.description = data.get('description', tag.description)
            
            session.commit()

        return jsonify({"message": "Tag updated successfully.", "data": data}), 200

    except Exception as e:
        logger.error("Error updating tag: %s", e)
        return jsonify({"error": "Unable to update tag."}), 500

def delete_tag(tag_id):
    try:
        with Session() as session:
            tag = session.query(Tag).filter_by(id=tag_id).first()
            if not tag:
                return jsonify({"error": "Tag not found."}), 404

            session.delete(tag)
            session.commit()

        return jsonify({"message": "Tag deleted successfully."}), 200

    except Exception as e:
        logger.error("Error deleting tag: %s", e)
        return jsonify({"error": "Unable to delete tag."}), 500
