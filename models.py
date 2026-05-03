from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class College(db.Model):
    __tablename__ = 'college'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    students = db.relationship('Student', back_populates='college', lazy='dynamic')

    def __repr__(self):
        return f'<College {self.name}>'


class Student(UserMixin, db.Model):
    __tablename__ = 'student'

    id            = db.Column(db.Integer, primary_key=True)
    enrollment_no = db.Column(db.String(50), unique=True, nullable=False)
    full_name     = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active     = db.Column(db.Boolean, default=True)
    is_admin      = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    college    = db.relationship('College', back_populates='students')

    incidents_as_victim = db.relationship(
        'Incident', foreign_keys='Incident.victim_id',
        back_populates='victim', lazy='dynamic'
    )
    incidents_as_perpetrator = db.relationship(
        'Incident', foreign_keys='Incident.perpetrator_id',
        back_populates='perpetrator', lazy='dynamic'
    )
    incidents_reported = db.relationship(
        'Incident', foreign_keys='Incident.reported_by_id',
        back_populates='reported_by', lazy='dynamic'
    )

    def set_password(self, raw_password):
        from .extensions import bcrypt
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        from .extensions import bcrypt
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f'<Student {self.full_name} ({self.enrollment_no})>'


class Platform(db.Model):
    __tablename__ = 'platform'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Platform {self.name}>'


class IncidentType(db.Model):
    __tablename__ = 'incident_type'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<IncidentType {self.name}>'


class Incident(db.Model):
    __tablename__ = 'incident'

    id = db.Column(db.Integer, primary_key=True)

    victim_id      = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    perpetrator_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    reported_by_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    platform_id    = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=True)
    type_id        = db.Column(db.Integer, db.ForeignKey('incident_type.id'), nullable=True)

    # Extra fields for better incident tracking
    description    = db.Column(db.Text, nullable=True)
    severity       = db.Column(db.String(20), default='medium')
    status         = db.Column(db.String(30), default='open')
    is_anonymous   = db.Column(db.Boolean, default=False)
    evidence_url   = db.Column(db.String(500), nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    victim      = db.relationship('Student', foreign_keys=[victim_id],      back_populates='incidents_as_victim')
    perpetrator = db.relationship('Student', foreign_keys=[perpetrator_id], back_populates='incidents_as_perpetrator')
    reported_by = db.relationship('Student', foreign_keys=[reported_by_id], back_populates='incidents_reported')
    platform    = db.relationship('Platform')
    type        = db.relationship('IncidentType')

    def __repr__(self):
        return f'<Incident #{self.id} [{self.severity}] {self.status}>'
