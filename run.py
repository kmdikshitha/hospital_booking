from app import create_app
from app.models import db
from app.utils.data_loader import load_csv_data

app = create_app()

with app.app_context():
    db.create_all()
    load_csv_data()  # load once

if __name__ == "__main__":
    app.run(debug=True)