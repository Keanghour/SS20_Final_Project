# controllers/user_controller.py

from flask import render_template

def user():
    return render_template('pages/user.html', module='user')
