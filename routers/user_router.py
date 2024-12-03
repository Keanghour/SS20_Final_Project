import uuid
from flask import Blueprint, jsonify, render_template, request, current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import time
import base64

from helpers import file_upload

user_router = Blueprint('user_router', __name__)

# Initialize the SQLite database engine
engine = create_engine("sqlite:///db/app_db.sqlite", echo=True)
Session = sessionmaker(bind=engine)

@user_router.route('/user')
def user_route():
    return render_template('pages/user.html', module='user')

@user_router.route('/userList', methods=['GET'])
def userList():
    try:
        session = Session()
        result = session.execute(text("SELECT * FROM user"))
        data = result.fetchall()
        user_list = [
            {
                "id": item[0],
                "name": item[1],
                "gender": item[2],
                "phone": item[3],
                "email": item[4],
                "address": item[5],
                "image": item[6] if item[6] else 'default.png',
            }
            for item in data
        ]
        session.close()
        return {"data": user_list}
    except Exception as e:
        print("Error in /userList:", e)
        return {"error": str(e)}, 500


@user_router.route('/saveRecord', methods=['POST'])
def saveRecord():
    try:
        form = request.get_json()
        name = form.get('name')
        gender = form.get('gender')
        phone = form.get('phone')
        email = form.get('email')
        address = form.get('address')
        base64_string = form.get('image')

        # Generate a unique image name or use the existing name if provided
        if base64_string:
            image_name = f"{uuid.uuid4().hex}.png"
            image_path = os.path.join(current_app.config['IMAGE_DIR'], image_name)
            
            # Save the image if a base64 string is provided
            try:
                with open(image_path, 'wb') as img_file:
                    img_file.write(base64.b64decode(base64_string.split(',')[1]))
            except Exception as file_error:
                print("File saving error:", file_error)
                return {"error": "Failed to save image"}, 500
        else:
            image_name = 'default.png'

        # Create a new session
        session = Session()
        session.execute(text(
            "INSERT INTO `user` (name, gender, phone, email, address, image) VALUES (:name, :gender, :phone, :email, :address, :image_name)"
        ), {
            'name': name,
            'gender': gender,
            'phone': phone,
            'email': email,
            'address': address,
            'image_name': image_name
        })
        session.commit()
        session.close()

        return jsonify({"message": f"{name} saved successfully", "image_path": image_path}), 201
    except Exception as e:
        print("Error in /saveRecord:", e)
        return {"error": str(e)}, 500
    

@user_router.route('/updateRecord', methods=['POST'])
def updateRecord():
    try:
        form = request.get_json()
        id = form.get('id')
        name = form.get('name')
        gender = form.get('gender')
        phone = form.get('phone')
        email = form.get('email')
        address = form.get('address')
        base64_string = form.get('image')

        # Create a new session
        session = Session()

        # Check if a new image is provided and handle the file update
        if base64_string:
            image_name = f"{uuid.uuid4().hex}.png"
            image_path = os.path.join(current_app.config['IMAGE_DIR'], image_name)
            
            try:
                # Save the new image file
                with open(image_path, 'wb') as img_file:
                    img_file.write(base64.b64decode(base64_string.split(',')[1]))
            except Exception as file_error:
                print("File saving error:", file_error)
                return {"error": "Failed to save image"}, 500

            # Update the record with the new image
            session.execute(text(
                "UPDATE `user` SET name = :name, gender = :gender, phone = :phone, email = :email, address = :address, image = :image_name WHERE id = :id"
            ), {
                'id': id,
                'name': name,
                'gender': gender,
                'phone': phone,
                'email': email,
                'address': address,
                'image_name': image_name
            })
        else:
            # If no new image is provided, just update the other fields
            session.execute(text(
                "UPDATE `user` SET name = :name, gender = :gender, phone = :phone, email = :email, address = :address WHERE id = :id"
            ), {
                'id': id,
                'name': name,
                'gender': gender,
                'phone': phone,
                'email': email,
                'address': address
            })

        session.commit()
        session.close()

        return jsonify({"message": f"{name} updated successfully", "image_path": image_path if base64_string else None}), 200
    except Exception as e:
        print("Error in /updateRecord:", e)
        return {"error": str(e)}, 500
    
    

@user_router.route('/deleteRecord', methods=['POST'])
def deleteRecord():
    try:
        form = request.get_json()
        id = form.get('id')

        session = Session()
        session.execute(text("DELETE FROM `user` WHERE id = :id"), {'id': id})
        session.commit()
        session.close()

        return {"message": "Deleted successfully"}, 200
    except Exception as e:
        print("Error in /deleteRecord:", e)
        return {"error": str(e)}, 500
