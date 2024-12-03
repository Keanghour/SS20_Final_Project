from flask import Blueprint
from controllers.tag_controller import tag, get_tags, add_tag, update_tag, delete_tag

tag_router = Blueprint('tag_router', __name__)

@tag_router.route('/tag')
def tag_route():
    return tag()

@tag_router.route('/getTags', methods=['GET'])
def tags_route():
    return get_tags()

@tag_router.route('/addTag', methods=['POST'])
def add_tag_route():
    return add_tag()

@tag_router.route('/updateTag/<int:tag_id>', methods=['PUT'])
def update_tag_route(tag_id):
    return update_tag(tag_id)

@tag_router.route('/deleteTag/<int:tag_id>', methods=['DELETE'])
def delete_tag_route(tag_id):
    return delete_tag(tag_id)
