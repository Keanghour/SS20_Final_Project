from flask import Blueprint
from controllers.unit_controller import (
    unit, get_units, add_unit, update_unit, delete_unit
)

unit_router = Blueprint('unit_router', __name__)

@unit_router.route('/unit', methods=['GET'])
def unit_route():
    return unit()

@unit_router.route('/getUnits', methods=['GET'])
def units_route():
    return get_units()

@unit_router.route('/addUnit', methods=['POST'])
def add_unit_route():
    return add_unit()

@unit_router.route('/updateUnit/<int:unit_id>', methods=['PUT'])
def update_unit_route(unit_id):
    return update_unit(unit_id)

@unit_router.route('/deleteUnit/<int:unit_id>', methods=['DELETE'])
def delete_unit_route(unit_id):
    return delete_unit(unit_id)
