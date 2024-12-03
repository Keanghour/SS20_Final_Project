from flask import render_template, jsonify, request
from db.database import Session
from db.unit import Unit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def unit():
    return render_template('pages/unit.html', module='unit')

def get_units():
    try:
        with Session() as session:
            units = session.query(Unit).all()

            unit_list = [
                {
                    "id": unit.id,
                    "name": unit.name,
                    "description": unit.description,
                }
                for unit in units
            ]

            return jsonify({"data": unit_list})

    except Exception as e:
        logger.error("Error retrieving units: %s", e)
        return jsonify({"error": "Unable to retrieve units."}), 500

def add_unit():
    data = request.json
    try:
        with Session() as session:
            new_unit = Unit(
                name=data['name'],
                description=data['description']
            )
            session.add(new_unit)
            session.commit()
        
        return jsonify({"message": "Unit added successfully."}), 201
    except Exception as e:
        logger.error("Error adding unit: %s", e)
        return jsonify({"error": "Unable to add unit.", "details": str(e)}), 500

def update_unit(unit_id):
    try:
        data = request.json
        with Session() as session:
            unit = session.query(Unit).filter_by(id=unit_id).first()
            if not unit:
                return jsonify({"error": "Unit not found."}), 404

            unit.name = data.get('name', unit.name)
            unit.description = data.get('description', unit.description)
            
            session.commit()

        return jsonify({"message": "Unit updated successfully.", "data": data}), 200

    except Exception as e:
        logger.error("Error updating unit: %s", e)
        return jsonify({"error": "Unable to update unit."}), 500

def delete_unit(unit_id):
    try:
        with Session() as session:
            unit = session.query(Unit).filter_by(id=unit_id).first()
            if not unit:
                return jsonify({"error": "Unit not found."}), 404

            session.delete(unit)
            session.commit()

        return jsonify({"message": "Unit deleted successfully."}), 200

    except Exception as e:
        logger.error("Error deleting unit: %s", e)
        return jsonify({"error": "Unable to delete unit."}), 500
