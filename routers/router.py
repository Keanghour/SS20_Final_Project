from flask import Blueprint, render_template

router = Blueprint('router', __name__)

@router.route('/')
def home_route():
    return render_template('pages/dashboard.html') 
