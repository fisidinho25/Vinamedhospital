from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Department, Doctor, Appointment, News
from forms import AppointmentForm, SearchForm
from sqlalchemy import or_

@app.route('/')
def index():
    """Homepage with hospital overview"""
    departments = Department.query.limit(4).all()
    doctors = Doctor.query.limit(3).all()
    recent_news = News.query.order_by(News.published_date.desc()).limit(3).all()
    return render_template('index.html', departments=departments, doctors=doctors, news=recent_news)

@app.route('/departments')
def departments():
    """Departments and services page"""
    all_departments = Department.query.all()
    return render_template('departments.html', departments=all_departments)

@app.route('/doctors')
def doctors():
    """All doctors listing"""
    department_id = request.args.get('department_id', type=int)
    if department_id:
        doctors_list = Doctor.query.filter_by(department_id=department_id).all()
        department = Department.query.get(department_id)
        page_title = f"Doctors in {department.name}" if department else "Doctors"
    else:
        doctors_list = Doctor.query.all()
        page_title = "Our Medical Team"
    
    departments = Department.query.all()
    return render_template('doctors.html', doctors=doctors_list, departments=departments, page_title=page_title)

@app.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    """Individual doctor profile page"""
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('doctor_profile.html', doctor=doctor)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    """Appointment booking form"""
    form = AppointmentForm()
    
    # Populate doctor choices
    doctors = Doctor.query.all()
    form.doctor_id.choices = [(doctor.id, f"Dr. {doctor.name} - {doctor.specialization}") for doctor in doctors]
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_name=form.patient_name.data,
            patient_email=form.patient_email.data,
            patient_phone=form.patient_phone.data,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            reason=form.reason.data
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Your appointment has been successfully booked! We will contact you shortly to confirm.', 'success')
        return redirect(url_for('appointments'))
    
    return render_template('appointments.html', form=form)

@app.route('/contact')
def contact():
    """Contact information and location"""
    return render_template('contact.html')

@app.route('/news')
def news():
    """Hospital news and announcements"""
    page = request.args.get('page', 1, type=int)
    news_items = News.query.order_by(News.published_date.desc()).paginate(
        page=page, per_page=6, error_out=False
    )
    return render_template('news.html', news=news_items)

@app.route('/search')
def search():
    """Basic search functionality"""
    form = SearchForm()
    results = []
    query = request.args.get('query', '').strip()
    
    if query:
        # Search doctors
        doctors = Doctor.query.filter(
            or_(
                Doctor.name.contains(query),
                Doctor.specialization.contains(query),
                Doctor.bio.contains(query)
            )
        ).all()
        
        # Search departments
        departments = Department.query.filter(
            or_(
                Department.name.contains(query),
                Department.description.contains(query)
            )
        ).all()
        
        # Search news
        news_items = News.query.filter(
            or_(
                News.title.contains(query),
                News.content.contains(query)
            )
        ).all()
        
        results = {
            'doctors': doctors,
            'departments': departments,
            'news': news_items,
            'query': query
        }
    
    return render_template('search_results.html', results=results, query=query)

@app.context_processor
def inject_search_form():
    """Make search form available in all templates"""
    return dict(search_form=SearchForm())

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
