import pandas as pd
from app import create_app, db
from app.models import Hospital, Doctor, User, Appointment, Location, Availability
from werkzeug.security import generate_password_hash
from datetime import datetime, date, time

app = create_app()
app.app_context().push()

def load_hospitals():
    df = pd.read_csv('schema/hospitals.csv')
    for _, row in df.iterrows():
        hospital = Hospital(name=row['name'], location_id=row['location_id'])
        db.session.add(hospital)
    db.session.commit()

def load_doctors():
    df = pd.read_csv('schema/doctors.csv')
    for _, row in df.iterrows():
        doctor = Doctor(
            name=row['name'],
            specialization=row['specialization'],
            hospital_id=row['hospital_id']  
        )
        db.session.add(doctor)
        print(f"✅ Loaded doctor: {row['name']}") 
    db.session.commit()


def load_users():
    df = pd.read_csv('schema/users.csv')

    for _, row in df.iterrows():
        # Always hash the password from CSV, even for admin
        hashed_password = generate_password_hash(row['password'])  

        user = User(
            username=row['username'],
            password=hashed_password,
            role=row['role']  # Directly use 'role' from CSV
        )
        db.session.add(user)
        print(f"✅ Loaded user: {row['username']} with role: {row['role']}")
    
    db.session.commit()
    
def load_locations():
    df = pd.read_csv('schema/locations.csv')
    for _, row in df.iterrows():
        location = Location(region=row['region'])
        db.session.add(location)
    db.session.commit()

def load_availability():
    df = pd.read_csv('schema/availabilty.csv')
    for _, row in df.iterrows():
        # Parse string to actual date and time objects
        availability = Availability(
            doctor_id=row['doctor_id'],
            date=datetime.strptime(row['date'], "%Y-%m-%d").date(),
            from_time=datetime.strptime(row['from_time'], "%H:%M").time(),
            to_time=datetime.strptime(row['to_time'], "%H:%M").time(),
            is_booked=row['is_booked'] in [True, 'True', 'true', 1]  # Normalize booleans
        )
        db.session.add(availability)
    db.session.commit()

def load_all():
    load_locations()
    load_hospitals()
    load_doctors()
    load_users()
    load_appointments()
    load_availability()
    print("✅ All data loaded successfully.")

# Run directly
if __name__ == "__main__":
    load_all()