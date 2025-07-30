from app import db
from datetime import datetime, date

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    doctors = db.relationship('Doctor', backref='department', lazy=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    available_days = db.Column(db.String(100))  # Comma-separated days
    consultation_hours = db.Column(db.String(100))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(120), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    doctor = db.relationship('Doctor', backref='appointments')

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

def initialize_sample_data():
    """Initialize the database with sample data if it's empty"""
    if Department.query.count() == 0:
        # Add departments
        departments_data = [
            {
                'name': 'Emergency Medicine',
                'description': '24/7 emergency care with state-of-the-art facilities and experienced medical professionals.',
                'image_url': 'https://pixabay.com/get/gaa94acb65c0aa104b3d7ed60d5595cd607a667f6f16b33ae264f38faf359dda581d09e49e18f4c2a10d84e77b88ac7a78b41853dcb35d9fcab4c7385436da48d_1280.jpg'
            },
            {
                'name': 'Cardiology',
                'description': 'Comprehensive heart care including diagnostics, treatment, and cardiac surgery.',
                'image_url': 'https://pixabay.com/get/g3482351ab0427c1be5e9b63a7b7cf043252f706d76afb6d6b854c26b2178d32e98ab8f39aa9b20117d5e53ca7d2c80abdd185b1232accb69a800815c544a5dc3_1280.jpg'
            },
            {
                'name': 'Pediatrics',
                'description': 'Specialized medical care for infants, children, and adolescents.',
                'image_url': 'https://pixabay.com/get/gf5e156d1f9e237cb42e7e18c3d7f0a94f28461f80dc7e5fbdbffe1fd5198a5723f85b2ec481eeaccf1e04265cd5c061347cafd59c560f1453c969f3a2371777c_1280.jpg'
            },
            {
                'name': 'Orthopedics',
                'description': 'Treatment of musculoskeletal conditions including bones, joints, and muscles.',
                'image_url': 'https://pixabay.com/get/g80d37c12d3e3a111f72a30b172d9813a3ec30f06d6d4ca4e77cff0736fe7ee5c948b65ba7f41e21a6c63b4fd50ceea369f7db7b488e946909cc2682a5bc04076_1280.jpg'
            }
        ]
        
        for dept_data in departments_data:
            department = Department(**dept_data)
            db.session.add(department)
        
        db.session.commit()
        
        # Add doctors
        doctors_data = [
            {
                'name': 'Dr. Oladosu Musiliu Atanda',
                'specialization': 'Orthopaedic Surgeon',
                'qualifications': 'MD, FACEP',
                'experience_years': 15,
                'bio': 'Dr. Oladosu is a board-certified emergency physician with over 15 years of experience in critical care.',
                'image_url': 'https://pixabay.com/get/g1588064a9fe803558e2e3239c6fcb32b39ccf708ade02b3fdf99bcd8a29b26a1d3b79320a90f1222dda9f3da05c13cf11e55246e5879ba18923af927cecf6912_1280.jpg',
                'department_id': 1,
                'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
                'consultation_hours': '24/7 Emergency'
            },
            {
                'name': 'Dr. Oladosu',
                'specialization': 'Cardiology',
                'qualifications': 'MD, FACC',
                'experience_years': 20,
                'bio': 'Renowned cardiologist specializing in interventional cardiology and heart disease prevention.',
                'image_url': 'https://pixabay.com/get/gf422c85003697174327cbf1c51a8dde5f76ed32ae7c1a74b11b3cffe7a2c2079eb2ac91e0580e1fc9594431d8237b70099171439362a12e592281fbbec90c45f_1280.jpg',
                'department_id': 2,
                'available_days': 'Monday,Wednesday,Friday',
                'consultation_hours': '9:00 AM - 5:00 PM'
            },
            {
                'name': 'Dr. Efo',
                'specialization': 'Pediatrics',
                'qualifications': 'MD, FAAP',
                'experience_years': 12,
                'bio': 'Pediatric specialist dedicated to providing comprehensive healthcare for children of all ages.',
                'image_url': 'https://pixabay.com/get/g56ec734312692d5a6e4dbb22ec314b2d222cdd4b18172321238b37aa6fa7c355cb0cf2e3a9ccda18d80607cfc13afe2b74559da619eabb9c6dd2076b376e9b60_1280.jpg',
                'department_id': 3,
                'available_days': 'Tuesday,Thursday,Saturday',
                'consultation_hours': '8:00 AM - 4:00 PM'
            },
            {
                'name': 'Dr. Dammy',
                'specialization': 'Orthopedic Surgery',
                'qualifications': 'MD, FAAOS',
                'experience_years': 18,
                'bio': 'Expert orthopedic surgeon specializing in joint replacement and sports medicine.',
                'image_url': 'https://pixabay.com/get/g9260a5fb2c5832d514a2abee135f0d777a500ae9ee2a0cf067dad07ca9d3e14a18a2f9a16a22b8ecaafe0baa98abe2ba9214f4a95971d0df6294fb9a361c6ae8_1280.jpg',
                'department_id': 4,
                'available_days': 'Monday,Tuesday,Thursday,Friday',
                'consultation_hours': '10:00 AM - 6:00 PM'
            }
        ]
        
        for doctor_data in doctors_data:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        # Add sample news
        news_data = [
            {
                'title': 'New Cardiac Care Unit Opens',
                'content': 'We are excited to announce the opening of our new state-of-the-art cardiac care unit, featuring the latest in cardiovascular technology and treatment options.',
                'summary': 'Advanced cardiac care unit now open with cutting-edge technology.',
                'author': 'Hospital Administration',
                'image_url': 'https://pixabay.com/get/g443a58bbfa15196ad753cf05e018a7efbc9cf0f3f97d3e277771a9571dd1352759701bede8a833432b3887685f67be4cf0751c5f0818bb68d3a155b05e4c39a5_1280.jpg'
            },
            {
                'title': 'COVID-19 Safety Protocols Updated',
                'content': 'In line with current health guidelines, we have updated our safety protocols to ensure the highest level of protection for our patients and staff.',
                'summary': 'Enhanced safety measures implemented for patient and staff protection.',
                'author': 'Dr. Oladosu',
                'image_url': 'https://pixabay.com/get/g3529cf3c6a44a638348aba507bab445a87c41877ef4e1f28faf2da3f82aad10b1476ae5656b0c6980fd1d5c4bcc4fb5490b120f88878920de2ff5accddfd4f52_1280.jpg'
            }
        ]
        
        for news_item in news_data:
            news = News(**news_item)
            db.session.add(news)
        
        db.session.commit()
