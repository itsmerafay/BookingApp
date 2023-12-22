from app import db
from flask_bcrypt import Bcrypt
from geopy.distance import geodesic
from datetime import datetime, timedelta,date, time
from sqlalchemy import UniqueConstraint, func
from collections import defaultdict
import sys
sys.dont_write_bytecode = True

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.Text, unique=True, nullable=True)
    role = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String(255))
    # is_vendor = db.Column(db.Boolean, default=False)

    # Define the relationship between User and Vendor (one-to-one)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), unique=True, nullable=True)
    vendor = db.relationship('Vendor', back_populates='user')

    def __init__(self, email, password, role):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.access_token = None
        self.role = role


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_vendor(self):
        user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        print(self.vendor,"////")
        if self.vendor:
            user_dict['vendor'] = self.vendor.as_dict()
            user_dict['vendor_profile_complete'] = self.vendor.is_profile_complete()
        else:
            user_dict['vendor_profile_complete'] = False
        return user_dict

    def as_dict_re(self):
        user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # Exclude sensitive fields
        user_dict.pop('password_hash', None)
        user_dict.pop('access_token', None)
        return user_dict

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.String(1024), nullable=False)
    # Define the reverse relationship from Vendor to User
    user = db.relationship('User', back_populates='vendor')
    event = db.relationship('Event', back_populates='vendor')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def is_profile_complete(self):
        required_fields = [self.full_name, self.phone_number, self.location, self.biography]
        return all(field is not None and field.strip() != '' for field in required_fields)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    thumbnail = db.Column(db.String(255), nullable=True)
    other_images = db.Column(db.JSON, nullable=True)
    video_showcase = db.Column(db.String(255), nullable=True)
    # location_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    fixed_price = db.Column(db.Boolean, nullable=True)

    details = db.Column(db.String(1024), nullable=True)
    location_name = db.Column(db.String(255), nullable = True)
    services = db.Column(db.String(1024), nullable=True)

    # For services and facilities, use a JSON field for multiple images
    facilities = db.Column(db.JSON, nullable=True)
    description = db.Column(db.String(1024), nullable=True)
    event_type = db.Column(db.String(255), nullable =  True)
    latitude = db.Column(db.Float, nullable =  True)
    longitude = db.Column(db.Float, nullable =  True)
    vendor = db.relationship("Vendor", back_populates="event")

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable = False)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_total_bookings(self):
        return len(self.bookings)

    def get_total_bookings_value(self):
        return sum(booking.calculate_total_cost() for booking in self.bookings)

    def earnings_per_month(self):
        current_month = datetime.now().strftime('%Y-%m')  # Get current month in 'YYYY-MM' format
        total_earnings = 0

        for booking in self.bookings:
            if booking.start_date.strftime('%Y-%m') == current_month:
                total_earnings += booking.calculate_total_cost()

        return total_earnings


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cleanliness_rating = db.Column(db.Float, nullable=False)
    price_value_rating = db.Column(db.Float, nullable=False)
    service_value_rating = db.Column(db.Float, nullable=False)
    location_rating = db.Column(db.Float, nullable=False)
    user_review = db.Column(db.String(1024), nullable=True)
    average_rating = db.Column(db.Float, nullable=False)

    booking = db.relationship("Booking", backref="reviews")  # Represents the one-to-many relationship
    event = db.relationship("Event", backref="reviews")  # Represents the one-to-many relationship
    user = db.relationship("User", backref="reviews")  # Represents the one-to-many relationship


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
    event_type = db.Column(db.String(255), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    cancelled = db.Column(db.Boolean, default = False)
    # event_icon = db.Column(db.String(255), nullable = True)

    # bookings instead of booking bcz of many relations
    # backref used is bcz of bi-directional relationship 
    event = db.relationship("Event", backref = "bookings")
    user = db.relationship("User", backref = "bookings")

    def calculate_total_cost(self):
        start_datetime = datetime.combine(self.start_date, self.start_time)
        end_datetime = datetime.combine(self.end_date, self.end_time)
        duration = end_datetime - start_datetime
        duration_hours = duration.total_seconds() / 3600  # Convert duration to hours
        # Calculate total cost based on hourly rate
        return duration_hours * self.event.rate

    def as_dict_bk(self):
        booking_dict = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            # Check if value is an instance of date or time
            if isinstance(value, (date, time)):
                # Convert date/time to string
                booking_dict[c.name] = value.isoformat()
            else:
                booking_dict[c.name] = value
        return booking_dict
    def as_dict(self):
        event_dict = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, (date, time)):
                event_dict[c.name] = value.isoformat()
            else:
                event_dict[c.name] = value
        return event_dict

    def booking_today(self):
            booking_dict = {}
            for c in self.__table__.columns:
                value = getattr(self, c.name)
                if isinstance(value, (date, time)):
                    # Convert date/time to string
                    booking_dict[c.name] = value.isoformat()
                else:
                    booking_dict[c.name] = value

            # Include event details
            if self.event:
                booking_dict['event'] = self.event.as_dict()

            # Include total paid price
            booking_dict['total_paid_price'] = self.calculate_total_price()

            # Include user profile image
            if self.user:
                booking_dict['user_profile_image'] = self.user.profile_image

            # Include event type from the Booking table
            booking_dict['event_type'] = self.event_type

            return booking_dict


    def calculate_total_price(self):
        # Calculate the duration in hours
        start_datetime = datetime.combine(self.start_date, self.start_time)
        end_datetime = datetime.combine(self.end_date, self.end_time)
        duration = end_datetime - start_datetime
        duration_hours = duration.total_seconds() / 3600

        # Calculate the total price
        hourly_rate = self.event.rate
        total_price = duration_hours * hourly_rate
        return total_price

    def get_booking_with_event_details(self):
        booking_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, (date, time)):
                booking_dict[c.name] = value.isoformat()
            else:
                booking_dict[c.name] = value

        # Include event details
        if self.event:
            booking_dict['event'] = self.event.as_dict()

        if self.user:
            booking_dict['user_profile_image'] = self.user.profile_image
        # Include total paid price
        booking_dict['total_paid_price'] = self.calculate_total_price()

        return booking_dict


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


class Preferences(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"), nullable = False)
    event_preference = db.Column(db.JSON , nullable = True)
    vendor_preference = db.Column(db.JSON, nullable = True)

    user = db.relationship("User", backref = "preferences")



