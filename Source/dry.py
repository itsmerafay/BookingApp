import re
from flask import jsonify 
from sqlalchemy import func
from app import db
from model import Review

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