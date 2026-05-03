from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, Student, Incident, IncidentType
from .forms import StudentLoginForm, StudentRegisterForm, IncidentForm
from .extensions import bcrypt

main  = Blueprint('main',  __name__, template_folder='templates')
auth  = Blueprint('auth',  __name__, template_folder='templates')
admin = Blueprint('admin', __name__, template_folder='templates')


# ── Public Routes ──────────────────────────────────────────

@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/report', methods=['GET', 'POST'])
def report():
    form = IncidentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You must be logged in to file a report.', 'danger')
            return redirect(url_for('auth.login'))

        incident = Incident(
            victim_id=current_user.id,
            platform_id=None,
            type_id=None,
        )
        db.session.add(incident)
        db.session.commit()
        flash('Your report has been submitted successfully. Reference: SC-' + str(incident.id).zfill(4), 'success')
        return redirect(url_for('main.index'))
    return render_template('main/report.html', form=form)


@main.route('/counseling')
@login_required
def counseling():
    sessions = Incident.query.filter_by(victim_id=current_user.id).all()
    return render_template('main/counseling.html', sessions=sessions)


@main.route('/dashboard')
@login_required
def student_dashboard():
    return render_template('main/student_dashboard.html')


# ── Auth Routes ────────────────────────────────────────────

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.student_dashboard'))

    login_form = StudentLoginForm()
    reg_form   = StudentRegisterForm()

    if login_form.validate_on_submit():
        user = Student.query.filter_by(enrollment_no=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('main.student_dashboard'))
        flash('Invalid enrollment number or password.', 'danger')

    return render_template('auth/login.html', form=login_form, reg_form=reg_form)


@auth.route('/register', methods=['POST'])
def register():
    from .models import College
    form = StudentRegisterForm()
    if form.validate_on_submit():
        college = College.query.filter_by(name=form.college.data).first()
        if not college:
            college = College(name=form.college.data)
            db.session.add(college)
            db.session.flush()

        student = Student(
            enrollment_no=form.enrollment_no.data,
            full_name=form.full_name.data,
            college_id=college.id
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('auth.login'))

    # Validation failed — re-show login page with errors
    return render_template('auth/login.html', form=StudentLoginForm(), reg_form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out successfully.', 'info')
    return redirect(url_for('auth.login'))


# ── Admin Routes ───────────────────────────────────────────

@admin.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    reports = Incident.query.order_by(Incident.id.desc()).all()
    return render_template('admin/dashboard.html', reports=reports)


@admin.route('/reports/<int:report_id>/resolve', methods=['POST'])
@login_required
def resolve_report(report_id):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    report = Incident.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash(f'Report #{report_id} has been marked as resolved and archived.', 'success')
    return redirect(url_for('admin.dashboard'))
