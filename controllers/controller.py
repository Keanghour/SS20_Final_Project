# controllers/controller.py

from flask import render_template

def dashboard():
    return render_template('pages/dashboard.html', module='dashboard')

def user():
    return render_template('pages/user.html', module='user')

def product():
    return render_template('pages/product.html', module='product')

def category():
    return render_template('pages/category.html', module='category')

def brand():
    return render_template('pages/brand.html', module='brand')

def tag():
    return render_template('pages/tag.html', module='tag')

def unit():
    return render_template('pages/unit.html', module='unit')
