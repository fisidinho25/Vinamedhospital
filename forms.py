from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, TimeField, EmailField
from wtforms.validators import DataRequired, Email, Length
from datetime import date, timedelta

class AppointmentForm(FlaskForm):
    patient_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    patient_email = EmailField('Email', validators=[DataRequired(), Email()])
    patient_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    appointment_time = SelectField('Appointment Time', validators=[DataRequired()])
    reason = TextAreaField('Reason for Visit', validators=[Length(max=500)])
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        
        # Set minimum date to tomorrow
        self.appointment_date.render_kw = {
            'min': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        }
        
        # Available time slots
        self.appointment_time.choices = [
            ('09:00', '9:00 AM'),
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('14:00', '2:00 PM'),
            ('15:00', '3:00 PM'),
            ('16:00', '4:00 PM'),
            ('17:00', '5:00 PM')
        ]

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(min=1, max=100)])
