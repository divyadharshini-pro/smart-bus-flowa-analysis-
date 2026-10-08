SmartBus Flow

SmartBus Flow is a smart bus tracking and management system designed to help users monitor bus information and improve transportation management.

Features

- Admin login and dashboard
- Driver login and dashboard
- Bus tracking page
- GPS location update support
- Simple and responsive interface
- Flask-based web application

User Login

Admin

- Username: "admin"
- Password: "admin123"

Driver

- Username: "driver"
- Password: "driver123"

Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Gunicorn

Project Structure

SmartBus-Flow/
├── app.py
├── requirements.txt
├── Procfile
├── README.md
├── templates/
│   ├── login.html
│   ├── admin.html
│   ├── driver.html
│   └── tracking.html
└── static/
    └── style.css

Run Locally

Install the required packages:

pip install -r requirements.txt

Start the application:

python app.py

Then open:

http://localhost:5000

Deployment

The application can be deployed using a service such as Render with Gunicorn.

Start command:

gunicorn app:app
