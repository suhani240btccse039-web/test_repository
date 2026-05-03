from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from .models import Student



class StudentLoginForm(FlaskForm):
    username = StringField(
        'Enrollment No.',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enrollment No.'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Password'}
    )



class StudentRegisterForm(FlaskForm):
    enrollment_no = StringField(
        'Enrollment No.',
        validators=[DataRequired(), Length(max=50)]
    )
    full_name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(max=120)]
    )
    college = StringField(
        'College',
        validators=[DataRequired(), Length(max=120)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords do not match')]
    )

    def validate_enrollment_no(self, field):
        """Check enrollment number is not already registered."""
        if Student.query.filter_by(enrollment_no=field.data).first():
            raise ValidationError('This enrollment number is already registered.')



# ── Incident Report ────────────────────────────────────────────────────────────

class IncidentForm(FlaskForm):
    victim = StringField(
        'Victim',
        validators=[DataRequired(), Length(max=120)]
    )
    perpetrator = StringField(
        'Perpetrator',
        validators=[Optional(), Length(max=120)]
    )
    platform = StringField(
        'Platform',
        validators=[Optional(), Length(max=120)]
    )
    type = SelectField(
        'Incident Type',
        choices=[
            ('harassment',      'Harassment'),
            ('cyberbullying',   'Cyberbullying'),
            ('ragging',         'Ragging'),
            ('discrimination',  'Discrimination'),
            ('assault',         'Assault'),
            ('other',           'Other'),
        ],
        validators=[DataRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=20, max=2000)]
    )
    evidence_url = URLField(
        'Evidence URL',
        validators=[Optional()]
    )
    severity = SelectField(
        'Severity',
        choices=[
            ('low',      'Low'),
            ('medium',   'Medium'),
            ('high',     'High'),
            ('critical', 'Critical'),
        ],
        validators=[DataRequired()]
    )
    status = SelectField(
        'Status',
        choices=[
            ('open',        'Open'),
            ('under_review','Under Review'),
            ('resolved',    'Resolved'),
            ('closed',      'Closed'),
        ],
        default='open',
        validators=[DataRequired()]
    )
