# controllers/dashboard_controller.py

from flask import render_template

def dashboard():
    return render_template('pages/dashboard.html', module='dashboard')
