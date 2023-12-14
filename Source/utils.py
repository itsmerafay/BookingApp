import re
from flask import jsonify 
from sqlalchemy import func
from app import db
from model import Review
from datetime import datetime, timedelta

import sys
sys.dont_write_bytecode = True

class Validations:
    
    # Password Validations
    
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$' # w is for chars, . and - as we know and then. and then for char like .com , .edu , .pk etc amd ^ for start
        
        if email is not None:
            check_email =  re.match(pattern, email)
            return check_email
        
    def is_valid_password(password):
        if len(password) < 8:
            return jsonify({
                'message':'Password is too short'
                })
        
        if not any(char.isupper() for char in password):
            return jsonify({
                'message':'There should at least one upper case letter in your password .'
                })
        
        if not any(char.islower() for char in password):
            return jsonify({
                'message':'There should at least one lower case letter in your password .'
                })
        
        if not any(char.isdigit() for char in password):
            return jsonify({
                'meesage':'There should be atleast one digit in your password .'
                })
        
        if not any(char in "@#$%^&*()_+[]}{;:,.<>?/" for char in password):
            return jsonify({
                'message':'There should be atleast one special character in your password'
            })

class Ratings:

    def get_average_rating(event_id):
        total_avg_rating = db.session.query(func.avg(Review.average_rating)).filter(Review.event_id == event_id).scalar()
        total_num_reviews = db.session.query(func.count(Review.id)).filter(Review.event_id == event_id).scalar()

        if total_avg_rating is None or total_num_reviews == 0:
            return 0
        else:
            return round(float(total_avg_rating), 2)

class DateTimeConversions:
    
    @staticmethod
    def convert_to_datetime(date_str, time_str):
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate_hours_for_duration(start_datetime, end_datetime):
        return (end_datetime - start_datetime).total_seconds() / 3600

    @staticmethod
    def calculate_days_involved(start_datetime, end_datetime):
        return (end_datetime.date() - start_datetime.date()).days + 1

    @staticmethod
    def calculate_event_hours(start_date, end_date, start_time, end_time, all_day):
        # If it's an all-day event, set start_time and end_time accordingly
        if all_day:
            start_time = "00:00:00"
            end_time = "23:59:59"

        # Convert start and end dates/times to datetime objects
        start_datetime = DateTimeConversions.convert_to_datetime(start_date, start_time)
        end_datetime = DateTimeConversions.convert_to_datetime(end_date, end_time)

        # If it's an all-day event, set end_datetime to 23:59:59 of the end_date
        if all_day:
            end_datetime = datetime.combine(end_datetime.date(), datetime.max.time())

        # Calculate total event hours for the specified time duration
        total_hours_for_duration = DateTimeConversions.calculate_hours_for_duration(start_datetime, end_datetime)

        # Calculate the number of days involved
        total_days_involved = DateTimeConversions.calculate_days_involved(start_datetime, end_datetime)

        # Use the minimum of total_hours_for_duration and total_days_involved as event_hours
        event_hours = max(total_hours_for_duration, total_days_involved * 24)

        return event_hours

