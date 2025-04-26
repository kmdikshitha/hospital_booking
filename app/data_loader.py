import pandas as pd
from app import create_app, db
from app.models import Hospital, Doctor, User, Appointment, Location

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
    db.session.commit()

def load_users():
    df = pd.read_csv('schema/users.csv')
    for _, row in df.iterrows():
        user = User(
            name=row['name'],
            password=row['password'],
            role=row['role']
        )
        db.session.add(user)
    db.session.commit()

def load_appointments():
    df = pd.read_csv('schema/appointments.csv')
    for _, row in df.iterrows():
        appointment = Appointment(
            user_id=row['user_id'],
            doctor_id=row['doctor_id'],
            user=row['user'],
            doctor=row['doctor']
        )
        db.session.add(appointment)
    db.session.commit()

def load_locations():
    df = pd.read_csv('schema/locations.csv')
    for _, row in df.iterrows():
        location = Location(region=row['region'])
        db.session.add(location)
    db.session.commit()

def load_all():
    load_locations()
    load_hospitals()
    load_doctors()
    load_users()
    load_appointments()
    print("✅ All data loaded successfully.")

# Run directly
if __name__ == "__main__":
    load_all()