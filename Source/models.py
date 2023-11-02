from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from sqlalchemy import UniqueConstraint

import sys
sys.dont_write_bytecode = True

bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), unique=True, nullable=True)
    role = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String(255))
    is_vendor = db.Column(db.Boolean, default=False)

    # Define the relationship between User and Vendor (one-to-one)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), unique=True, nullable=True)
    vendor = db.relationship('Vendor', back_populates='user')

    def __init__(self, email, password, role):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.access_token = None
        self.role = role
        self.is_vendor = role == "vendor"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Part 1
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.String(1024), nullable=False)
    # Define the reverse relationship from Vendor to User
    user = db.relationship('User', back_populates='vendor')
    event = db.relationship('Event', back_populates='vendor')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    thumbnail = db.Column(db.String(255), nullable=False)
    other_images = db.Column(db.JSON, nullable=True)
    video_showcase = db.Column(db.String(255), nullable=True)
    location_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.String(255), nullable=False)
    fixed_price = db.Column(db.Boolean, nullable=True)

    details = db.Column(db.String(1024), nullable=True)
    services = db.Column(db.String(1024), nullable=True)

    # For services and facilities, use a JSON field for multiple images
    facilities = db.Column(db.JSON, nullable=True)
    description = db.Column(db.String(1024), nullable=True)
    event_type = db.Column(db.String(255), nullable =  True)

    vendor = db.relationship("Vendor", back_populates="event")

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable = False)



class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    guest_count = db.Column(db.Integer, nullable = False)
    additional_notes = db.Column(db.String(1024), nullable = True)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    all_day = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    # bookings instead of booking bcz of many relations
    # backref used is bcz of bi-directional relationship 
    event = db.relationship("Event", backref = "bookings")
    user = db.relationship("User", backref = "bookings")


    def calculate_total_cost(self):
        pass

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expired_at = db.Column(db.DateTime)

    def __init__(self, user_id, token, expires_in_minutes):
        self.user_id = user_id
        self.token = token
        self.expired_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)

























# from app import db
# from flask_bcrypt import Bcrypt
# from datetime import datetime, timedelta
# from sqlalchemy import UniqueConstraint

# import sys
# sys.dont_write_bytecode = True

# bcrypt = Bcrypt()


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     access_token = db.Column(db.String(255), unique=True, nullable=True)
#     role = db.Column(db.String(50), nullable=False)
#     profile_image = db.Column(db.String(255))
#     is_vendor = db.Column(db.Boolean, default=False)

#     # Define the relationship between User and Vendor (one-to-one)
#     vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), unique=True, nullable=True)
#     vendor = db.relationship('Vendor', back_populates='user')

#     def __init__(self, email, password, role):
#         self.email = email
#         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
#         self.access_token = None
#         self.role = role
#         self.is_vendor = role == "vendor"

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password_hash, password)


# class Vendor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
#     # Part 1
#     full_name = db.Column(db.String(255), nullable=False)
#     phone_number = db.Column(db.String(255), nullable=False)
#     location = db.Column(db.String(255), nullable=False)
#     biography = db.Column(db.String(1024), nullable=False)
#     # Define the reverse relationship from Vendor to User
#     user = db.relationship('User', back_populates='vendor')
#     event = db.relationship('Event', back_populates='vendor')


# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     thumbnail = db.Column(db.String(255), nullable=False)
#     other_images = db.Column(db.JSON, nullable=True)
#     video_showcase = db.Column(db.String(255), nullable=True)
#     location_name = db.Column(db.String(255), nullable=False)
#     address = db.Column(db.String(255), nullable=False)
#     rate = db.Column(db.String(255), nullable=False)
#     fixed_price = db.Column(db.Boolean, nullable=True)

#     details = db.Column(db.String(1024), nullable=True)
#     services = db.Column(db.String(1024), nullable=True)

#     # For services and facilities, use a JSON field for multiple images
#     facilities = db.Column(db.JSON, nullable=True)
#     description = db.Column(db.String(1024), nullable=True)
#     event_type = db.Column(db.String(255), nullable =  True)

#     vendor = db.relationship("Vendor", back_populates="event")

#     vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable = False)




# class PasswordResetToken(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     token = db.Column(db.String(255), unique=True, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     expired_at = db.Column(db.DateTime)

#     def __init__(self, user_id, token, expires_in_minutes):
#         self.user_id = user_id
#         self.token = token
#         self.expired_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
