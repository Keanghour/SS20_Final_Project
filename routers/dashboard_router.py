from flask import Blueprint
from controllers.dashboard_controller import dashboard

dashboard_router = Blueprint('dashboard_router', __name__)

@dashboard_router.route('/dashboard')
def dashboard_route():
    return dashboard()
