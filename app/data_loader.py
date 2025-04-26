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
        print(f"✅ Loaded doctor: {row['name']}") 
    db.session.commit()


def load_users():
    df = pd.read_csv('schema/users.csv')
    for _, row in df.iterrows():
        # Here you can define the admin username directly or from the CSV if needed
        role = 'admin' if row['username'] == 'admin' else 'user'  # Adjust this based on your admin username
        
        # Hash the password before saving to the database
        hashed_password = generate_password_hash(row['password'])  # Hash the password for security

        user = User(
            username=row['username'],            
            password=hashed_password,  # Store the hashed password
            role=role  # Assign the role based on the username
        )
        db.session.add(user)
        print(f"✅ Loaded user: {row['username']} with role: {role}")
    
    db.session.commit()




def load_appointments():
    df = pd.read_csv('schema/appointments.csv')
    for _, row in df.iterrows():
        appointment = Appointment(
            user_id=row['user_id'],
            doctor_id=row['doctor_id']
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