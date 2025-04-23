from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import db, User, Doctor, Appointment

bcrypt = Bcrypt()

routes = Blueprint('routes', __name__)

# Register a new user (admin or user)
@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Ensure all required fields are provided
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    username = data['username']
    password = data['password']
    role = data['role']

    # Check if the user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists!"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert new user into the database
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


# Login route to get JWT token
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Ensure that required fields are provided
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


# Route for adding doctors (admin only)
@routes.route('/doctors', methods=['POST'])
@jwt_required()
def add_doctor():
    current_user = get_jwt_identity()

    # Check if the current user is an admin
    if current_user['role'] != 'admin':
        return jsonify({"message": "Access forbidden: Admins only"}), 403

    data = request.get_json()

    # Ensure required fields are provided
    if not data or 'name' not in data or 'specialization' not in data or 'available' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    name = data['name']
    specialization = data['specialization']
    available = data['available']

    new_doctor = Doctor(name=name, specialization=specialization, available=available)
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({"message": "Doctor added successfully!"}), 201


# Route for booking an appointment
@routes.route('/appointments', methods=['POST'])
@jwt_required()
def book_appointment():
    current_user = get_jwt_identity()

    data = request.get_json()

    # Ensure required fields are provided
    if not data or 'doctor_id' not in data or 'appointment_date' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    doctor_id = data['doctor_id']
    appointment_date = data['appointment_date']

    new_appointment = Appointment(
        patient_id=current_user['username'],
        doctor_id=doctor_id,
        appointment_date=appointment_date
    )
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({"message": "Appointment booked successfully!"}), 201


# Route for updating or deleting an appointment (user can only modify their own appointment)
@routes.route('/appointments/<int:id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manage_appointment(id):
    current_user = get_jwt_identity()

    appointment = Appointment.query.get(id)
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404

    if current_user['username'] != appointment.patient_id:
        return jsonify({"message": "Access forbidden: You can only modify your own appointment"}), 403

    if request.method == 'PUT':
        data = request.get_json()
        status = data.get('status', None)
        
        if status:
            appointment.status = status
            db.session.commit()
            return jsonify({"message": "Appointment updated successfully!"})
        else:
            return jsonify({"message": "No status provided"}), 400

    if request.method == 'DELETE':
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted successfully!"})


# Route for viewing all appointments (admins can view all, users can view their own)
@routes.route('/appointments', methods=['GET'])
@jwt_required()
def view_appointments():
    current_user = get_jwt_identity()

    if current_user['role'] == 'admin':
        appointments = Appointment.query.all()
    else:
        appointments = Appointment.query.filter_by(patient_id=current_user['username']).all()

    appointment_list = [{"id": appt.id, "doctor_id": appt.doctor_id, "appointment_date": appt.appointment_date, "status": appt.status} for appt in appointments]

    return jsonify({"appointments": appointment_list}), 200
