"""
seed.py  — Run this ONCE to create demo accounts in the database.

Usage:
    cd /path/to/output_project
    python3 seed.py

After running, you can log in with:
    Student  →  enrollment: 2024BTCSE001   password: password123
    Admin    →  enrollment: ADMIN001        password: admin123
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app
from models import db, Student, College
from extensions import bcrypt

app = create_app()

with app.app_context():
    # Create a college
    college = College.query.filter_by(name='School of Engineering').first()
    if not college:
        college = College(name='School of Engineering')
        db.session.add(college)
        db.session.flush()

    # Student account
    if not Student.query.filter_by(enrollment_no='2024BTCSE001').first():
        student = Student(
            enrollment_no='2024BTCSE001',
            full_name='Aarav Sharma',
            college_id=college.id,
            is_admin=False,
            is_active=True
        )
        student.set_password('password123')
        db.session.add(student)
        print('✅ Student created → 2024BTCSE001 / password123')
    else:
        print('⚠️  Student already exists.')

    # Admin account
    admin_college = College.query.filter_by(name='Administration').first()
    if not admin_college:
        admin_college = College(name='Administration')
        db.session.add(admin_college)
        db.session.flush()

    if not Student.query.filter_by(enrollment_no='ADMIN001').first():
        admin = Student(
            enrollment_no='ADMIN001',
            full_name='Admin User',
            college_id=admin_college.id,
            is_admin=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print('✅ Admin created   → ADMIN001 / admin123')
    else:
        print('⚠️  Admin already exists.')

    db.session.commit()
    print('\n🎉 Done! You can now log in at http://localhost:8000/auth/login')
