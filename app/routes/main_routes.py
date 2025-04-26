from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Hospital, Doctor, Appointment
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

# Register
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully.")
        return redirect(url_for('main.login'))
    return render_template('register.html')

# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    query = request.args.get('location')
    if query:
        hospitals = Hospital.query.filter(Hospital.location.ilike(f'%{query}%')).all()
    else:
        hospitals = Hospital.query.all()
    return render_template('dashboard.html', hospitals=hospitals)

# Hospital -> Doctors
@main.route('/hospitals/<int:id>')
@login_required
def view_doctors(id):
    doctors = Doctor.query.filter_by(hospital_id=id).all()
    hospital = Hospital.query.get_or_404(id)
    return render_template('doctors.html', doctors=doctors, hospital=hospital)

# Doctor -> Book
@main.route('/doctors/<int:id>/book', methods=['GET', 'POST'])
@login_required
def book_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        appt = Appointment(user_id=current_user.id, doctor_id=id)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('main.confirmation'))
    return render_template('book.html', doctor=doctor)

# Confirmation
@main.route('/confirm')
@login_required
def confirmation():
    return render_template('confirmation.html')

# View Appointments
@main.route('/appointments')
@login_required
def view_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('appointments.html', appointments=appointments)

# Delete Appointment
@main.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appt = Appointment.query.get_or_404(id)
    if appt.user_id != current_user.id:
        flash('Unauthorized action')
        return redirect(url_for('main.view_appointments'))
    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for('main.view_appointments'))