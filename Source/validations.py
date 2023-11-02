import re
from flask import jsonify

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