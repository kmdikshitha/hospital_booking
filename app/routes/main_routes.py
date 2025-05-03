from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Availability, db, User, Hospital, Doctor, Appointment, Location
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from sqlalchemy.dialects import postgresql

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))

@main.route('/health')
def health_check():
    return 'OK', 200

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

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))

        flash('Invalid credentials')
    return render_template('login.html')


# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/dashboard')
@login_required
def dashboard():
    query = request.args.get('location')
    
    current_app.logger.info(f"Location query received: {query}")
    
    if query:
        current_app.logger.info(f"Fetching hospitals for location: {query}")
        try:
            hospitals = (
                Hospital.query
                .join(Location)
                .options(joinedload(Hospital.location)) 
                .filter(Location.region.ilike(f'%{query}%'))
                .all()
            )  
            current_app.logger.info(f"Found {len(hospitals)} hospitals for location: {query}")
        except Exception as e:
            current_app.logger.error(f"Error while querying hospitals: {e}")
            hospitals = []
    else:
        current_app.logger.info("No location query provided, fetching all hospitals.")
        try:
            hospitals = Hospital.query.options(joinedload(Hospital.location)).all()
            current_app.logger.info(f"Found {len(hospitals)} hospitals in total.")
        except Exception as e:
            current_app.logger.error(f"Error while fetching all hospitals: {e}")
            hospitals = []
    
    # Log the SQL query to understand what's being executed
    current_app.logger.info(f"SQL Query: {str(hospitals)}")
    
    return render_template('dashboard.html', hospitals=hospitals)


# Hospital -> Doctors
@main.route('/doctors/<int:hospital_id>', methods=['GET'])
@login_required
def doctors(hospital_id):
    # Get the selected hospital
    hospital = Hospital.query.get_or_404(hospital_id)
    
    # Fetch the doctors for this hospital
    doctors = Doctor.query.filter_by(hospital_id=hospital.id).all()
    
    # Render the doctors page with the doctors list
    return render_template('doctors.html', hospital=hospital, doctors=doctors)

# Doctor -> Book
@main.route('/doctors/<int:id>/book', methods=['GET', 'POST'])
@login_required
def book_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    
    # Retrieve availability for the selected doctor where the slot is not booked
    available_slots = Availability.query.filter_by(doctor_id=doctor.id, is_booked=False).all()

    if request.method == 'POST':
        slot_id = request.form['slot_id']
        slot = Availability.query.get_or_404(slot_id)
        
        if slot.is_booked:
            flash('This time slot is already booked.')
            return redirect(request.url)

        # Mark the slot as booked
        slot.is_booked = True

        # Create appointment (this assumes appointment model and user logic is set up)
        appt = Appointment(user_id=current_user.id, doctor_id=doctor.id, slot_id=slot.id)
        db.session.add(appt)
        db.session.commit()
        
        flash('Appointment booked successfully!')
        return redirect(url_for('main.confirmation'))

    return render_template('book.html', doctor=doctor, available_slots=available_slots)



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


# Admin Dashboard - View Admin Actions
@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.dashboard'))
    
    return render_template('admin_dashboard.html')


# Admin - Add Region (Location)
@main.route('/admin/add_location', methods=['GET', 'POST'])
@login_required
def add_location():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        region = request.form['region']
        location = Location(region=region)
        db.session.add(location)
        db.session.commit()
        flash(f"Location '{region}' added successfully!")
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('add_location.html')


# Admin - Add Hospital
@main.route('/admin/add_hospital', methods=['GET', 'POST'])
@login_required
def add_hospital():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.dashboard'))
    
    locations = Location.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        location_id = request.form['location_id']
        hospital = Hospital(name=name, location_id=location_id)
        db.session.add(hospital)
        db.session.commit()
        flash(f"Hospital '{name}' added successfully!")
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('add_hospital.html', locations=locations)


# Admin - Add Doctor
@main.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.dashboard'))
    
    hospitals = Hospital.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        hospital_id = request.form['hospital_id']
        doctor = Doctor(name=name, specialization=specialization, hospital_id=hospital_id)
        db.session.add(doctor)
        db.session.commit()
        flash(f"Doctor '{name}' added successfully!")
        return redirect(url_for('main.admin_dashboard'))
    
    return render_template('add_doctor.html', hospitals=hospitals)

@main.route('/admin/add_availability', methods=['GET', 'POST'])
@login_required
def add_availability():
    if current_user.role != 'admin':
        flash('Unauthorized access.')
        return redirect(url_for('main.dashboard'))

    doctors = Doctor.query.all()

    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        from_time = request.form['from_time']
        to_time = request.form['to_time']

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.strptime(from_time, "%H:%M").time()
        end_time = datetime.strptime(to_time, "%H:%M").time()

        exists = Availability.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj,
            from_time=start_time,
            to_time=end_time
        ).first()

        if exists:
            flash("Availability already exists for the selected doctor and time.")
        else:
            availability = Availability(
                doctor_id=doctor_id,
                date=date_obj,
                from_time=start_time,
                to_time=end_time
            )
            db.session.add(availability)
            db.session.commit()
            flash("Availability added successfully!")

        return redirect(url_for('main.admin_dashboard'))

    return render_template('add_availability.html', doctors=doctors)
