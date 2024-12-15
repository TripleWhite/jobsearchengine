from datetime import datetime, UTC
import bcrypt
from app import db
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64))
    resume_text = db.Column(db.Text)
    resume_parsed_data = db.Column(db.Text)  # Stored as JSON string
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def set_resume_parsed_data(self, data):
        self.resume_parsed_data = json.dumps(data)

    def get_resume_parsed_data(self):
        return json.loads(self.resume_parsed_data) if self.resume_parsed_data else None

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'resume_text': self.resume_text,
            'resume_parsed_data': self.get_resume_parsed_data(),
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120), nullable=False, index=True)
    company_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False, index=True)
    responsibilities = db.Column(db.Text, nullable=False)  # Stored as JSON string
    requirements = db.Column(db.Text, nullable=False)      # Stored as JSON string
    raw_jd_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    def set_responsibilities(self, responsibilities_list):
        self.responsibilities = json.dumps(responsibilities_list)

    def get_responsibilities(self):
        return json.loads(self.responsibilities) if self.responsibilities else []

    def set_requirements(self, requirements_list):
        self.requirements = json.dumps(requirements_list)

    def get_requirements(self):
        return json.loads(self.requirements) if self.requirements else []

    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'company_name': self.company_name,
            'location': self.location,
            'responsibilities': self.get_responsibilities(),
            'requirements': self.get_requirements(),
            'raw_jd_text': self.raw_jd_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
