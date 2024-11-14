from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Contact

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('form.html')

@main.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')

    new_contact = Contact(name=name, email=email, phone=phone, address=address)
    db.session.add(new_contact)
    db.session.commit()

    return redirect(url_for('main.view_contacts'))

@main.route('/contacts')
def view_contacts():
    contacts = Contact.query.all()
    return render_template('display.html', contacts=contacts)
