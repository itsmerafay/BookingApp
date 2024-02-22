from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta,date, time
from sqlalchemy import UniqueConstraint
from sqlalchemy import func, or_
from collections import defaultdict
import sys
sys.dont_write_bytecode = True

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(1024), unique=True, nullable=True)
    role = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String(255))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), unique=True, nullable=True)
    vendor = db.relationship('Vendor', back_populates='user')
    google_token = db.Column(db.String(255), unique=True, nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    otp = db.Column(db.String(10), nullable=True)
    device_token = db.Column(db.Text, nullable=True)
    inquiries = db.relationship("Inquiry", back_populates="user")

    favorites = db.relationship("Favorites", backref="user")  # Relationship to the 'Favorites' model


    # def __init__(self, email,password ,role, otp):
    #     self.email = email
    #     self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    #     self.access_token = None
    #     self.role = role
    #     self.otp = otp

    def __init__(self, email, password_hash, role, access_token, otp): # for the time being otp removed 
        self.email = email
        self.password_hash = password_hash
        self.access_token = None
        self.access_token = access_token
        self.role = role
        self.otp = otp


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



class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

    event = db.relationship("Event", backref="favorites")  # Relationship to the 'Event' model



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    message_type = db.Column(db.String(255))
    creation_date = db.Column(db.TIMESTAMP, server_default=func.now(), nullable=False)
    readed = db.Column(db.Boolean, default=None)
    user_id = db.Column(db.Integer)
    # Define the relationship with the User table
    def as_dict(self):
        event_dict = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, (date, time)):
                event_dict[c.name] = value.isoformat()
            else:
                event_dict[c.name] = value
        return event_dict
    
    
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Part 1
    full_name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    biography = db.Column(db.String(1024), nullable=False)
    wallet = db.Column(db.Float, server_default = '0.0' ,default = 0.0)
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
    thumbnail = db.Column(db.String(255), nullable=False)
    other_images = db.Column(db.JSON, nullable=True)
    video_showcase = db.Column(db.String(255), nullable=True)
    location_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    fixed_price = db.Column(db.Boolean, nullable=True)

    details = db.Column(db.String(1024), nullable=True)
    custom_event_name = db.Column(db.String(255), nullable = True)
    services = db.Column(db.String(1024), nullable=True)

    # For services and facilities, use a JSON field for multiple images
    facilities = db.Column(db.JSON, nullable=True)
    description = db.Column(db.String(1024), nullable=True)
    event_type = db.Column(db.String(255), nullable =  True)
    latitude = db.Column(db.Float, nullable =  True)
    longitude = db.Column(db.Float, nullable =  True)
    guest_capacity = db.Column(db.Integer, nullable =  True)
    vendor = db.relationship("Vendor", back_populates="event")
    event_timing = db.relationship("eventtiming", back_populates="event")
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"), nullable = False)
    inquiries = db.relationship("Inquiry", back_populates="event")
    extra_facilities = db.relationship("ExtraFacility", back_populates="event", lazy='joined')

    def as_dict(self):
        # converting event objects into a dictionary, extracting name and values of the columns by getattr
        event_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        event_timings = eventtiming.query.filter_by(event_id=self.id).all()
        
        event_dict["event_timings"] = {
            timing.day_of_week: {
                "start_time": timing.start_time.isoformat() if timing.start_time else None,
                "end_time": timing.end_time.isoformat() if timing.end_time else None
            } for timing in event_timings
        }

        # extra facilities
        event_dict["extra_facilities"] = [{
            "name":facility.name,
            "image":facility.image,
            "rate":facility.rate,
            "rate":facility.rate,
            "unit":facility.unit
            
        } for facility in self.extra_facilities]

        return event_dict

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




class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    additional_notes = db.Column(db.String(1024), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    all_day = db.Column(db.Boolean, default=False)
    event_type = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cancelled = db.Column(db.Boolean, default=False)

    # event = db.relationship("Event", backref="inquiries")
    # user = db.relationship("User", backref="inquiries_user")

    event = db.relationship("Event", back_populates="inquiries")
    user = db.relationship("User", back_populates="inquiries")


    # event = db.relationship('Event', back_populates='event_timing')

    # event_timing = db.relationship("eventtiming", back_populates="event")




    def as_dict(self):
        inquiry_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # converting time objects into string
        for key, value in inquiry_dict.items():
            if isinstance(value,time):
                inquiry_dict[key] = value.strftime("%H:%M:%S") if value else None 
        event_details = {
            "location_name":self.event.location_name if self.event else None,
        }

        inquiry_dict["event_details"] = event_details
        return inquiry_dict


class ExtraFacility(db.Model):
    __tablename__ = 'extra_facility'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=True)
    image = db.Column(db.JSON, nullable=True)
    rate = db.Column(db.Float, nullable=True, server_default='0')
    unit = db.Column(db.String(255), nullable=True)

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    event = db.relationship("Event", back_populates="extra_facilities")
    def as_dict(self):
        facility_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # Include the image field in the dictionary
        facility_dict["image"] = self.image
        return facility_dict


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
    # bookings instead of booking bcz of many relations
    # backref used is bcz of bi-directional relationship 
    event = db.relationship("Event", backref = "bookings")
    user = db.relationship("User", backref = "bookings")
    extra_facility_id = db.Column(db.Integer, db.ForeignKey("extra_facility.id"))
    extra_facilities = db.relationship("BookingExtraFacility", backref="bookings", lazy="joined")

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

    def as_dict_po(self):
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

           # Include extra_facilities if present
        if self.extra_facilities:
            booking_dict["extra_facilities_user_booked"] = [facility.as_dict() for facility in self.extra_facilities]

        # Include event details
        if self.event:
            booking_dict['event'] = self.event.as_dict()

        if self.user:
            booking_dict['user_profile_image'] = self.user.profile_image
        # Include total paid price
        booking_dict['total_paid_price'] = self.calculate_total_price()

        return booking_dict


class BookingExtraFacility(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    booking_id = db.Column(db.ForeignKey("booking.id"), nullable = False)
    extra_facility_id = db.Column(db.ForeignKey("extra_facility.id"), nullable = False)
    unit = db.Column(db.String(10), nullable = False)
    quantity = db.Column(db.Float, nullable = False)
    image = db.Column(db.JSON, nullable=True)
    extra_facility = db.relationship("ExtraFacility", lazy="joined")

    def as_dict(self):
        facility_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # Include the image field from the ExtraFacility model
        if self.extra_facility:
            facility_dict["image"] = self.extra_facility.image
            facility_dict["rate"] = self.extra_facility.rate
        return facility_dict

class eventtiming(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    available = db.Column(db.Boolean, nullable = True, default = False)

    event = db.relationship('Event', back_populates='event_timing')


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



class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    user_type = db.Column(db.String(10), nullable = False)
    transaction_time = db.Column(db.DateTime, default = datetime.utcnow(), nullable = False)
    transaction_amount = db.Column(db.Float , nullable = False)
    trans_id = db.Column(db.String(255), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)

    def __init__(self, user_id, user_type, transaction_amount, trans_id, transaction_time, transaction_type):
        self.user_id = user_id
        self.user_type = user_type
        self.transaction_amount = transaction_amount
        self.trans_id = trans_id  # Correcting the attribute name
        self.transaction_time = transaction_time
        self.transaction_type = transaction_type