from flask import Flask, render_template, request, redirect, url_for
from peewee import *
from models import User, db
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    success_message = None
    error_message = None

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        cpf = request.form['cpf']
        birth_date = request.form['birth_date']
        phone_number = request.form['phone_number']
        email = request.form['email']
        car_model = request.form['car_model']

        # Server-side validation: Check if CPF contains only numbers
        if not cpf.isdigit():
            error_message = "CPF must contain only numbers."
        else:
            # Create new user if no validation errors
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
            user = User.create(name=name, gender=gender, cpf=cpf, birth_date=birth_date, phone_number=phone_number, email=email, car_model=car_model)
            success_message = "User registered successfully!"

    return render_template('register.html', success_message=success_message, error_message=error_message)

@app.route('/consult')
def consult():
    users = User.select()
    return render_template('consult.html', users=users,display_column='geral')

@app.route('/names')
def get_names():
    names = User.select(User.name)
    return render_template('consult.html',users=names,display_column='name')

@app.route('/genders')
def get_genders():
    genders = User.select(User.gender)
    return render_template('consult.html',users=genders,display_column='gender')

@app.route('/cpfs')
def get_cpfs():
    cpfs = User.select(User.cpf)
    return render_template('consult.html',users=cpfs,display_column='cpf')

@app.route('/birth_dates')
def get_birth_dates():
    birth_dates = User.select(User.birth_date)
    return render_template('consult.html',users=birth_dates,display_column='birth_date')

@app.route('/phone_number')
def get_phone_numbers():
    phone_numbers = User.select(User.phone_number)
    return render_template('consult.html',users=phone_number,display_column='phone_number')

@app.route('/email')
def get_email():
    emails = User.select(User.email)
    return render_template('consult.html',users=emails,display_column='email')
    
@app.route('/car_models')
def get_car_models():
    # Query the car_model column only
    car_models = User.select(User.car_model)
    return render_template('consult.html', users=car_models, display_column='car_model')

# Route to delete a user by CPF
@app.route('/delete_user/<string:cpf>', methods=['POST', 'GET'])
def delete_user(cpf):
    try:
        user = User.get(User.cpf == cpf)
        user.delete_instance()  # Delete user from database
        return redirect(url_for('consult'))  # Redirect to consult after deletion
    except User.DoesNotExist:
        return "User not found", 404

# Route to update user information by CPF
@app.route('/update_user/<string:cpf>', methods=['GET', 'POST'])
def update_user(cpf):
    try:
        user = User.get(User.cpf == cpf)
        if request.method == 'POST':
            # Get data from form and update the user fields
            name = request.form['name']
            gender = request.form['gender']
            cpf = request.form['cpf']
            birth_date = request.form['birth_date']
            phone_number = request.form['phone_number']
            email = request.form['email']
            car_model = request.form['car_model']
            
            # Update specific fields
            user.name = name
            user.gender = gender
            user.cpf = cpf
            user.birth_date = birth_date
            user.phone_number = phone_number
            user.email = email
            user.car_model = car_model
            user.save()  # Save changes to the database

            return redirect(url_for('consult'))
        
        # Render form with current user information
        return render_template('update_user.html', user=user)

    except User.DoesNotExist:
        return "User not found", 404

if __name__ == '__main__':
    db.connect()
    app.run(host='0.0.0.0', port=5000)
