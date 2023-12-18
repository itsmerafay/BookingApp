import re
from flask import jsonify 
from geopy.distance import geodesic
from sqlalchemy import func
from app import db
from model import Review, Booking, Event
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


class BookingAvailability:
    def check_availability(booking, current_date_time):
        start_datetime = datetime.combine(booking.start_date, booking.start_time)
        end_datetime = datetime.combine(booking.end_date , booking.end_time)

        if start_datetime <= current_date_time <= end_datetime:
            return True
        else:
            return False


class Filterations:

    # Filteration based event location 
    @staticmethod
    def filter_events_by_location(events_data, user_location, max_distance=None):
        filtered_events = [
            event for event in events_data
            if Filterations.is_valid_latitude(event.get("event_latitude")) and
               Filterations.is_valid_longitude(event.get("event_longitude")) and
               Filterations.calculate_distance(user_location, (event.get("event_latitude"), event.get("event_longitude"))) <= max_distance
        ]
        return filtered_events
    
    @staticmethod
    def is_valid_latitude(latitude):
        return -90 <= latitude <= 90 if latitude is not None else False

    @staticmethod
    def is_valid_longitude(longitude):
        return -180 <= longitude <= 180 if longitude is not None else False


    @staticmethod
    def calculate_distance(location1, location2):
        return geodesic(location1, location2).km if location1 and location2 else float('inf')


    @staticmethod
    def calculate_distance(location1, location2):
        return geodesic(location1, location2).km if location1 and location2 else float('inf')
    # Filteration based cheapest events 

    @staticmethod
    def filter_events_by_cheapest(events_data):
        filtered_events = sorted(events_data, key=lambda x: x.get("event_rate", float("inf")))
        return filtered_events

    # Filteration based filter events by least rated

    @staticmethod
    def filter_events_by_least_rated(events_data):
        filtered_events = [
            event for event in events_data 
            if Ratings.get_average_rating(event.get("event_id")) <= 4
        ]
        
        return filtered_events
    
    # Filteration based filter top rated events

    @staticmethod
    def filter_events_by_top_rated(events_data):
        filtered_events = [
            event for event in events_data
            if Ratings.get_average_rating(event.get("event_id")) == 5
        ]
        return filtered_events
    
    @staticmethod
    def filtered_events_by_trending(events_data):
        current_datetime = datetime.now()
        filtered_events = sorted(events_data , key = lambda event : len([
            booking for booking in event.get("bookings", [])
            if booking["start_date"] <= current_datetime <= booking["end_date"]
        ]), reverse = True)
        print(len(events_data))
        return filtered_events
    

    @staticmethod
    def apply_filters(events_data, prefered_filter, user_location, max_distance=None):
        if prefered_filter.lower() == "my_location":
            filtered_events = Filterations.filter_events_by_location(events_data, user_location, max_distance)
            return filtered_events
        
        if prefered_filter.lower() == "cheapest":
            filtered_events = Filterations.filter_events_by_cheapest(events_data)
            return filtered_events
        
        if prefered_filter.lower() == "least_rated":
            filtered_events = Filterations.filter_events_by_least_rated(events_data)
            return filtered_events

        if prefered_filter.lower() ==  "top_rated":
            filtered_events = Filterations.filter_events_by_top_rated(events_data)
            return filtered_events

        if prefered_filter.lower() == "trending":
            filtered_events = Filterations.filtered_events_by_trending(events_data)
            return filtered_events

        else:
            filtered_events = events_data
            return filtered_events


class BookingCount:

    def count_booking(event_id):   
        try:
            booking_count = Booking.query.filter_by(event_id=event_id).count()

        except Exception as e:
            print(f"Error fetching booking count : {e}")
            return 0