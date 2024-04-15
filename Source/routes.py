import random
from sqlalchemy import func, or_
from utils import Validations
from app import app, db, mail
from sqlalchemy.orm import joinedload
from utils import Validations, Ratings, DateTimeConversions, Notificationpush, BookingAvailability, Filterations, Password
from flask import request, jsonify, url_for, current_app, send_file, send_from_directory
from datetime import datetime, timedelta
from model import User, PasswordResetToken, Vendor, Event, Booking , Review, eventtiming, Inquiry, ExtraFacility,Favorites, Transaction, Notification, BookingExtraFacility, Preferences         
import secrets
from sqlalchemy.exc import IntegrityError
import uuid
import base64
from flask_mail import Message
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity, decode_token
from model import bcrypt   
from werkzeug.utils import secure_filename
import os
from google.oauth2 import id_token
import google.auth.transport.requests as req
from geopy.distance import geodesic
import sys
import string
from firebase_admin import auth
from dotenv import load_dotenv
from google.auth.exceptions import InvalidValue
import stripe 
sys.dont_write_bytecode = True

stripe.api_key = app.config["STRIPE_SECRET_KEY"]
load_dotenv()


######################### Set User Preferences ############################


@app.route("/set_user_preferences", methods = ["POST","PUT"])
@jwt_required()
def set_user_preference():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message":"User not authenticated !!"
            }), 401

        if user.role != "user":
            return jsonify({
                "status":False,
                "message":"Unauthorized access: Only users can set preferences"
            })
        
        user_preference = Preferences.query.filter_by(user_id = user.id).first()

        event_preference = data.get("event_preferences")
        vendor_preference = data.get("vendor_preferences")
        guest_count =  data.get("guest_count")

        if not user_preference:
            user_preference = Preferences(user_id=user.id , event_preference=event_preference, vendor_preference=vendor_preference, guest_count=guest_count)
            db.session.add(user_preference)
        else:
            user_preference.event_preference = event_preference
            user_preference.vendor_preference = vendor_preference
            user_preference.guest_count = guest_count
            
        db.session.commit()

        return jsonify({
            "status":True,
            "message":"User preference set successfully !!"
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500




######################### Category ############################# 


@app.route("/category", methods = ["GET"])
def category():
    try:
        event_types_count = db.session.query(Event.event_type, func.count(Event.id)).group_by(Event.event_type).all()
        if not event_types_count:
            return jsonify({
                "status":False,
                "message":"Not found"
            }), 404
        
        event_icon_path = os.path.join(app.static_folder, "event_icons")
        event_icon_file = os.listdir(event_icon_path)

        event_types_data = []

        for event_type , count in event_types_count:
            image_url = None
            for filename in event_icon_file:
                if event_type.lower() in filename.lower():
                    image_url = url_for("static", filename=f"event_icons/{filename}")
                    break

            event_type_data = {
                "name":event_type,
                "image_url":image_url,
                "total_count": count
            }
            event_types_data.append(event_type_data)
        return jsonify({
            "status":True,
            "event_categories":event_types_data
        }), 200

    except Exception as e:
        return jsonify({
            "status":False,
            "message":str(e)
        }), 500

















######################### Security ############################



@app.route("/security", methods =  ["PUT"])
@jwt_required()
def security():
    data = request.get_json()
    current_user = get_current_user()

    if not current_user:
        return jsonify({
            "status":False,
            "message":"User should be authenticated to access the security !!"
        }), 401
    
    email = data.get("email")
    password = data.get("password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not all([email,password,new_password,confirm_password]):
        return jsonify({
            "message":"All fields should be filled !! "
        }), 400
    

    user = User.query.filter_by(email=email).first()

    if not user  :
        return jsonify({
            "status":False,
            "message":"User not found !!"
        }), 400
    
    if user.email != email:
        return jsonify({
            "status":False,
            "message":"Please enter your correct email !!"
        }), 400
    
    if not user.check_password(password):
        return jsonify({
            "status":False,
            "message":"Please enter correct password !!"
        }), 400
    # print(user.check_password)

    if new_password !=  confirm_password:
        return jsonify({
            "status":False,
            "message":"Please enter same password for both fields"
        }), 400
    
    password_validation_result = Validations.is_valid_password(new_password)
    print(password_validation_result)
    
    if password_validation_result:
        return jsonify({
            "status":False,
            "message":"Please enter strong password !!"
        }), 400

    user.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    db.session.commit()

    return jsonify({
        "message":"Password updated successfully !!"
    }), 200


###############################     Google Auth     ######################################

# working
@app.route('/google_login', methods=['POST'])
def google_login():
    try:
        data = request.get_json()
        token = data.get("token")
        client_id = os.environ.get("GOOGLE_CLIENT_ID")  # Correct environment variable name
        idinfo = id_token.verify_oauth2_token(token, req.Request(), client_id)

        print(idinfo['email'])  # email
        print(idinfo['picture'])  # profile image

        email = idinfo.get("email")
        profile_image = idinfo.get("picture")

        if not email:
            return jsonify({
                    "status":False,
                    "message":"Invalid Email provided"  
                }), 400

        access_token = create_access_token(identity=email, expires_delta=False) 
            
        user = User.query.filter_by(email=email).first()
        if user :
            if profile_image:
                user.profile_image = profile_image
            if not user.role:
                return jsonify({
                        "status":False,
                        "message":"User Registration incomplete due to role !"
                    }), 400
                
            user.access_token = access_token
            user.google_token = token
            db.session.commit()  # Committing here after updating access_token
            
        else:
            role = data.get("role")
            password = Password.generate_random_password()
            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

            user = User(email=email, password_hash=password_hash, role=role, access_token=access_token)
            user.google_token = token

            if profile_image:
                user.profile_image = profile_image

                # Add the user to the database
            db.session.add(user)
            db.session.commit()

        return jsonify({
                "status": True,
                "message": "Successfully logged in using google",
                "role": user.role,
                "id": user.id,
                "profile_image": profile_image,
                "access_token": access_token
            }), 200

    except InvalidValue as e:
        # print(idinfo["client_id"])
        return jsonify({
            "status": False,
            "message": "Invalid token or client ID",
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500



# @app.route('/google_login', methods=['POST'])
# def google_login():
#     data = request.get_json()
#     token = data.get("token")
#     client_id = os.environ.get("client_id")
#     idinfo = id_token.verify_oauth2_token(token, req.Request(), client_id)

#     print(idinfo['email'])  # email
#     print(idinfo['picture'])  # profile image
#     print(idinfo)

#     email = idinfo.get("email")
#     profile_image = idinfo.get("picture")

#     if not email:
#         return jsonify({
#                 "status":False,
#                 "message":"Invalid Email provided"  
#             }), 400

#     access_token = create_access_token(identity=email)
        
#     user = User.query.filter_by(email=email).first()
#     if user :
#         if profile_image:
#             user.profile_image = profile_image
#         if not user.role:
#             return jsonify({
#                     "status":False,
#                     "message":"User Registration incomplete due to role !"
#                 }), 400
            
#         user.access_token = access_token
#         user.google_token = token
#         db.session.commit()  # Committing here after updating access_token
        
#     else:
#         role = data.get("role")
#         password = Password.generate_random_password()
#         password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

#         user = User(email=email, password_hash=password_hash, role=role, access_token=access_token)
#         user.google_token = token

#         if profile_image:
#             user.profile_image = profile_image

#             # Add the user to the database
#         db.session.add(user)
#         db.session.commit()

#     return jsonify({
#             "status": True,
#             "message": "Successfully logged in using google",
#             "role": user.role,
#             "id": user.id,
#             "profile_image": profile_image,
#             "access_token": access_token
#         }), 200
    




# @app.route('/google_login', methods=['POST'])
# def google_login():
#     try:
#         data = request.get_json()
#         token = data.get("token")
#         client_id = data.get("client_id")
#         idinfo = id_token.verify_oauth2_token(token, req.Request(), client_id)

#         print(idinfo['email'])  # email
#         print(idinfo['picture'])  # profile image

#         email = idinfo.get("email")
#         print(email)
#         profile_image = idinfo.get("picture")

#         access_token = create_access_token(identity=email)

#         role = data.get("role")

#         user = User.query.filter_by(email=email).first()
#         if user:
#             user.access_token = access_token
#             user.google_token = token
#             db.session.commit()  # Committing here after updating access_token
            
#             return jsonify({
#                 "status": True,
#                 "message": "Successfully logged in using google",
#                 "role": user.role,
#                 "id": user.id,
#                 "profile_image": profile_image,
#                 "access_token": access_token
#             })

#         password = Password.generate_random_password()
#         password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

#         # Create the User instance and pass the password hash
#         user = User(email=email, password_hash=password_hash, role=role, otp=None, access_token=access_token)

#         # Set the profile_image attribute
#         user.profile_image = profile_image

#         # Add the user to the database
#         db.session.add(user)
#         db.session.commit()

#         return jsonify({
#             "status": True,
#             "message": "Successfully logged in using google",
#             "role": user.role,
#             "id": user.id,
#             "profile_image": profile_image,
#             "access_token": access_token
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": False,
#             "error": str(e)
#         }), 500



###############################     Route For Create Inquiry     ######################################


@app.route("/create_inquiry", methods = ["POST"])
@jwt_required()
def create_inquiry():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can create bookings."
            }), 401

        event_id = data.get("event_id")

        event = Event.query.filter_by(id = event_id)
        if not event:
            return jsonify({
                "status":False,
                "message":"Event doesn't exist !!"
            }), 404
        
        new_inquiry = Inquiry(
            event_id = event_id,
            user_id = user.id,
            full_name=data.get("full_name"),
            email=data.get("email"),
            guest_count=data.get("guest_count"),
            additional_notes=data.get("additional_notes"),
            start_date = data.get("start_date"),
            end_date = data.get("end_date"),
            start_time = data.get("start_time"),
            end_time = data.get("end_time"),
            all_day = data.get("all_day", False),
            event_type = data.get("event_type"),
        )
        db.session.add(new_inquiry)
        db.session.commit()

        return jsonify({
            "status":True,
            "message":"Successfully submitted the inquiry !!"
        }), 200

    
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500





# new
# for both user and vendor
# get specific inquiry with inqiry_id for both user and vendor
@app.route("/get_specific_inquiry/<int:inquiry_id>", methods = ["GET"])
@jwt_required()
def get_specific_inquiry(inquiry_id):
    try:
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role == "user":
            inquiry = Inquiry.query.filter_by(user_id = user.id, id = inquiry_id).first()

        elif user.role == "vendor":
            inquiry = Inquiry.query.join(Event).filter(Event.vendor_id == user.vendor.id , Inquiry.id == inquiry_id).first()

        if not inquiry:
            return jsonify({
                "status":False,
                "message":"Inquiry doesn't exist !!"
            }), 404

        inquiries_data = inquiry.as_dict()
        
        
        return jsonify({
            "status":True,
            "inquiries_data":inquiries_data
        }), 200

    
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500


@app.route("/update_event/<int:event_id>", methods = ["PUT"])
@jwt_required()
def update_event(event_id):
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message":"User Not Found !!"
            }), 401

        if user.role != "vendor":
            return jsonify({
                "status":False,
                "message":"User Authentication Error !!!"
            })

        # Ensuring that user is associated with a vendor profile
        if not user.vendor:
            return jsonify({
                "status":False,
                "message":"User is not associated with a vendor profile make sure to complete the vendor profile first !!! "
            })

        # Basically used this here so that we should know that the user is associated with a vendor profile or not
        # Here we are actually retrieving the vendor profile associated with a user
        vendor = user.vendor

        # Giving the database two pieces of information to find the right event
        # Here vendor is that vendor associated with a user profile

        event = Event.query.filter_by(id = event_id, vendor = vendor).first()
        if not event:   
            return jsonify({
                "status":False,
                "message":"Event Doesn't Exist !!"
            })

        # Updating the fields
        # How it works ? It will get the thumbnail value from field at the time of update but if we don't get the value then it will make it remain for the old value
        event.thumbnail = data.get("thumbnail", event.thumbnail)
        event.other_images = data.get("other_images", event.other_images)
        event.video_showcase = data.get("video_showcase", event.video_showcase)
        event.location_name = data.get("location_name", event.location_name)
        event.address = data.get("address", event.address)
        event.rate = float(data.get("rate", event.rate))
        event.fixed_price = data.get("fixed_price", event.fixed_price)
        event.details = data.get("details", event.details)
        event.services = data.get("services", event.services)
        event.facilities = data.get("facilities", event.facilities)
        event.description = data.get("description", event.description)
        event.event_type = data.get("event_type", event.event_type)
        event.longitude = data.get("longitude", event.event_type)
        event.latitude = data.get("latitude", event.event_type)


        # Getting the byte codes for the images to be updated
        if data.get("thumbnail"):
            thumbnail_filename = f"{uuid.uuid4()}.png"
            thumbnail_path = os.path.join(app.config["VENDOR_IMAGES_FOLDER"], thumbnail_filename)        
            
            # base 64 data and path to access image from the directory
            # will return filename
            
            save_image_from_base64(data["thumbnail"],thumbnail_path )
            
            # will store the image name i.e, image.png to thumnail column

            event.thumbnail = thumbnail_filename


        if data.get("other_images"):
            event.other_images = save_multiple_images_from_base64(data["other_images"])


        if data.get("facilities"):
            event.facilities = save_multiple_images_from_base64(data["facilities"])

        db.session.commit()

        return jsonify({
            "status":True,
            "message":"Event Updated Successfully !!!"
        })


    except Exception as e:
        print(str(e))
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500



@app.route("/upload_event_icon", methods = ["POST"])
@jwt_required()
def upload_event_icon():
    user = get_current_user()
    UPLOAD_FOLDER = "static"
    EVENT_ICON_SUBFOLDER = "event_icons"
    app.config["EVENT_ICON_FOLDER"] = os.path.join(UPLOAD_FOLDER, EVENT_ICON_SUBFOLDER)
    data = request.get_json()
    event_type = data.get("event_type")
    event_icon = data.get("event_icon")

    try :
        if user.role != "vendor":
            return jsonify({
                "status":False,
                "message":"Authorization error , only vendor can upload an icon !!"
            }), 401
        
        if not event_type or not event_icon:
            return jsonify({
                "status":False,
                "message":"Event type or icon not provided !!"
            }), 400
        
        event_icon_bytes = base64.b64decode(event_icon)
        event_icon_filename = f"{event_type.lower()}_icon_{uuid.uuid4()}.png"
        event_icon_path = os.path.join(app.config["EVENT_ICON_FOLDER"], event_icon_filename)

        if not os.path.exists(app.config["EVENT_ICON_FOLDER"]):
            os.makedirs(app.config["EVENT_ICON_FOLDER"])

        with open(event_icon_path, "wb") as icon_file:
            icon_file.write(event_icon_bytes)

        return jsonify({
            "status":True,
            "message":"Event icon created successfully !!",
            "file_path":event_icon_path,
        }), 200

        
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500






# fin
@app.route('/update_event_hours', methods=["POST"])
@jwt_required()
def update_event_hours():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User not authenticated !!"
            }), 401

        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendors can update their event timings."
            }), 401

        event_id = data.get("event_id")
        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return jsonify({
                "status": False,
                "message": "Can't Update event hours as event does not exist !"
            }), 404
        
        timings = data.get("timings")

        for day_of_week, timing_data in timings.items():
            start_time = timing_data.get("start_time")
            end_time = timing_data.get("end_time")

            # Check if eventtiming entry exists, if not create a new one
            event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=day_of_week).first()
            if not event_timings:
                event_timings = eventtiming(event_id=event_id, day_of_week=day_of_week)

            # Update start_time and end_time
            if start_time is not None:
                event_timings.start_time = datetime.strptime(start_time, "%H:%M:%S").time()
            if end_time is not None:
                event_timings.end_time = datetime.strptime(end_time, "%H:%M:%S").time()

            db.session.add(event_timings)  # Add event_timings to the session for update

        db.session.commit()

        return jsonify({
            "status": True,
            "message": "Successfully updated the working hours !!"
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500




@app.route('/signup', methods=['POST'])  # Updated route
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get("password")
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        role = data.get('role')  # Get the user's role from the request

        # Validate email and password using your Validations class
        email_validation_result = Validations.is_valid_email(email)
        password_validation_result = Validations.is_valid_password(password)

        if email_validation_result is None:
            return jsonify({"message": "Invalid Email Address","status":False}), 400

        if password_validation_result is not None:
            return password_validation_result, 400 # json response result according to the error

        if not email or not password or not role:
            return jsonify({'message': 'Email, password, and role are required',"status":False}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists',"status":False}), 400

        if role not in ['user', 'vendor']:
            return jsonify({"message": "Invalid Role","status":False}), 400
        # gen_otp = ''.join(random.choices(string.digits, k=4))
        # user = User(email=email, password=password, role=role, otp=gen_otp)  # Pass the role during user creation
        # msg = Message('Email verification', sender='noreply@gmail.com', recipients=[email])
        # msg.body = f"This is your OTP for email verification {gen_otp}"
        # mail.send(msg)
        user = User(email=email, password_hash=password_hash, role=role, otp=None, access_token=None)  # Pass the role during user creation

        if role == "vendor":
                vendor = user.vendor
                # If vendor profile doesn't exist then create a new one
                if not vendor:
                    vendor_data = {
                        'full_name': "",
                        'phone_number': "",
                        'location': "",
                        'biography': ""
                    }
                    vendor = Vendor(**vendor_data)
                    user.vendor = vendor
                    #db.session.commit()
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"status":True, "message": "Registered Successfully !!"})
    except Exception as e:
        print(e)
        return jsonify({"status":False, "error":str(e)})



###############################     Route For SignIn      ######################################



# @app.route("/verify_otp",methods=["POST"])
# def verify_otp():
#     data = request.get_json()
#     otp = data.get("otp")
#     email = data.get('email')
#     device_token = data.get("device_token")
#     user = User.query.filter_by(email=email,otp=otp).first()
#     if not user:
#         return jsonify({"status":False,'message': 'Invalid credentials'}), 401
#     user.verified = True
#     user.otp=None
#     db.session.commit()
#     access_token = create_access_token(identity=email)
#     user.device_token = device_token
#     db.session.commit()
    
#     return jsonify({
#         "status":True,
#         "access_token": access_token,
#         "message": "Successfully Logged In !!",
#         "role":user.role,
#         "id":user.id,
#         "profile_image":user.profile_image
#     })



@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # device_token = data.get("device_token")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"status":False,'message': 'Invalid credentials'}), 401

    if not user.role:  # This line is not necessary, as 'role' should always be present due to your database model
        return jsonify({"status":False,"message": "Please specify if you are signing in as a user or a vendor"}), 400
    # if not user.verified:
    #     return jsonify({"status":False,"message":"not_verified"})
    # Generate the access token
    access_token = create_access_token(identity=email, expires_delta=False)

    # Update the user's access_token column with the new access token
    user.access_token = access_token
    # user.device_token = device_token
    db.session.commit()

    return jsonify({
        "status":True,
        "access_token": access_token,
        "message": "Successfully Logged In !!",
        "role":user.role,
        "id":user.id,
        "profile_image":user.profile_image
    }), 200



###############################     Function For Getting The Current User      ######################################


def get_current_user():
    # Get the identity (user's email) from the JWT token
    current_user_email = get_jwt_identity()
    # Use the email to retrieve the user from the database
    user = User.query.filter_by(email=current_user_email).first()
    return user



###############################     Route For Protected Route      ######################################



@app.route('/protected_route', methods=['GET'])
@jwt_required()
def protected_route():
    user = get_current_user()
    if user:
        return jsonify({ "message": "This route is protected and accessible to authenticated users"})
    else:
        return jsonify({"message": "Authentication failed"}), 401





###############################     Route For Vendor Profile Complete       ######################################

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        user = get_current_user()
        return jsonify({"status": True, "user": user.as_vendor()})
    except Exception as e:
        print(e)  # Log the error for debugging
        return jsonify({"status": False, "error": str(e)})

@app.route('/complete_vendor_profile', methods=["POST"])
@jwt_required()
def complete_vendor_profile():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401

    if user.role != "vendor":
        return jsonify({"status":False,"message": "User Auth Error, not a vendor"}), 401

    full_name = data.get("full_name")
    phone_number = data.get("phone_number")
    location = data.get("location")
    biography = data.get("biography")

    if not all([full_name, phone_number, location, biography]):
        return jsonify({"status":False,"message": "All fields are required for the vendor profile"}), 400

    vendor = user.vendor

    # If vendor profile doesn't exist then create a new one
    if not vendor:
        vendor_data = {
            'full_name': full_name,
            'phone_number': phone_number,
            'location': location,
            'biography': biography
        }
        vendor = Vendor(**vendor_data)
        user.vendor = vendor
        db.session.commit()
        return jsonify({"status":True,"message": "Vendor profile created successfully"})
    
    # else update the existing
    else:
        vendor.full_name = full_name
        vendor.phone_number = phone_number
        vendor.location = location
        vendor.biography = biography
        db.session.commit()
        return jsonify({"status":True,"message": "Vendor profile completed successfully"})
    



VENDOR_IMAGES_FOLDER = 'images'
app.config["VENDOR_IMAGES_FOLDER"] = VENDOR_IMAGES_FOLDER


###############################     Route For Event Management      ######################################

###############################     Create Event       ######################################

# First vendor will be registered or complete his profile then can create event

@app.route("/create_event", methods=["POST"])
@jwt_required()
def create_event():    
    try: 
        data = request.get_json()
        user = get_current_user()
        # print(data)

        if not user:
            return jsonify({"status":False, "message": "User not found"}), 401

        if user.role != "vendor":
            return jsonify({"status":False,"message": "User Auth Error, not a vendor"}), 401

        # Ensure the user is associated with a vendor profile
        if not user.vendor:
            return jsonify({"status":False,"message": "User is not associated with a vendor profile"}), 400

        vendor = user.vendor

        # Fields for the event
        thumbnail = data.get("thumbnail")
        other_images = data.get("other_images")
        video_showcase = data.get("video_showcase")
        location_name = data.get("location_name")
        address = data.get("address")
        rate = data.get("rate")
        fixed_price = data.get("fixed_price")

        # Additional fields
        details = data.get("details")
        services = data.get("services")
        custom_event_name = data.get("custom_event_name")
        print(services)

        facilities = data.get("facilities")
        description = data.get("description")
        event_type = data.get("event_type")
        latitude=   data.get("latitude")
        longitude = data.get("longitude")
        timings_data = data.get("timings")
        extra_facility_data = data.get("extra_facility_data")
        guest_capacity = data.get("guest_capacity")

        # Create an event for the vendor
        event = Event(
            thumbnail=thumbnail,
            other_images=other_images,
            video_showcase=video_showcase,
            location_name=location_name,
            address=address,
            rate=rate,
            fixed_price=fixed_price,
            details=details,
            custom_event_name=custom_event_name,
            guest_capacity=guest_capacity,
            services =services,
            facilities = facilities,
            description=description,
            event_type=event_type,
            latitude=latitude,
            longitude=longitude,
            vendor=vendor  # Associate the event with the vendor
        )
        event.guest_capacity = data.get("Guest_capacity", event.guest_capacity)
        # Handle thumbnail image if provided
        if thumbnail:
            thumbnail_filename = f"{uuid.uuid4()}.png"
            thumbnail_path = os.path.join(app.config['VENDOR_IMAGES_FOLDER'], thumbnail_filename)
            save_image_from_base64(thumbnail, thumbnail_path)
            event.thumbnail = thumbnail_filename

        if other_images:
            other_image_filenames = save_multiple_images_from_base64(other_images)
            event.other_images = other_image_filenames

        if facilities:
            facility_image_filenames = save_multiple_images_from_base64(facilities)
            event.facilities = facility_image_filenames
        

        if extra_facility_data:
            for extra_facility_info in extra_facility_data: # iterate through each dict object 
                image_filenames = extra_facility_info.get("image", []) # get that image object in list

                # Handle image data for extra facility similar to other images
                if image_filenames:
                    image_paths = save_multiple_images_from_base64(image_filenames)
                    extra_facility_info["image"] = image_paths
                    print("image file tk theek hai")

                extra_facilities = ExtraFacility(
                    name=extra_facility_info.get("name"),
                    image=image_paths,  
                    rate=extra_facility_info.get("rate"),
                    unit=extra_facility_info.get("unit"),
                    event=event
                )

                db.session.add(extra_facilities)

            db.session.commit()


            print(f" Extra Facilities : DONE")


        db.session.add(event)  # Add the event to the session
        db.session.commit()  # Commit the transaction

        if timings_data:
            print(f"Timings Data : {timings_data}")
            for day, timings in timings_data.items():
                start_time = timings.get("start_time")
                end_time = timings.get("end_time")

                # Set a default day if it's not provided
                day_of_week = day or "DefaultDay"

                if start_time is None or end_time is None:
                    available = False
                else:
                    if start_time and end_time:
                        # Ensure start_time and end_time are in the correct format
                        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
                        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()
                        available = True
                    else:
                        available = False

                    # Check if the timings are valid before storing them
                    event_timing = eventtiming(
                        day_of_week=day_of_week,
                        start_time=start_time_obj if available else "00:00:00",
                        end_time=end_time_obj if available else "00:00:00",
                        available=available,
                        event=event
                    )
                    db.session.add(event_timing)

            db.session.commit()

        return jsonify({"status":True,"message": "Event created successfully"})
    
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500


###############################     Update Event     ######################################

@app.route("/get_my_events", methods=["GET"])
@jwt_required()
def getmyevents():
    try:
        user = get_current_user()
        print(user,"core fish")
        vendor = user.vendor
        events = Event.query.filter_by(vendor=vendor).all()
        print(vendor,"ll")
        events_data = []

        for event in events:
            event_dict = event.as_dict()
            event_dict["event_rating"]= Ratings.get_average_rating(event.id)
            event_dict['total_bookings'] = event.get_total_bookings()
            event_dict['total_bookings_value'] = event.earnings_per_month()  # Total earnings for the current month
            events_data.append(event_dict)

        return jsonify({"status": True, "events": events_data})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "events": []})



@app.route("/withdraw", methods = ["POST"])
@jwt_required()
def withdraw():
    try:
        user = get_current_user()
        data = request.get_json()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role == "vendor":
            vendor = Vendor.query.filter_by(id=user.vendor_id).first()

            if vendor and vendor.wallet >= 30:
                withdrawal_amount = data.get("withdrawal_amount")
                if withdrawal_amount > 30:
                    vendor.wallet -= withdrawal_amount
                    transaction = Transaction(user_id = user.id , user_type = "vendor", transaction_amount = withdrawal_amount)
                    db.session.add(transaction)
                    db.session.commit()

                    return jsonify({
                        "status":True,
                        "message": "Withdrawal success!!",
                        "new_wallet_balance":vendor.wallet
                    }), 200
            
                else:
                    return jsonify({
                    "status":False,
                    "message": "Amount should be greater than 30!!"
                }), 400

            else:
                return jsonify({
                    "status":False,
                    "message":"The amount should be greater than 30 for making any withdrawal"
                }), 404
        else:
            return jsonify({
                    "status":False,
                    "message":"Only vendors are allowed for making the withdrawal !!"
                }), 404    
        
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500


# @app.route("/update_event_extra_facility/<int:event_id>", methods=["PUT"])
# @jwt_required()
# def update_event_extra_facility(event_id):
#     try:
#         print("dfdfdfdfdfdf")
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status": False,
#                 "message": "User Not Found !!"
#             }), 401

#         if user.role != "vendor":
#             return jsonify({
#                 "status": False,
#                 "message": "User Authentication Error !!!"
#             })

#         # Ensuring that user is associated with a vendor profile
#         if not user.vendor:
#             return jsonify({
#                 "status": False,
#                 "message": "User is not associated with a vendor profile make sure to complete the vendor profile first !!! "
#             })

#         event = Event.query.filter_by(id=event_id, vendor=user.vendor).first()
#         print(event,"/////")


#         facilities_data = data.get("facilities_data", [])

#         for facility_data in facilities_data:
#             facility_id = facility_data.get("id")
#             facility_name = facility_data.get("name")
#             facility_unit = facility_data.get("unit")
#             facility_rate = facility_data.get("rate")
#             images = facility_data.get("image", [])

#             if facility_id != "":
#                 facility = ExtraFacility.query.filter_by(id=facility_id, event_id = event_id).first()

#                 if facility:
#                     facility.name = facility_name
#                     facility.unit = facility_unit
#                     facility.rate = float(facility_rate)

#                     if images:
#                             images_filenames = save_multiple_images_from_base64(images)
#                             facility.image = images_filenames
#                             print(images_filenames,"facilie dsdsdsdsd")

#                 else:
#                     print("ereror s here ")
#                     return jsonify({
#                             "status": False,
#                             "message": f"Facility with ID {facility_id} not found for event {event_id}"
#                         }), 404

#             else:
#                 new_facility = ExtraFacility(
#                         name=facility_name,
#                         unit=facility_unit,
#                         rate=facility_rate,
#                         event_id=event_id
#                     )
                    
#                 if images:
#                         images_filenames = save_multiple_images_from_base64(images)
#                         new_facility.image = images_filenames
#                         print(images_filenames,"///////")

#                 db.session.add(new_facility)
#                     # print(new_facil)


#             db.session.commit()

#         return jsonify({
#             "status": True,
#             "message": "Updated successfully !!"
#         })

#     except Exception as e:
#         print(str(e))
#         return jsonify({
#             "status": False,
#             "message": str(e)
#         }), 500


@app.route("/update_event_extra_facility/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event_extra_facility(event_id):
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User Not Found !!"
            }), 401

        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "User Authentication Error !!!"
            })

        # Ensuring that user is associated with a vendor profile
        if not user.vendor:
            return jsonify({
                "status": False,
                "message": "User is not associated with a vendor profile make sure to complete the vendor profile first !!! "
            })

        event = Event.query.filter_by(id=event_id, vendor=user.vendor).first()

        if not event:
            return jsonify({
                "status": False,
                "message": "Event not found or unauthorized user"
            }), 404

        facilities_data = data.get("facilities_data", [])

        for facility_data in facilities_data:
            facility_id = facility_data.get("facility_id")
            facility_name = facility_data.get("facility_name")
            facility_unit = facility_data.get("facility_unit")
            facility_rate = facility_data.get("facility_rate")
            images = facility_data.get("images", [])

            if facility_id is not None:
                facility = ExtraFacility.query.filter_by(id=facility_id, event_id = event_id).first()

                if facility:
                    facility.name = facility_name or facility.name
                    facility.unit = facility_unit or facility.unit
                    facility.rate = facility_rate or facility.rate

                    uuid_format = all(image.endswith(".png") and "-" in image for image in images)
                    
                    if not uuid_format :
    
                        images_filenames = save_multiple_images_from_base64(images)
                        facility.image = images_filenames

                else:
                    return jsonify({
                            "status": False,
                            "message": f"Facility with ID {facility_id} not found for event {event_id}"
                        }), 404

            else:
                new_facility = ExtraFacility(
                        name=facility_name,
                        unit=facility_unit,
                        rate=facility_rate,
                        event_id=event_id
                    )
                uuid_format = all(image.endswith(".png") and "-" in image for image in images )
                if not uuid_format:
                        images_filenames = save_multiple_images_from_base64(images)
                        new_facility.image = images_filenames

                db.session.add(new_facility)
                    # print(new_facil)


            db.session.commit()

        return jsonify({
            "status": True,
            "message": "Updated successfully !!"
        })

        

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500







##############################     Submit Review      ####################################


@app.route("/submit_review", methods=["POST"])
@jwt_required()
def submit_review():
    data = request.get_json()
    user = get_current_user()

    if user.role != "user":
        return jsonify({
            "status": False,
            "message": "Unauthorized access: Only users can create bookings."
        })

    booking_id = data.get("booking_id")
    cleanliness_rating = data.get("cleanliness_rating")
    price_value_rating = data.get("price_value_rating")
    service_value_rating = data.get("service_value_rating")
    location_rating = data.get("location_rating")
    user_review = data.get("user_review")

    reviews_sum = cleanliness_rating + price_value_rating + service_value_rating + location_rating
    average_of_reviews = round((reviews_sum / 4), 1)

    # Check if the booking exists or not
    booking = Booking.query.filter_by(id=booking_id).first()

    if not booking:
        return jsonify({     "status": False,"message": "Booking Does Not Exist!"}), 400

    # Check if the booking belongs to the authenticated user
    if booking.user_id != user.id:
        return jsonify({"status": False,"message": "Unauthorized: You can only review your own bookings!"}), 403

    booking_end_time = datetime.combine(booking.end_date, booking.end_time)

    if datetime.utcnow() >= booking_end_time:
        user_email = get_jwt_identity()  # Assuming get_jwt_identity() returns email
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({"status": False,"message": "User not found!"}), 400

        existing_review = Review.query.filter_by(booking_id=booking_id, user_id=user.id).first()

        if existing_review:
            return jsonify({"status": False,"message": "You have already reviewed this event!"}), 400

        new_review = Review(
            booking_id=booking_id,
            event_id=booking.event_id,
            user_id=user.id,  # Use user.id as the user_id
            cleanliness_rating=cleanliness_rating,
            price_value_rating=price_value_rating,
            service_value_rating=service_value_rating,
            location_rating=location_rating,
            user_review=user_review,
            average_rating=average_of_reviews
        )

        try:
            db.session.add(new_review)
            db.session.commit()

            return jsonify({
                     "status": True,"message": "Successfully reviewed !!"
            }), 200

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                    "status": False, "message": f"You have already reviewed this event !! {str(e)}"
            }), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({
                    "status": False, "message": f"Failed to rate {str(e)}"
            }), 500

    else:
        return jsonify({     "status": False,"message": "Booking has not been completed yet. Can't rate the event now."}), 400
##############################     Pending Review      ####################################

@app.route("/pending_reviews", methods=["GET"])
@jwt_required()
def pending_reviews():
    try:
        # Extract the user's email from the JWT token
        email = get_jwt_identity()
        
        # Find the user's ID using the email retrieved from the JWT token
        user = User.query.filter_by(email=email).first()
        
        # Get the user ID
        user_id = user.id

        # Fetch all bookings made by the user
        user_bookings = Booking.query.filter_by(user_id=user_id).all()

        # Fetch all reviews made by the user
        user_reviews = Review.query.filter_by(user_id=user_id).all()

        # Initialize a set to hold reviewed event and booking IDs
        reviewed_events_bookings = {(review.event_id, review.booking_id) for review in user_reviews}

        # Collect pending reviews by comparing bookings and reviewed events
        pending_reviews_info = []
        for booking in user_bookings:
            is_reviewed = False
            for review in user_reviews:
                if review.event_id == booking.event_id and review.booking_id == booking.id:
                    is_reviewed = True
                    break

            if not is_reviewed:
                event = Event.query.get(booking.event_id)
                if event:
                    event_rate = event.rate
                    event_type = event.event_type
                    event_address = event.address
                    event_thumbnail = event.thumbnail
                    custom_event_name = event.custom_event_name if event.custom_event_name else "Unknown Custom Event Name"

                    pending_reviews_info.append({
                        "booking_id":booking.id,
                        "location_name":booking.event.location_name,
                        "event_id": event.id,
                        "event_rate": event_rate,
                        "event_type": event_type,
                        "event_address": event_address,
                        "event_thumbnail": event_thumbnail,
                        "custom_event_name": custom_event_name,
                        "booking_date": booking.start_date.isoformat(),
                        "booking_time": booking.start_time.isoformat()
                    })

        return jsonify({
            "Pending Reviews": pending_reviews_info,
            "Pending Reviews Length": len(pending_reviews_info)
        })

    except Exception as e:
        print(f"Error fetching pending reviews: {str(e)}")
        return jsonify({"error": "An error occurred while fetching pending reviews."}), 500

##############################     All Rated Reviews      ####################################

@app.route('/all_reviews', methods=["GET"])
@jwt_required()
def all_reviews():
    try:
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if user.role == "user":
            # Fetch all reviews given by the user
            reviews = (
                db.session.query(Review, Event, Vendor)
                .join(Event, Review.event_id == Event.id)
                .join(Vendor, Event.vendor_id == Vendor.id)
                .filter(Review.user_id == user.id)
                .all()
            )
        elif user.role == "vendor":
            reviews = (
                db.session.query(Review, Event, Vendor)
                .join(Event, Review.event_id == Event.id)
                .join(Vendor, Event.vendor_id == Vendor.id)
                .filter(Event.vendor_id == user.vendor_id)
                .all()
            )
        else:
            return jsonify({"message": "Invalid user role."}), 400

        if not reviews:
            return jsonify({
                "rated_reviews": [],
                "total_rated_reviews": 0,
                "status":True
            }), 200
        
        review_data = []

        for review, event, vendor in reviews:
            vendor_user = User.query.filter_by(vendor_id=vendor.id).first()
            vendor_profile_image = getattr(vendor_user, 'profile_image', None)
            review_user = User.query.get(review.user_id)
            user_profile_image = getattr(review_user ,"profile_image", None)
            print(review_user)

            # Fetch all bookings for this event
            bookings = Booking.query.filter_by(event_id=event.id).all()

            # Calculate total amount earned for the event
            total_amount = 0
            for booking in bookings:
                # Calculate event hours for each booking
                event_hours = DateTimeConversions.calculate_event_hours(
                    booking.start_date, booking.end_date,
                    booking.start_time, booking.end_time,
                    booking.all_day
                )

                subtotal = event.rate * event_hours
                print(f"Subtotal : {subtotal}")
                tax_percentage = 0.15
                tax_amount = subtotal * tax_percentage
                print(f"tax amount : {tax_amount}")
                total_price = subtotal + tax_amount
                total_amount += total_price
                print(f"Total amount : {total_amount}")

                print(total_amount)

            review_data.append({
                "event_id": event.id,
                "event_thumbnail": event.thumbnail,
                "event_name": event.location_name,
                "event_type":event.event_type,
                "event_rate": event.rate,
                "total_event_hours": event_hours,
                "total_amount_earned_by_the_vendor": total_amount,
                "tax_amount": tax_amount, 
                "event_address": event.address,
                "user_profile_image":user_profile_image,
                "vendor_profile_image": vendor_profile_image,
                "user_review": review.user_review,
                "cleanliness_rating": review.cleanliness_rating,
                "price_value_rating": review.price_value_rating,
                "service_value_rating": review.service_value_rating,
                "location_rating": review.location_rating
            })
        print(review_data)
        return jsonify({
            "rated_reviews": review_data,
            "total_rated_reviews": len(review_data),
            "status":True
        })
    
    except Exception as e:
        print(f"Error in fetching rated reviews: {str(e)}")
        return jsonify({"error": "An error occurred while fetching rated reviews."}), 500


# new
# for vendor
# get all_inquiries for vendor irrespective of the event_id or inq.id
@app.route("/get_all_my_inquiries_vendor", methods = ["GET"])
@jwt_required()
def get_all_my_inquiries():
    try:
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendors can create inquiries."
            }), 401
        
        vendor_id = user.vendor.id

        inquiries = Inquiry.query.join(Event).filter(Event.vendor_id == vendor_id).all()

        if not inquiries:
            return jsonify({
                "status":False,
                "message":"Inquiries not found !!"
            }), 404

        inquiries_data = [inquiry.as_dict() for inquiry in inquiries]

        return jsonify({
            "status":False,
            "inquiries_data":inquiries_data
        }), 200

    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500

# for user
@app.route("/get_all_my_inquiries_user", methods = ["GET"])
@jwt_required()
def get_all_my_inquiries_user():
    try:
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendors can create inquiries."
            }), 401

        user_id = user.id

        inquiry = Inquiry.query.filter_by(user_id = user_id).all()
    
        if not inquiry:
            return jsonify({
                "status":False,
                "message":"Inquiry doesn't exist !!"
            }), 404

        inquiries_data = [inquiries.as_dict() for inquiries in inquiry]
        
        
        return jsonify({
            "status":True,
            "inquiries_data":inquiries_data
        }), 200

    
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500



# for vendor getting specifc inquiries for events
    
@app.route("/get_my_inquiry_vendor/<int:event_id>", methods = ["GET"])
@jwt_required()
def get_my_inquiry_vendor(event_id):
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendors can create inquiries."
            }), 401

        # inquiry_id = data.get("inquiry_id")
        vendor_id = user.vendor.id


        inquiries = Inquiry.query.join(Event).filter(Event.vendor_id == vendor_id, Event.id == event_id).all()
    
        if not inquiries:
            return jsonify({
                "status":False,
                "message":"Inquiry doesn't exist !!"
            }), 404

        inquiries_data = [inquiry.as_dict() for inquiry in inquiries]
        
        
        return jsonify({
            "status":True,
            "inquiries_data":inquiries_data
        }), 200

    
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500

@app.route('/all_reviewssss', methods=["GET"])
@jwt_required()
def all_reviewsss():
    try:
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if user.role == "user":
            # Fetch all reviews given by the user
            reviews = (
                db.session.query(Review, Event, Vendor)
                .join(Event, Review.event_id == Event.id)
                .join(Vendor, Event.vendor_id == Vendor.id)
                .filter(Review.user_id == user.id)
                .all()
            )
        elif user.role == "vendor":
            reviews = (
                db.session.query(Review, Event, Vendor)
                .join(Event, Review.event_id == Event.id)
                .join(Vendor, Event.vendor_id == Vendor.id)
                .filter(Event.vendor_id == user.vendor_id)
                .all()
            )
        else:
            return jsonify({"status":False, "message": "Invalid user role."}), 400

        if not reviews:
            return jsonify({"status":False,"message": "Reviews Not Found !!"}), 400

        review_data = []

        for review, event, vendor in reviews:
            vendor_user = User.query.filter_by(vendor_id=vendor.id).first()
            vendor_profile_image = getattr(vendor_user, 'profile_image', None)

            review_data.append({
                "event_id": event.id,
                "event_thumbnail": event.thumbnail,
                "event_name": event.location_name,
                "event_rate": event.rate,
                "event_address": event.address,
                "vendor_profile_image": vendor_profile_image,
                "user_review": review.user_review,
                "cleanliness_rating": review.cleanliness_rating,
                "price_value_rating": review.price_value_rating,
                "service_value_rating": review.service_value_rating,
                "location_rating": review.location_rating
            })

        return jsonify({
            "status":True,
            "rated_reviews": review_data,
            "total_rated_reviews": len(review_data)
        })

    except Exception as e:
        print(f"Error in fetching rated reviews: {str(e)}")
        return jsonify({"status":False, "message": "An error occurred while fetching rated reviews."}), 500



###############################     Delete Event     ######################################

@app.route("/get_reviews", methods=["GET"])
def get_review():
    return jsonify({"status":True,"reviews":[]})

# @app.route("/delete_event/<int:event_id>", methods = ["DELETE"])
# @jwt_required()
# def delete_event(event_id):
#     user = get_current_user()
    
#     if not user:
#         return jsonify({
#             "status":False,
#             "message":"User Not Found !!"
#         })

#     if user.role != "vendor":
#         return jsonify({
#             "status":False,
#             "message":"User Auth Error, Not a vendor !!"
#         })

#     try:
#         # Basically used this here so that we should know that the user is associated with a vendor profile or not
#         # Here we are actually retrieving the vendor profile associated with a user
#         vendor = user.vendor
#         event = Event.query.filter_by(id = event_id , vendor=vendor).first()
#         if not event:
#           return jsonify({
#                 "status":False,
#                 "message":"User Not Found !!"
#           })

#         db.session.delete(event)
#         db.session.commit()
#         return jsonify({
#             "status":True,
#             "message":"Event Deleted Successfully !!!"
#         })
#     except Exception as e:
#         print(e)
#         return jsonify({
#            "status":False,
#            "message":"booking"
#         })


@app.route("/delete_event/<int:event_id>", methods = ["DELETE"])
@jwt_required()
def delete_event(event_id):
    user = get_current_user()
    
    if not user:
        return jsonify({
            "status":False,
            "message":"User Not Found !!"
        }), 401

    if user.role != "vendor":
        return jsonify({
            "status":False,
            "message":"User Auth Error, Not a vendor !!"
        })

    try:
        # Basically used this here so that we should know that the user is associated with a vendor profile or not
        # Here we are actually retrieving the vendor profile associated with a user
        vendor = user.vendor
        event = Event.query.filter_by(id = event_id , vendor=vendor).first()
        if not event:
            return jsonify({
            "status":False,
            "message":"User Not Found !!"
        })

        if event.extra_facilities:
            return jsonify({
                "status":False,
                "message":"Event has associated records, so can't delete it."
            })


        db.session.delete(event)
        db.session.commit()
        return jsonify({
        "status":True,
        "message":"Event Deleted Successfully !!!"
        })

    except IntegrityError as e:
        db.session.rollback()  # Rollback transaction to avoid leaving the database in an inconsistent state
        return jsonify({"status": False, "message": "IntegrityError: Deleting associated records failed."}), 500

    
    except Exception as e:
        print(e)
        return jsonify({
        "status":False,
        "message":"booking",
        "error":str(e)
        })



###############################   Booking History For User      ######################################

@app.route("/booking_history", methods = ["POST"])
@jwt_required()
def booking_history():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            })
            
        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can check booking history."
            })

        booking_type = data.get("booking_type")
        current_datetime = datetime.now()


        if booking_type.lower() == "done":
            bookings = Booking.query.filter(
                (Booking.user_id == user.id) &
                ((Booking.end_date < current_datetime.date()) |
                ((Booking.end_date == current_datetime.date()) &
                (Booking.end_time < current_datetime.time())))
                ).all()
                    
        elif booking_type.lower() == "upcoming":
            bookings =  Booking.query.filter(
                (Booking.user_id ==  user.id) &
                ((Booking.start_date > current_datetime.date()) |
                ((Booking.start_date == current_datetime.date) & 
                (Booking.start_time > current_datetime.time())))
            ).all()


        elif booking_type.lower() == "cancelled":
            bookings = Booking.query.filter(
                (Booking.user_id == user.id) &
                (Booking.cancelled == True)
            ).all()
        

        user_bookings = []
        for booking in bookings:
            vendor_image = None
            print(booking.id)
            if booking.event.vendor:
                if isinstance(booking.event.vendor, Vendor):
                    vendor = booking.event.vendor
                    vendor_image = vendor.user.profile_image if hasattr(vendor.user, 'profile_image') else None
                    print(vendor_image)
                    # You can handle other vendor details here similarly
            else:
                # If it's a list (unexpected), iterate through it
                for vendor in booking.event.vendor:
                    vendor_image = vendor.user.profile_image if hasattr(vendor.user, 'profile_image') else None
                    print(vendor_image)
    

            user_booking = {
                "booking_id":booking.id,
                "event_id":booking.event_id,
                "event_vendor_id":booking.event.vendor_id,
                "location_name": booking.event.location_name,
                "event_address":booking.event.address,
                "event_rate":booking.event.rate,
                "booking_end_date": str(booking.end_date),
                "booking_start_time": str(booking.start_time),
                "booking_end_time":str(booking.end_time),
                "vendor_image": vendor_image
            }

            user_bookings.append(user_booking)

        return jsonify({
            "status":True,
            "booking_details":user_bookings,
            "Total Bookings":len(user_bookings)
        })

    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500
###############################     Get Event     ######################################

@app.route("/booking_details/<int:booking_id>", methods=["GET"])
@jwt_required()
def booking_details(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({"status": False, "error": "Booking not found"})

        booking_data = booking.get_booking_with_event_details()
        return jsonify({"status": True, "booking_details": booking_data})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "error": str(e)})


@app.route("/get_event/<int:event_id>", methods = ["GET"])
@jwt_required()
def get_event(event_id):
    user = get_current_user()
    event = Event.query.get(event_id) 
    
    if event:
        fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]
        is_favorite = event.id in fav_event_ids
        event_details = {
            "id": event.id,
            "thumbnail": event.thumbnail,
            "other_images": event.other_images,
            "video_showcase": event.video_showcase,
            "location_name": event.location_name,
            "address": event.address,
            "rate": event.rate,
            "fixed_price": event.fixed_price,
            "details": event.details,
            "services": event.services,
            "facilities": event.facilities,
            "description": event.description,
            "event_type": event.event_type,
            "vendor_id": event.vendor_id,  # You can include vendor details if needed
            "custom event name":event.custom_event_name,
            "longitude":event.longitude,
            "latitude":event.latitude,
            "guest_capacity":event.guest_capacity,
            "favorite":is_favorite
        }
        # Fetch vendor details
        event_timings = event.event_timing
        print(event_timings)
        if event_timings:
            event_details["event_timings"] = {
                timing.day_of_week : {
                    "start_time":timing.start_time.isoformat(),
                    "end_time":timing.end_time.isoformat()
                }
            for timing in event_timings}
        else:
            event_details["event_timings"] = {}

        if event.vendor:
            vendor = event.vendor
            vendor_details = {
                "id": vendor.id,
                "full_name": vendor.full_name,
                "phone_number": vendor.phone_number,
                "location": vendor.location,
                "biography": vendor.biography,
                "email":vendor.user[0].email,
                  "profile_image": vendor.user[0].profile_image
            }

            event_details['vendor_details'] = vendor_details
        extra_facility_list = [{
                "id":extra_fac.id,
                "name":extra_fac.name,
                "image":extra_fac.image,
                "rate":extra_fac.rate,
                "unit":extra_fac.unit,
            } for extra_fac in event.extra_facilities] # extra facility as bidirectional relationship is defined in the model class for Event

        event_details['extra_facility_list'] = extra_facility_list
        return jsonify({"status":True,"Event Details":event_details})

    else:
        return jsonify({
            "status":False,
            "message":"Event not Found !!"
        })






# decoding image


def save_image_from_base64(base64_data, filename):
    with open(filename, "wb") as image_file:
        image_file.write(base64.b64decode(base64_data))
    return filename

def save_multiple_images_from_base64(base64_images):
    # other_images is an array of base64-encoded images, allowing users to upload multiple images.
    image_paths = []
    for image_base64 in base64_images:
        print(image_base64,"////sdsdsdsd")
        if image_base64.endswith("png") or image_base64.endswith("jpg"):
            image_paths.append(image_base64)
            print("BAH")
        else:
            image_filename = f"{uuid.uuid4()}.png"
            image_path = os.path.join(app.config['VENDOR_IMAGES_FOLDER'], image_filename)
            save_image_from_base64(image_base64, image_path)
            image_paths.append(image_filename)
    return image_paths


def refresh_token_is_valid(refresh_token, current_user):
    try:
        decoded_token = decode_token(refresh_token)
        return decoded_token.get("identity") == current_user
    except Exception as e:
        return False
    
@app.route('/refresh_token', methods=['POST'])
@jwt_required()
def refresh_token():
    refresh_token = request.form.get('refresh_token')
    current_user = get_jwt_identity()
    
    if refresh_token_is_valid(refresh_token, current_user):
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token)
    else:
        return jsonify({"status":False,'message': 'Invalid refresh token'}), 401





# # # corrected home_events
# @app.route("/home_events", methods=["POST"])
# @jwt_required()
# def home_events():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status": False,
#                 "message": "User not authenticated !!"
#             }), 401

#         requested_availability = data.get("is_available")
#         user_location = (data.get("latitude"), data.get("longitude"))  # Retrieve user's location from request data
#         max_distance = 300000

#         event_types = Event.query.with_entities(Event.event_type).distinct().all()

#         events_by_types = {}
#         for event_type in event_types:
#             events = (
#                 Event.query.join(Event.vendor)
#                     .join(Vendor.user)
#                     # .filter(Event.event_type == event_type[0])
#                     .order_by(func.random())
#                     .limit(15)
#                     .all()
#             )

#             events_data = []
#             for event in events:
#                 current_date_time = datetime.now()

#                 if requested_availability:
#                                         # Check event availability considering booking and cancellation
#                     is_event_available = any(
#                         BookingAvailability.check_availability(booking, current_date_time)
#                         for booking in event.bookings
#                         if not booking.all_day and not booking.cancelled
#                         or (booking.start_date <= current_date_time.date() <= booking.end_date)
#                     )


#                     if not is_event_available:
#                         continue

#                 # Check the condition from Booking table before adding to the response
#                 if any(booking.all_day for booking in event.bookings):
#                     continue  # Skip this event if the condition is met

#                 # Calculate total bookings
#                 total_bookings = sum(1 for booking in event.bookings)

#                 serialized_event = {
#                     "event_id": event.id,
#                     "vendor_id": event.vendor_id,
#                     "event_type": event.event_type,
#                     "event_rate": event.rate,
#                     "event_address": event.address,
#                     "event_latitude": event.latitude,
#                     "event_longitude": event.longitude,
#                     "event_ratings": Ratings.get_average_rating(event.id),
#                     "total_bookings": total_bookings  # Include total bookings in the response
#                     # Add other necessary event details
#                 }
#                 events_data.append(serialized_event)

#             prefered_filter = data.get("prefered_filter")
#             if prefered_filter:
#                 events_data = Filterations.apply_filters(events_data, prefered_filter, user_location, max_distance)
#             else:
#                 continue
            
#             events_by_types[event_type[0]] = events_data

#         return jsonify({
#             "status": True,
#             "events_by_events_types": events_by_types
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": False,
#             "message": str(e)
#         }), 500


# # working
# @app.route("/home_events", methods=["POST"])
# @jwt_required()
# def home_events():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status": False,
#                 "message": "User not authenticated !!"
#             }), 401

#         requested_availability = data.get("is_available")
#         user_location = (data.get("latitude"), data.get("longitude"))  # Retrieve user's location from request data
#         max_distance = 300000

#         events = []
#         event_types = Event.query.with_entities(Event.event_type).distinct().all()

#         for event_type in event_types:
#             events.extend(
#                 Event.query.join(Event.vendor)
#                     .join(Vendor.user)
#                     .order_by(func.random())
#                     .limit(15)
#                     .all()
#             )

#         serialized_events = []
#         for event in events:
#             current_date_time = datetime.now()

#             if requested_availability:
#                 is_event_available = any(
#                     BookingAvailability.check_availability(booking, current_date_time)
#                     for booking in event.bookings
#                     if not booking.all_day and not booking.cancelled
#                     or (booking.start_date <= current_date_time.date() <= booking.end_date)
#                 )

#                 if not is_event_available:
#                     continue

#             if any(booking.all_day for booking in event.bookings):
#                 continue

#             total_bookings = sum(1 for booking in event.bookings)

#             serialized_event = {
#                 "event_id": event.id,
#                 "vendor_id": event.vendor_id,
#                 "event_type": event.event_type,
#                 "event_rate": event.rate,
#                 "event_address": event.address,
#                 "event_latitude": event.latitude,
#                 "event_longitude": event.longitude,
#                 "event_ratings": Ratings.get_average_rating(event.id),
#                 "total_bookings": total_bookings,
#                 "location_name": event.location_name,  # assuming you have a location_name attribute
#                 "fixed_price": event.fixed_price,  # assuming you have a fixed_price attribute
#                 "thumbnail": event.thumbnail,  # assuming you have a thumbnail attribute
#                 "vendor_details": {
#                     "vendor_id": event.vendor.id,
#                     "vendor_profile_image": event.vendor.user[0].profile_image,
#                 }
#             }
#             serialized_events.append(serialized_event)

#         prefered_filter = data.get("prefered_filter")
#         if prefered_filter:
#             serialized_events = Filterations.apply_filters(serialized_events, prefered_filter, user_location, max_distance)

#         return jsonify({
#             "status": True,
#             "Events": serialized_events,
#             "Total_Events": len(serialized_events)
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": False,
#             "message": str(e)
#         }), 500



# @app.route("/home_events", methods=["POST"])
# @jwt_required()
# def home_events():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status": False,
#                 "message": "User not authenticated !!"
#             }), 401

#         requested_availability = data.get("is_available")
#         user_location = (data.get("latitude"), data.get("longitude"))  # Retrieve user's location from request data
#         max_distance = 300000

#         events = Event.query.join(Event.vendor).join(Vendor.user).order_by(func.random()).limit(15).all()

#         serialized_events = []
#         for event in events:
#             current_date_time = datetime.now()

#             if requested_availability:
#                 is_event_available = any(
#                     BookingAvailability.check_availability(booking, current_date_time)
#                     for booking in event.bookings
#                     if not booking.all_day and not booking.cancelled
#                     or (booking.start_date <= current_date_time.date() <= booking.end_date)
#                 )

#                 if not is_event_available:
#                     continue

#             if any(booking.all_day for booking in event.bookings):
#                 continue

#             total_bookings = sum(1 for booking in event.bookings)

#             serialized_event = {
#                 "event_id": event.id,
#                 "vendor_id": event.vendor_id,
#                 "event_type": event.event_type,
#                 "event_rate": event.rate,
#                 "event_address": event.address,
#                 "event_latitude": event.latitude,
#                 "event_longitude": event.longitude,
#                 "event_ratings": Ratings.get_average_rating(event.id),
#                 "total_bookings": total_bookings,
#                 "location_name": event.location_name,  # assuming you have a location_name attribute
#                 "fixed_price": event.fixed_price,  # assuming you have a fixed_price attribute
#                 "thumbnail": event.thumbnail,  # assuming you have a thumbnail attribute
#                 "vendor_details": {
#                     "vendor_id": event.vendor.id,
#                     "vendor_profile_image": event.vendor.user[0].profile_image,
#                 }
#             }
#             serialized_events.append(serialized_event)
        

#         prefered_filter = data.get("prefered_filter")
#         if prefered_filter:
#             serialized_events = Filterations.apply_filters(serialized_events, prefered_filter, user_location, max_distance)

#         unique_events = []
#         seen_event_ids = set()
#         for event in serialized_events:
#             event_id = event["event_id"]
#             if event_id not in seen_event_ids:
#                 unique_events.append(event)
#                 seen_event_ids.add(event_id)

#         # Remove duplicate events if any
#         serialized_events = [dict(t) for t in {tuple(d.items()) for d in serialized_events}]

#         return jsonify({
#             "status": True,
#             "Events": unique_events,
#             "Total_Events": len(unique_events)
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": False,
#             "message": str(e)
#         }), 500

# newlylllllllllll
@app.route("/home_events", methods=["POST"])
@jwt_required()
def home_events():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User not authenticated !!"
            }), 401

        requested_availability = data.get("is_available")
        user_location = (data.get("latitude"), data.get("longitude"))  # Retrieve user's location from request data
        max_distance = 300000

        events = Event.query.join(Event.vendor).join(Vendor.user).order_by(func.random()).limit(15).all()

        serialized_events = []
        for event in events:
            current_date_time = datetime.now()

            if requested_availability:
                is_event_available = any(
                    BookingAvailability.check_availability(booking, current_date_time)
                    for booking in event.bookings
                    if not booking.all_day and not booking.cancelled
                    or (booking.start_date <= current_date_time.date() <= booking.end_date)
                )

                if not is_event_available:
                    continue

            if any(booking.all_day for booking in event.bookings):
                continue

            total_bookings = sum(1 for booking in event.bookings)

            serialized_event = {
                "event_id": event.id,
                "vendor_id": event.vendor_id,
                "event_type": event.event_type,
                "event_rate": event.rate,
                "event_address": event.address,
                "event_latitude": event.latitude,
                "event_longitude": event.longitude,
                "event_ratings": Ratings.get_average_rating(event.id),
                "total_bookings": total_bookings,
                "location_name": event.location_name,  # assuming you have a location_name attribute
                "fixed_price": event.fixed_price,  # assuming you have a fixed_price attribute
                "thumbnail": event.thumbnail,  # assuming you have a thumbnail attribute
                # "favorite":is_favorite,
                "vendor_details": {
                    "vendor_id": event.vendor.id,
                    "vendor_profile_image": event.vendor.user[0].profile_image,
                }
            }
            serialized_events.append(serialized_event)

            fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]
            is_favorite = event.id in fav_event_ids
            serialized_event["favorite"] = is_favorite

        prefered_filter = data.get("prefered_filter")
        if prefered_filter:
            serialized_events = Filterations.apply_filters(serialized_events, prefered_filter, user_location, max_distance)
        
        unique_events = []
        already_had_event_ids = set()
        for event in serialized_events:
            event_id = event["event_id"]
            if event_id not in already_had_event_ids:
                unique_events.append(event)
                already_had_event_ids.add(event_id)

        return jsonify({
            "status": True,
            "Events": unique_events,
            "Total_Events": len(unique_events)
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500


###############################     Search Events API        ######################################

@app.route("/top_venues/<int:vendor_id>", methods=["GET"])
def top_venues(vendor_id):
    try:
        # Get the total number of bookings for the vendor
        total_bookings = (db.session.query(func.count(Booking.id))
                          .join(Event)
                          .filter(Event.vendor_id == vendor_id)
                          .scalar())

        # Get booking count per venue (using location_name as the venue identifier)
        # venue_bookings = (db.session.query(Event.location_name, func.count(Booking.id).label('booking_count'))
        #                   .join(Event)
        #                   .filter(Event.vendor_id == vendor_id)
        #                   .group_by(Event.location_name)
        #                   .order_by(func.count(Booking.id).desc())
        #                   .all())
        venue_bookings = (db.session.query(Event.location_name, Event.thumbnail, func.count(Booking.id).label('booking_count'))
                          .join(Event)
                          .filter(Event.vendor_id == vendor_id)
                          .group_by(Event.location_name, Event.thumbnail)
                          .order_by(func.count(Booking.id).desc())
                          .all())

        # Calculate the percentage for each venue
        venues_list = []
        # for venue, count in venue_bookings:
        #     percentage = (count / total_bookings) * 100 if total_bookings > 0 else 0
        #     venues_list.append({"venue": venue, "bookings": count, "percentage": round(percentage, 2)})
        for location_name, thumbnail, count in venue_bookings:
            percentage = (count / total_bookings) * 100 if total_bookings > 0 else 0
            venues_list.append({
                "venue": location_name,
                "thumbnail": thumbnail,
                "bookings": count,
                "percentage": round(percentage, 2)
            })


        return jsonify({"status": True, "top_venues": venues_list})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "error": str(e)})


@app.route("/bookings_today", methods=["GET"])
@jwt_required()
def bookings_today():
    try:
        user = get_current_user()
        vendor = user.vendor
        print(vendor.id)
        today = datetime.now().date()
        bookings = Booking.query.join(Event, Booking.event_id == Event.id)\
                                .filter(Event.vendor_id == vendor.id)\
                                .filter(Booking.start_date <= today, Booking.end_date >= today)\
                                .all()

        bookings_data = [booking.booking_today() for booking in bookings]

        print(bookings_data,bookings,"ssssa")

        return jsonify({"status": True, "bookings": bookings_data})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "error": str(e)})


@app.route("/search_event", methods=["POST"])
@jwt_required()
def search_event():
    user = get_current_user()
    page_number = request.args.get('page', default=1, type=int)
    data = request.get_json()
    event_type = data.get("event_type")
    location_name = data.get("location_name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    distance_limit = data.get("distance_km", 3)  # Default to 10km if distance_km is not provided

    # Query based on event_type
    events_query = Event.query

    if event_type and event_type.lower() != "all":
        events_query = events_query.filter_by(event_type=event_type)

    # Apply location_name filter only if it's provided
    if location_name:
        events_query = events_query.filter(or_(Event.location_name.ilike(f"%{location_name}%")))

    all_events = events_query.all()


    user_location = (latitude, longitude)
    results_within_range = []

    for event in all_events:
        if event.latitude is not None and event.longitude is not None:
            event_location = (event.latitude, event.longitude)
            distance = geodesic(event_location, user_location).kilometers
            # Ensure distance is less than or equal to the specified or default distance limit
            if distance <= distance_limit:
                results_within_range.append((event, distance))

    # Sort events within range by event rating
    sorted_within_range = sorted(results_within_range, key=lambda x: Ratings.get_average_rating(x[0].id), reverse=True)

    total_events_found = len(sorted_within_range)
    events_per_page = 5
    offset = (page_number - 1) * events_per_page
    end_index = min(offset + events_per_page, len(sorted_within_range))

    paginated_results = sorted_within_range[offset:end_index]

    fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]


    event_list = []

    for result in paginated_results:
        event = result[0]
        within_radius = result[1]

        is_favorite = event.id in fav_event_ids

        vendor_details = {
            "vendor_profile_image": event.vendor.user[0].profile_image,
            "vendor_id": event.vendor.id
        }


        event_info = {
            "id": event.id,
            "thumbnail": event.thumbnail,
            "event_type": event.event_type,
            "rate": event.rate,
            "event_rating": Ratings.get_average_rating(event.id),
            "fixed_price": event.fixed_price,
            "distance_km": geodesic((event.latitude, event.longitude), user_location).kilometers,
            "address": event.vendor.location,
            "location_name": event.location_name,
            "vendor_details": vendor_details,
            "favorite":is_favorite
        }
        event_list.append(event_info)

    return jsonify({
        "status": True,
        "Total_Events": total_events_found,
        "Events": event_list
    }), 200






@app.route('/search_eventtt', methods=["POST"])
@jwt_required()
def search_evettttt():
    data = request.get_json()
    event_type = data.get("event_type")
    location_name = data.get("location_name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Pagination setup
    events_per_page = 5
    page = int(request.args.get("page", 1))
    offset = (page - 1) * events_per_page

    if event_type.lower() != "all":
        # Query based on event_type and location_name
        events = Event.query.filter_by(event_type=event_type).offset(offset).limit(events_per_page).all()

        if not events:
            return jsonify({
                "status": False,
                "message": "Events Not Found !!"
            })
    else:
        # Get all events if event_type is "all"
        all_events = Event.query.all()
        user_location = (latitude, longitude)

        # Calculate distances for events with latitude and longitude
        results_with_distance = [
            (event, geodesic((event.latitude, event.longitude), user_location).kilometers)
            for event in all_events 
            if event.latitude is not None and event.longitude is not None
        ]

        # Sort events based on distance in ascending order
        sorted_results = sorted(results_with_distance, key=lambda x: x[1])

        total_events_found = len(sorted_results)

        # Paginate the sorted results
        paginated_results = sorted_results[offset: offset + events_per_page]

        event_list =[]
        for event, _ in paginated_results:
            vendor = event.vendor
        
            vendor_details=vendor.user[0].profile_image
            #vendor.user[0].profile_image
                # Ensure that vendor_details is a dictionary
            #vendor_details = vendor_details.__dict__ if hasattr(vendor_details, '__dict__') else str(vendor_details)

            print(vendor_details)
            event_info = {
                "id": event.id,
                "thumbnail": event.thumbnail,
                "event_type": event.event_type,
                "custom_event_name": event.custom_event_name,
                "rate": event.rate,
                "fixed_price": event.fixed_price,
                "address":event.address,
                "location":event.location_name,
                "vendor_details":  vendor_details  # Ensure vendor_details is a dictionary
            }
            event_list.append(event_info)
            if not isinstance(vendor_details, dict):
            # Handle the case where vendor_details is not a dictionary
            # You can log a warning, raise an exception, or handle it as needed
                print("Warning: vendor_details is not a dictionary!")
        print(event_list,"ssdsdsdsdssds")
        return jsonify({
            "status": True,
            "Total_Events": total_events_found,
            "Events":event_list
        }), 200

    # If event_type is not "all", proceed with filtered events
    total_events_found = len(events)

    event_list = []
    for event in events:
        vendor_details = [
            {"vendor_profile_image": vendor_user.profile_image}
            for vendor_user in event.vendor.user
        ]

        event_info = {
            "id": event.id,
            "thumbnail": event.thumbnail,
            "event_type": event.event_type,
            "custom event name": event.custom_event_name,
            "rate": event.rate,
            "fixed_price": event.fixed_price,
            "vendor details": vendor_details
        }
        event_list.append(event_info)

    return jsonify({
        "status": True,
        "Total Events": total_events_found,
        "Events": event_list
    }), 200

################### Custom Event Search ###########################


# # new 
# @app.route("/custom_event_search", methods=["POST"])
# @jwt_required()
# def custom_event_search():
#     user = get_current_user()
#     data = request.get_json()
#     event_type = data.get("event_type")
#     location_name = data.get("location_name")
#     min_price = data.get("min_price")
#     max_price = data.get("max_price")
#     start_date = data.get("start_date")
#     end_date = data.get("end_date")
#     start_time = data.get("start_time")
#     end_time = data.get("end_time")
#     all_day = data.get("all_day")
#     latitude = data.get("event_latitude")
#     longitude = data.get("event_longitude")
#     ratings = data.get("ratings")
#     query = db.session.query(Event)

#     if event_type:
#         query = query.filter(func.lower(Event.event_type) == event_type.lower())

#     if location_name:
#         query = query.filter(or_(Event.location_name.ilike(f"%{location_name}%")))

#     if min_price is not None and max_price is not None:
#         query = query.filter(Event.rate.between(min_price, max_price))
#     elif min_price is not None or max_price is not None:
#         if min_price is not None:
#             query = query.filter(Event.rate >= min_price)
#         elif max_price is not None:
#             query = query.filter(Event.rate <= max_price)

#     if not all_day and start_date and end_date and start_time and end_time:
#         subquery = db.session.query(Booking.event_id).filter(
#             (Booking.start_date <= end_date) &
#             (Booking.end_date >= start_date) &
#             (Booking.start_time <= end_time) &
#             (Booking.end_time >= end_time)
#         ).distinct()
#         query = query.filter(~Event.id.in_(subquery))

#     results = query.all()
#     user_location = (latitude, longitude)
#     serialized_results = []

#     for event in results:
#         if event.latitude is not None and event.longitude is not None:
#             event_location = (event.latitude, event.longitude)
#             distance = geodesic(event_location, user_location).kilometers
#             if distance <= 5:
#                 vendor_profile_image = event.vendor.user[0].profile_image  # Assuming only one user for the vendor

#                 fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]

#                 is_favorite = event.id in fav_event_ids

#                 serialized_event = {
#                     "id": event.id,
#                     "thumbnail": event.thumbnail,
#                     "event_type": event.event_type,
#                     "rate": event.rate,
#                     "event_rating": Ratings.get_average_rating(event.id),
#                     "fixed_price": event.fixed_price,
#                     "distance_km": distance,
#                     "address": event.vendor.location,  # Modify as per the actual address field in your model
#                     "location": event.location_name,  # Modify as per the actual field name
#                     "favorite": is_favorite,
#                     "vendor_details": {
#                         "vendor_profile_image": vendor_profile_image,
#                         "vendor_id": event.vendor.id
#                     }
#                 }
#                 serialized_results.append(serialized_event)

#     sorted_results = sorted(serialized_results, key=lambda x: x["event_rating"], reverse=True)

#     return jsonify({
#         "status": True,
#         "Search Result Found": f"{len(sorted_results)} vendors found for {location_name} with {ratings} star rating",
#         "Search results": sorted_results
#     })



# # # new one
# @app.route("/custom_event_search", methods=["POST"])
# @jwt_required()
# def custom_event_search():
#     user = get_current_user()
#     data = request.get_json()
#     event_type = data.get("event_type")
#     location_name = data.get("location_name")
#     min_price = data.get("min_price")
#     max_price = data.get("max_price")
#     start_date = data.get("start_date")
#     end_date = data.get("end_date")
#     start_time = data.get("start_time")
#     end_time = data.get("end_time")
#     all_day = data.get("all_day")
#     latitude = data.get("event_latitude")
#     longitude = data.get("event_longitude")
#     ratings = data.get("ratings")
#     query = db.session.query(Event)

#     if event_type:
#         query = query.filter(func.lower(Event.event_type) == event_type.lower())

#     if location_name:
#         query = query.filter(or_(Event.location_name.ilike(f"%{location_name}%")))

#     if min_price is not None and max_price is not None:
#         query = query.filter(Event.rate.between(min_price, max_price))

#     elif min_price is not None or max_price is not None:
#         if min_price is not None:
#             query = query.filter(Event.rate >= min_price)
#         elif max_price is not None:
#             query = query.filter(Event.rate <= max_price)

#     if not all_day and start_date and end_date and start_time and end_time:
#         subquery = db.session.query(Booking.event_id).filter(
#             (Booking.start_date <= end_date) &
#             (Booking.end_date >= start_date) &
#             (Booking.start_time <= end_time) &
#             (Booking.end_time >= end_time)
#         ).distinct()  # .distinct is used where we are getting multiple rows for the same event it will get one only
#         query = query.filter(~Event.id.in_(subquery))  

#     if latitude is not None and longitude is not None:
#         # If latitude and longitude are provided, prioritize location-based search
#         user_location = (latitude, longitude)
#         results = query.all()
#         serialized_results = []

#         for event in results:
#             if event.latitude is not None and event.longitude is not None:
#                 event_location = (event.latitude, event.longitude)
#                 distance = geodesic(event_location, user_location).kilometers
#                 if distance <= 5:
#                     vendor_profile_image = event.vendor.user[0].profile_image  # Assuming only one user for the vendor

#                     fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]

#                     is_favorite = event.id in fav_event_ids

#                     serialized_event = {
#                         "id": event.id,
#                         "thumbnail": event.thumbnail,
#                         "event_type": event.event_type,
#                         "rate": event.rate,
#                         "event_rating": Ratings.get_average_rating(event.id),
#                         "fixed_price": event.fixed_price,
#                         "distance_km": distance,
#                         "address": event.vendor.location,  
#                         "location": event.location_name,  
#                         "favorite": is_favorite,
#                         "vendor_details": {
#                             "vendor_profile_image": vendor_profile_image,
#                             "vendor_id": event.vendor.id
#                         }
#                     }
#                     serialized_results.append(serialized_event)

#         sorted_results = sorted(serialized_results, key=lambda x: x["event_rating"], reverse=True)

#         return jsonify({
#             "status": True,
#             "Search Result Found": f"{len(sorted_results)} vendors found for {location_name} with {ratings} star rating",
#             "Search results": sorted_results
#         })
#     else:
#         results = query.all()
#         serialized_results = []
#         for event in results:
#             vendor_profile_image = event.vendor.user[0].profile_image  

#             serialized_event = {
#                 "id": event.id,
#                 "thumbnail": event.thumbnail,
#                 "event_type": event.event_type,
#                 "rate": event.rate,
#                 "event_rating": Ratings.get_average_rating(event.id),
#                 "fixed_price": event.fixed_price,
#                 "address": event.vendor.location,  
#                 "location": event.location_name,  
#                 "vendor_details": {
#                     "vendor_profile_image":vendor_profile_image,
#                     "vendor_id": event.vendor.id
#                 }
#             }
#             serialized_results.append(serialized_event)

#         sorted_results = sorted(serialized_results, key=lambda x: x["event_rating"], reverse=True)

#         return jsonify({
#             "status": True,
#             "Search Result Found": f"{len(sorted_results)} vendors found for {location_name} with {ratings} star rating",
#             "Search results": sorted_results
#         })


# # new one two
@app.route("/custom_event_search", methods=["POST"])
@jwt_required()
def custom_event_search():
    user = get_current_user()
    data = request.get_json()
    event_type = data.get("event_type")
    location_name = data.get("location_name")
    min_price = data.get("min_price")
    max_price = data.get("max_price")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    all_day = data.get("all_day")
    latitude = data.get("event_latitude")
    longitude = data.get("event_longitude")
    ratings = data.get("ratings")
    query = db.session.query(Event)

    if event_type:
        query = query.filter(func.lower(Event.event_type) == event_type.lower())

    if location_name:
        query = query.filter(or_(Event.location_name.ilike(f"%{location_name}%")))

    if min_price is not None and max_price is not None:
        query = query.filter(Event.rate.between(min_price, max_price))

    elif min_price is not None or max_price is not None:
        if min_price is not None:
            query = query.filter(Event.rate >= min_price)
        elif max_price is not None:
            query = query.filter(Event.rate <= max_price)

    if not all_day and start_date and end_date and start_time and end_time:
        subquery = db.session.query(Booking.event_id).filter(
            (Booking.start_date <= end_date) &
            (Booking.end_date >= start_date) &
            (Booking.start_time <= end_time) &
            (Booking.end_time >= end_time)
        ).distinct()  
        query = query.filter(~Event.id.in_(subquery))  

    if latitude is not None and longitude is not None:
        # If latitude and longitude are provided, prioritize location-based search
        user_location = (latitude, longitude)
        results = query.all()
        serialized_results = []

        for event in results:
            if event.latitude is not None and event.longitude is not None:
                event_location = (event.latitude, event.longitude)
                distance = geodesic(event_location, user_location).kilometers
                event_rating = Ratings.get_average_rating(event.id)  # Get event rating using Ratings class
                if distance <= 5 and event_rating <= ratings:  # Filter by rating threshold
                    vendor_profile_image = event.vendor.user[0].profile_image  

                    fav_event_ids = [favorite.event_id for favorite in Favorites.query.filter_by(user_id=user.id).all()]

                    is_favorite = event.id in fav_event_ids

                    serialized_event = {
                        "id": event.id,
                        "thumbnail": event.thumbnail,
                        "event_type": event.event_type,
                        "rate": event.rate,
                        "event_rating": event_rating,  # Use event_rating obtained from Ratings class
                        "fixed_price": event.fixed_price,
                        "distance_km": distance,
                        "address": event.vendor.location,  
                        "location": event.location_name,  
                        "favorite": is_favorite,
                        "vendor_details": {
                            "vendor_profile_image": vendor_profile_image,
                            "vendor_id": event.vendor.id
                        }
                    }
                    serialized_results.append(serialized_event)

        sorted_results = sorted(serialized_results, key=lambda x: x["event_rating"], reverse=True)

        return jsonify({
            "status": True,
            "Search Result Found": f"{len(sorted_results)} vendors found for {location_name} with {ratings} star rating or below",
            "Search results": sorted_results
        })
    else:
        results = query.all()
        serialized_results = []
        for event in results:
            event_rating = Ratings.get_average_rating(event.id)  # Get event rating using Ratings class
            if event_rating <= ratings:  # Filter by rating threshold
                vendor_profile_image = event.vendor.user[0].profile_image  

                serialized_event = {
                    "id": event.id,
                    "thumbnail": event.thumbnail,
                    "event_type": event.event_type,
                    "rate": event.rate,
                    "event_rating": event_rating,  # Use event_rating obtained from Ratings class
                    "fixed_price": event.fixed_price,
                    "address": event.vendor.location,  
                    "location": event.location_name,  
                    "vendor_details": {
                        "vendor_profile_image":vendor_profile_image,
                        "vendor_id": event.vendor.id
                    }
                }
                serialized_results.append(serialized_event)

        sorted_results = sorted(serialized_results, key=lambda x: x["event_rating"], reverse=True)

        return jsonify({
            "status": True,
            "Search Result Found": f"{len(sorted_results)} vendors found for {location_name} with {ratings} star rating or below",
            "Search results": sorted_results
        })



@app.route("/cancel_booking_by_vendor", methods = ["POST"])
@jwt_required()
def cancel_booking_by_vendor():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendors can cancel bookings."
            })
        
        booking_id = data.get("booking_id")

        booking_to_cancel = Booking.query.filter_by(id=booking_id).first()

        if booking_to_cancel.cancelled == 1:
            return jsonify({
                "message":"Booking is already cancelled !1"
        })

        if not booking_to_cancel or booking_to_cancel.event.vendor.id != user.vendor.id:
            return jsonify({
                "message":"Booking not found or unauthorized to cancel"})

        booking_to_cancel.cancelled = True  
        db.session.commit()
        vendor = user.vendor
        notification = Notification(
            title="Booking Cancellation",
            message="We regret to inform you that your booking with "+vendor.full_name+" has been canceled. The venue/vendor has updated their availability. If you have any concerns, feel free to reach out. 🙁",
            message_type="booking",
            readed=False,
            user_id=booking_to_cancel.user_id
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({
            "status":True,
            "message":"Successfully cancelled the booking !!",
            "event_id":booking_to_cancel.event_id,
            "vendor_id":booking_to_cancel.event.vendor.id
        })
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500
        

        
@app.route("/cancel_booking", methods = ["POST"])
@jwt_required()
def cancel_booking():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            })
            
        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only vendor can cancel bookings."
            })

        booking_id = data.get("booking_id")

        booking_to_cancel = Booking.query.filter_by(id=booking_id, user_id = user.id).first()

        if not booking_to_cancel:
            return jsonify({
                "status":False,
                "message":"Booking not found"
            })
        
        booking_to_cancel.cancelled = True  
        db.session.commit()
        event = Event.query.filter_by(id=booking_to_cancel.event_id).first()
        notification = Notification(
            title="Booking Cancellation",
            message="Attention: A booking for your venue has been canceled. Please review your calendar, and if needed, update availability for future bookings. 🗓️",
            message_type="booking",
            readed=False,
            user_id=event.vendor.id
        )
        db.session.add(notification)
        db.session.commit()
        return jsonify({
            "status":True,
            "message":"Booking cancelled successfully !!"
        })
    
    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500

###############################   Create Booking      ######################################

@app.route('/create_bookingss', methods=["POST"])
@jwt_required()
def create_bookingaa():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            })

        full_name = data.get('full_name')
        email = data.get('email')
        guest_count = data.get('guest_count')
        additional_notes = data.get('additional_notes', '')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        all_day = data.get('all_day')
        event_id = data.get('event_id')
        event_type = data.get("event_type")
        if not all([full_name, email, guest_count, start_date, end_date, event_id]):
            return jsonify({
                "status":False,
                "message": "All necessary fields must be set !!"
            })

        # If it's an all-day event, set start_time and end_time accordingly
        if all_day:
            start_time = "00:00:00"
            end_time = "23:59:59"
        else:
            start_time = data.get('start_time', "00:00:00")
            end_time = data.get('end_time', "23:59:59")

        # Calculate total event hours
        event_hours = calculate_event_hours(start_date, end_date, start_time, end_time, all_day)

        overlapping_booking = Booking.query.filter(
            (Booking.event_id == event_id) &
            (Booking.start_date <= start_date) &
            (Booking.end_date >= end_date) &
            (Booking.start_time <= start_time) &
            (Booking.end_time == end_time)
        ).first()

        if overlapping_booking:
            return jsonify({
                "status":False,
                "message": "Event Is already booked !!"
            })

        # Calculate the rate and other values
        event = Event.query.filter_by(id=event_id).first()
        subtotal = event_hours * event.rate
        tax_percentage = 0.15
        total_price = subtotal + (subtotal * tax_percentage)

        # Create and save the booking
        booking = Booking(
            user_id=user.id,
            full_name=full_name,
            email=email,
            guest_count=guest_count,
            additional_notes=additional_notes,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            all_day=all_day,
            event_id=event_id,
            event_type=event_type
        )

        db.session.add(booking)
        db.session.commit()

        return jsonify({
            "status":True,
            "Summary": {
                "Event Hours": f"{event_hours} Hours",
                "Guests": f"{guest_count}",
                "Vendor Rate": f"{event.rate}$",
                "Subtotal": f"{subtotal}$",
                "Taxes (15%)": "15%",
                "Total Price": f"{total_price} $"
            }
        })

    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500


###############################   Vendor's Events      ######################################



@app.route("/vendor_events", methods=["POST"])
@jwt_required()
def vendor_events():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User not authenticated",
            }), 401
    
        if user.role != "vendor":
            return jsonify({
                "status": False,
                "message": "Can only access by the vendor !!"
            }), 401
        
        event_date_str = data.get("event_date_str")
        if not event_date_str:
            return jsonify({
                "status": False,
                "message": "Date is required!"
            }), 400
        
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

        # Query to fetch events on the specified date
        events_on_date = Booking.query.options(joinedload(Booking.event)).filter(
            (Booking.start_date == event_date) &
            (Booking.event.has(Event.vendor.has(Vendor.id == user.vendor.id))) &
            (~Booking.cancelled)
        ).all()

        # Query to fetch events for the rest of the month # options is for getting the additional data with the main data
        events_for_month_afterwards = Booking.query.options(joinedload(Booking.event)).filter(
            (Booking.start_date > event_date) &
            (Booking.start_date < event_date.replace(day=1) + timedelta(days=32)) &
            (Booking.event.has(Event.vendor.has(Vendor.id == user.vendor.id))) &
            (Booking.cancelled)
        ).all()

        events_on_date_dict = []
        for booking in events_on_date:
            events_dict = {
                "location_name":booking.event.location_name,
                "event_thumbnail":booking.event.thumbnail,
                "user_profile_image":booking.user.profile_image,
                "other_details":booking.as_dict()
            }
            events_on_date_dict.append(events_dict)


        events_after_date_dict = []
        for booking in events_for_month_afterwards:
            events_dict = {
                "location_name":booking.event.location_name,
                "event_thumbnail":booking.event.thumbnail,
                "user_profile_image":booking.user.profile_image,
                "other_details":booking.as_dict_po()
            }
            events_after_date_dict.append(events_dict)

        return jsonify({
            "status": True,
            "total_events_on_date": events_on_date_dict,
            "total_length_of_events_on_date": len(events_on_date_dict),
            "total_events_after_date": events_after_date_dict,
            "total_length_of_events_after_date": len(events_after_date_dict)
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500



# @app.route('/create_booking_validate', methods=["POST"])
# @jwt_required()
# def create_booking_validate():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status":False,
#                 "message": "User not authenticated !!"
#             })
            
#         if user.role != "user":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only users can create bookings."
#             })

#         full_name = data.get('full_name')
#         email = data.get('email')
#         guest_count = data.get('guest_count')
#         additional_notes = data.get('additional_notes', '')
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         all_day = data.get('all_day')
#         event_id = data.get('event_id')
#         print("Event ID:", event_id)  # Debugging: Print event ID to check if it's received correctly
#         event_type = data.get("event_type")
#         apply_extra_facility_for_complete_event = data.get("apply_extra_facility_for_complete_event", False)
#         extra_facilities = data.get("extra_facilities", [])

#         desired_day_of_week = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
#         print("Desired day of week:", desired_day_of_week)  # Debugging: Print desired day of the week
#         event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=desired_day_of_week).first()
#         print("Event timings:", event_timings)  # Debugging: Print event timings to check if they are found

#         if not event_timings:
#             return jsonify({
#                 "status": False,
#                 "message": "Event timings not found. Unable to create booking !!"
#             }), 400

#         if not all([full_name, email, guest_count, start_date, end_date, event_id]):
#             return jsonify({
#                 "status":False,
#                 "message": "All necessary fields must be set !!"
#             })
#         # print("SSSSSSSSSSSSSSSSSSSSSSSSSSSS",start_time)
#         # print("EEEEEEEEEEEEEEEEEEEEEEEEEEEE",end_time)

#         # Debugging: Print event details to check if the event exists and its capacities
#         event = Event.query.filter_by(id=event_id).first()
#         print("Event:", event)
#         print("Event guest capacity:", event.guest_capacity)

#         if guest_count:
#             if not guest_count <= event.guest_capacity:
#                 return jsonify({
#                     "status":False,
#                     "message":"This event has the capacity of people up to ___ only."
#                 })
#         print("",guest co)

#         start_time = datetime.strptime(data.get("start_time", str(event_timings.start_time)), "%H:%M:%S").time()
#         end_time = datetime.strptime(data.get("end_time", str(event_timings.end_time)), "%H:%M:%S").time()


#         if start_time < event_timings.start_time or end_time > event_timings.end_time:
#             print("Booking timings out of range for this day.")
#             return jsonify({
#                 "status": False,
#                 "message": "Booking timings out of range for this day."
#             }), 400

#         # If it's an all-day event, set start_time and end_time accordingly
#         if all_day:
#             start_time = event_timings.start_time
#             end_time = event_timings.end_time
#         else:
#             start_time = data.get('start_time', event_timings.start_time)
#             end_time = data.get('end_time', event_timings.end_time)

#         selected_extra_facility = None

#         extra_facility_id = None
#         for facility in extra_facilities:
#             facility_id = facility.get("extra_facility_id")
#             if facility_id:
#                 extra_facility_id = facility_id
#                 break

#         if extra_facility_id:
#             print(f"Trying to find ExtraFacility with ID {extra_facility_id} for Event ID {event_id}")
#             selected_extra_facility = ExtraFacility.query.filter_by(id=extra_facility_id, event_id=event_id).first()
#             print("Selected ExtraFacility:", selected_extra_facility)

#         if selected_extra_facility is None and len(extra_facilities)!=0:
#             print("Selected extra facility is not available for the specified event !!")
#             return jsonify({
#                 "status": False,
#                 "message": "Selected extra facility is not available for the specified event !!"
#             }), 400

#         # Calculate total event hours
#         event_hours = DateTimeConversions.calculate_event_hours(start_date, end_date, start_time, end_time, all_day)

#         overlapping_booking = Booking.query.filter(
#             (Booking.event_id == event_id) &
#             (Booking.start_date <= start_date) &
#             (Booking.end_date >= end_date) &
#             (Booking.start_time <= start_time) &
#             (Booking.end_time == end_time)
#         ).first()

#         if overlapping_booking:
#             print("Event is already booked !!")
#             return jsonify({
#                 "status": False,
#                 "message": "Event is already booked !!"
#             })

#         extra_facility_cost = 0
#         event = Event.query.filter_by(id=event_id).first()
#         subtotal = event_hours * event.rate
#         subtotal += extra_facility_cost

#         # Calculate tax (15% of the subtotal, not including extra_facility_cost)
#         tax_percentage = 0.15
#         tax_amount = subtotal * tax_percentage

#         # Calculate the final total price
#         total_price = subtotal + tax_amount
#         print("Extra Facility ID:", extra_facility_id)
#         print("This is ssss")
#         # Create and save the booking
#         if event and event_timings.available:
#             booking = Booking(
#                 user_id=user.id,
#                 full_name=full_name,
#                 email=email,
#                 guest_count=guest_count,
#                 additional_notes=additional_notes,
#                 start_date=start_date,
#                 end_date=end_date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 all_day=all_day,
#                 event_id=event_id,
#                 event_type=event_type,
#                 extra_facility_id=extra_facility_id
#             )
#             db.session.add(booking)

#             vendor = Vendor.query.filter_by(id=event.vendor_id).first()
#             if vendor:
#                 vendor.wallet += subtotal

#         for facility in extra_facilities:
#             facility_id = facility.get("extra_facility_id")
#             if facility_id:
#                 selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

#                 if selected_extra_facility is not None:
#                     unit_price_count = facility.get("unit_price_count")
#                     extra_facility_hours = facility.get("extra_facility_hours")
#                     apply_extra_facility_for_complete_event = facility.get("apply_extra_facility_for_complete_event")
#                     print(selected_extra_facility.unit," this is the unit")
#                     if selected_extra_facility.unit == "item":
#                             unit = "item"
#                             quantity = unit_price_count
#                             extra_facility_cost += unit_price_count * selected_extra_facility.rate
#                     else:
#                         if selected_extra_facility.unit == "hour":
#                             unit = "hour"
#                             quantity = extra_facility_hours
#                             extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
#                         else:
#                             print("Invalid input. This extra facility is not based on hours.")
#                             return jsonify({
#                                 "status": False,
#                                 "message": "Invalid input. This extra facility is not based on hours."
#                             }), 400
#                         if apply_extra_facility_for_complete_event:
#                             extra_facility_cost += selected_extra_facility.rate * event_hours

#                 else:
#                     print("Invalid input. Please provide either unit_price_count, extra_facility_hours, or apply_extra_facility_for_complete_event.")
#                     return jsonify({
#                     "status": False,
#                     "message": "Invalid input. Please provide either unit_price_count, extra_facility_hours, or apply_extra_facility_for_complete_event."
#                 }), 400

#                 booking_extra_facility = BookingExtraFacility(
#                         booking_id=booking.id,
#                         unit=unit,
#                         extra_facility_id=facility_id,
#                         quantity=quantity
#                         )
#                 db.session.add(booking_extra_facility)

#             else:
#                 print("Specified facility for your selected event is not available")
#                 return jsonify({
#                     "status":False,
#                     "message":"Specified facility for your selected event is not available"
#                 }), 404

#             return jsonify({
#                 "status": True,
#                 "Summary": {
#                     "event_hours": f"{event_hours} Hours",
#                     "guest_count": f"{guest_count}",
#                     "event_rate": f"{event.rate}$",
#                     "subtotal": f"{subtotal}$",
#                     "extra_facility_cost": f"{extra_facility_cost}",
#                     "tax": f"{tax_amount}$ (15%)",
#                     "total_price": f"{total_price} $"
#                 }
#             }), 200
#         else:
#             print(f"{event.location_name} is not operating today !!")
#             print(f"{event.id} is not operating today !!")

#             return jsonify({
#                 "status": False,
#                 "message": f"{event.location_name} is not operating today !!"
#             }), 400

#     except Exception as e:
#         print(e)
#         return jsonify({
#             "status":False,
#             "message": str(e)
#         }), 500


# # working api
# @app.route('/create_booking_validate', methods=["POST"])
# @jwt_required()
# def create_booking_validate():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status": False,
#                 "message": "User not authenticated !!"
#             }), 401
            
#         if user.role != "user":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only users can create bookings."
#             }), 401

#         full_name = data.get('full_name')
#         email = data.get('email')
#         guest_count = data.get('guest_count')
#         additional_notes = data.get('additional_notes', '')
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         all_day = data.get('all_day')
#         event_id = data.get('event_id')
#         event_type = data.get("event_type")
#         apply_extra_facility_for_complete_event = data.get("apply_extra_facility_for_complete_event", False)
#         extra_facilities = data.get("extra_facilities", [])

#         desired_day_of_week = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
#         event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=desired_day_of_week).first()

#         if not event_timings:
#             return jsonify({
#                 "status": False,
#                 "message": "Event timings not found. Unable to create booking !!"
#             }), 400

#         if not all([full_name, email, guest_count, start_date, end_date, event_id]):
#             return jsonify({
#                 "status": False,
#                 "message": "All necessary fields must be set !!"
#             }), 400

#         event = Event.query.filter_by(id=event_id).first()

#         if event.guest_capacity is not None and guest_count is not None:
#             if guest_count > event.guest_capacity:
#                 return jsonify({
#                     "status": False,
#                     "message": "This event has a maximum capacity of {} guests.".format(event.guest_capacity)
#                 }), 400

#         start_time = datetime.strptime(data.get("start_time", str(event_timings.start_time)), "%H:%M:%S").time()
#         end_time = datetime.strptime(data.get("end_time", str(event_timings.end_time)), "%H:%M:%S").time()

#         if start_time >= end_time:
#             return jsonify({
#                 "status":False,
#                 "message":"Invalid Timing (start_time is greater than the end time)"
#             }), 400

#         if start_time < event_timings.start_time or end_time > event_timings.end_time:
#             return jsonify({
#                 "status": False,
#                 "message": "Booking timings out of range for this day."
#             }), 400

#         if all_day:
#             start_time = event_timings.start_time
#             end_time = event_timings.end_time

#         # Calculate event hours
#         start_datetime = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d"), start_time)
#         end_datetime = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d"), end_time)
#         event_hours = (end_datetime - start_datetime).total_seconds() / 3600  # Convert seconds to hours

#         overlapping_booking = Booking.query.filter(
#             (Booking.event_id == event_id) &
#             (Booking.start_date <= start_date) &
#             (Booking.end_date >= end_date) &
#             (Booking.start_time <= start_time) &
#             (Booking.end_time == end_time)
#         ).first()

#         if overlapping_booking:
#             return jsonify({
#                 "status": False,
#                 "message": "Event is already booked."
#             }), 400

#         extra_facility_cost = 0
#         subtotal = event_hours * event.rate

#         if apply_extra_facility_for_complete_event:
#             for facility in extra_facilities:
#                 facility_id = facility.get("extra_facility_id")
#                 if facility_id:
#                     selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

#                     if selected_extra_facility:
#                         unit_price_count = facility.get("unit_price_count", 0)
#                         extra_facility_hours = facility.get("extra_facility_hours", 0)
#                         if selected_extra_facility.unit == "item":
#                             extra_facility_cost += unit_price_count * selected_extra_facility.rate
#                         elif selected_extra_facility.unit == "hour":
#                             extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
#                         else:
#                             return jsonify({
#                                 "status": False,
#                                 "message": "Invalid input. This extra facility is not based on hours."
#                             }), 400


#         if event and event_timings.available:
#             print(event_hours)
#             booking = Booking(
#                 user_id=user.id,
#                 full_name=full_name,
#                 email=email,
#                 guest_count=guest_count,
#                 additional_notes=additional_notes,
#                 start_date=start_date,
#                 end_date=end_date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 all_day=all_day,
#                 event_id=event_id,
#                 event_type=event_type
#             )
#             db.session.add(booking)

#             vendor = Vendor.query.filter_by(id=event.vendor_id).first()
#             if vendor:
#                 vendor.wallet += subtotal

#             for facility in extra_facilities:
#                 facility_id = facility.get("extra_facility_id")
#                 if facility_id:
#                     selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

#                     if selected_extra_facility:
#                         unit_price_count = facility.get("unit_price_count", 0)
#                         extra_facility_hours = facility.get("extra_facility_hours", 0)
#                         if selected_extra_facility.unit == "item":
#                             extra_facility_cost += unit_price_count * selected_extra_facility.rate
#                         elif selected_extra_facility.unit == "hour":
#                             extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
#                         else:
#                             return jsonify({
#                                 "status": False,
#                                 "message": "Invalid input. This extra facility is not based on hours."
#                             }), 400

#                         booking_extra_facility = BookingExtraFacility(
#                             booking_id=booking.id,
#                             unit=selected_extra_facility.unit,
#                             extra_facility_id=facility_id,
#                             quantity=unit_price_count if selected_extra_facility.unit == "item" else extra_facility_hours
#                         )
#                         db.session.add(booking_extra_facility)

#             tax_percentage = 0.15
#             print(extra_facility_cost)
#             subtotal += extra_facility_cost
#             tax_amount = subtotal * tax_percentage
#             total_price = subtotal + tax_amount 
#         else:
#             return jsonify({
#                 "status": False,
#                 "message": "Event is not available for booking on this day."
#             }), 400

#         return jsonify({
#             "status": True,
#             "Summary": {
#                 "event_hours": "{:.2f} Hours".format(event_hours),
#                 "guest_count": str(guest_count),
#                 "event_rate": "{:.2f}$".format(event.rate),
#                 "subtotal": "{:.2f}$".format(subtotal),
#                 "extra_facility_cost": "{:.2f}$".format(extra_facility_cost),
#                 "tax": "{:.2f}$ (15%)".format(tax_amount),
#                 "total_price": "{:.2f} $".format(total_price)
#             }
#         }), 200

#     except Exception as e:
#         print(e)
#         return jsonify({
#             "status": False,
#             "message": str(e)
#         }), 500



# working api
@app.route('/create_booking_validate', methods=["POST"])
@jwt_required()
def create_booking_validate():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User not authenticated !!"
            }), 401
            
        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can create bookings."
            }), 401

        full_name = data.get('full_name')
        email = data.get('email')
        guest_count = data.get('guest_count')
        additional_notes = data.get('additional_notes', '')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        all_day = data.get('all_day')
        event_id = data.get('event_id')
        event_type = data.get("event_type")
        apply_extra_facility_for_complete_event = data.get("apply_extra_facility_for_complete_event", False)
        extra_facilities = data.get("extra_facilities", [])

        desired_day_of_week = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
        event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=desired_day_of_week).first()

        if not event_timings:
            return jsonify({
                "status": False,
                "message": "Event timings not found. Unable to create booking !!"
            }), 400

        if not all([full_name, email, guest_count, start_date, end_date, event_id]):
            return jsonify({
                "status": False,
                "message": "All necessary fields must be set !!"
            }), 400

        event = Event.query.filter_by(id=event_id).first()

        if event.guest_capacity is not None and guest_count is not None:
            if guest_count > event.guest_capacity:
                return jsonify({
                    "status": False,
                    "message": "This event has a maximum capacity of {} guests.".format(event.guest_capacity)
                }), 400

        start_time = datetime.strptime(data.get("start_time", str(event_timings.start_time)), "%H:%M:%S").time()
        end_time = datetime.strptime(data.get("end_time", str(event_timings.end_time)), "%H:%M:%S").time()

        if start_time >= end_time:
            return jsonify({
                "status":False,
                "message":"Invalid Timing (start_time is greater than the end time)"
            }), 400

        if start_time < event_timings.start_time or end_time > event_timings.end_time:
            return jsonify({
                "status": False,
                "message": "Booking timings out of range for this day."
            }), 400

        if all_day:
            start_time = event_timings.start_time
            end_time = event_timings.end_time

        # Calculate event hours
        start_datetime = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d"), start_time)
        end_datetime = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d"), end_time)
        event_hours = (end_datetime - start_datetime).total_seconds() / 3600  # Convert seconds to hours

        overlapping_booking = Booking.query.filter(
            (Booking.event_id == event_id) &
            (Booking.start_date <= start_date) &
            (Booking.end_date >= end_date) &
            (Booking.start_time <= start_time) &
            (Booking.end_time == end_time)
        ).first()

        if overlapping_booking:
            return jsonify({
                "status": False,
                "message": "Event is already booked."
            }), 400

        extra_facility_cost = 0
        subtotal = event_hours * event.rate

        if apply_extra_facility_for_complete_event:
            for facility in extra_facilities:
                facility_id = facility.get("extra_facility_id")
                if facility_id:
                    selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

                    if selected_extra_facility:
                        unit_price_count = facility.get("unit_price_count", 0)
                        extra_facility_hours = facility.get("extra_facility_hours", 0)
                        if selected_extra_facility.unit == "item":
                            extra_facility_cost += unit_price_count * selected_extra_facility.rate
                        elif selected_extra_facility.unit == "hour":
                            extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
                        else:
                            return jsonify({
                                "status": False,
                                "message": "Invalid input. This extra facility is not based on hours."
                            }), 400


        if event and event_timings.available:
            print(event_hours)
            booking = Booking(
                user_id=user.id,
                full_name=full_name,
                email=email,
                guest_count=guest_count,
                additional_notes=additional_notes,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                all_day=all_day,
                event_id=event_id,
                event_type=event_type
            )
            db.session.add(booking)

            vendor = Vendor.query.filter_by(id=event.vendor_id).first()
            if vendor:
                vendor.wallet += subtotal

            for facility in extra_facilities:
                facility_id = facility.get("extra_facility_id")
                if facility_id:
                    selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

                    if selected_extra_facility:
                        unit_price_count = facility.get("unit_price_count", 0)
                        extra_facility_hours = facility.get("extra_facility_hours", 0)
                        if selected_extra_facility.unit == "item":
                            extra_facility_cost += unit_price_count * selected_extra_facility.rate
                        elif selected_extra_facility.unit == "hour":
                            extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
                        else:
                            return jsonify({
                                "status": False,
                                "message": "Invalid input. This extra facility is not based on hours."
                            }), 400

                        booking_extra_facility = BookingExtraFacility(
                            booking_id=booking.id,
                            unit=selected_extra_facility.unit,
                            extra_facility_id=facility_id,
                            quantity=unit_price_count if selected_extra_facility.unit == "item" else extra_facility_hours
                        )
                        db.session.add(booking_extra_facility)

            tax_percentage = 0.15
            print(extra_facility_cost)
            subtotal += extra_facility_cost
            tax_amount = subtotal * tax_percentage
            total_price = subtotal + tax_amount 
        else:
            return jsonify({
                "status": False,
                "message": "Event is not available for booking on this day."
            }), 400

        return jsonify({
            "status": True,
            "Summary": {
                "event_hours": round(event_hours, 2),  # Round event_hours to two decimal places
                "guest_count": guest_count,
                "event_rate": round(event.rate, 2),  # Round event.rate to two decimal places
                "subtotal": round(subtotal, 2),  # Round subtotal to two decimal places
                "extra_facility_cost": round(extra_facility_cost, 2),  # Round extra_facility_cost to two decimal places
                "tax": round(tax_amount, 2),  # Round tax_amount to two decimal places
                "total_price": round(total_price, 2)  # Round total_price to two decimal places
            }
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500




# # testing now
# @app.route('/create_booking', methods=["POST"])
# @jwt_required()
# def create_booking():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status":False,
#                 "message": "User not authenticated !!"
#             })
            
#         if user.role != "user":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only users can create bookings."
#             })

#         full_name = data.get('full_name')
#         email = data.get('email')
#         guest_count = data.get('guest_count')
#         additional_notes = data.get('additional_notes', '')
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')
#         all_day = data.get('all_day')
#         event_id = data.get('event_id')
#         print(event_id)
#         event_type = data.get("event_type")
#         apply_extra_facility_for_complete_event = data.get("apply_extra_facility_for_complete_event", False)
#         extra_facilities = data.get("extra_facilities", [])

#         desired_day_of_week = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
#         event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=desired_day_of_week).first()
#         if not event_timings:
#             return jsonify({
#                 "status": False,
#                 "message": "Event timings not found. Unable to create booking !!"
#             }), 400

#         if not all([full_name, email, guest_count, start_date, end_date, event_id]):
#             return jsonify({
#                 "status":False,
#                 "message": "All necessary fields must be set !!"
#             })
#         start_time = datetime.strptime(data.get("start_time", str(event_timings.start_time)), "%H:%M:%S").time()
#         end_time = datetime.strptime(data.get("end_time", str(event_timings.end_time)), "%H:%M:%S").time()

#         if start_time < event_timings.start_time or end_time > event_timings.end_time:
#             return jsonify({
#                 "status": False,
#                 "message": "Booking timings out of range for this day."
#             }), 400

#         # If it's an all-day event, set start_time and end_time accordingly
#         if all_day:
#             start_time = event_timings.start_time
#             end_time = event_timings.end_time
#         else:
#             start_time = data.get('start_time', event_timings.start_time)
#             end_time = data.get('end_time', event_timings.end_time)

#         selected_extra_facility = None

#         extra_facility_id = None
#         for facility in extra_facilities:
#             facility_id = facility.get("extra_facility_id")
#             if facility_id:
#                 extra_facility_id = facility_id
#                 break


#         if extra_facility_id:

#             print(f"Trying to find ExtraFacility with ID {extra_facility_id} for Event ID {event_id}")
#             selected_extra_facility = ExtraFacility.query.filter_by(id=extra_facility_id, event_id=event_id).first()
#             print("Selected ExtraFacility:", selected_extra_facility)

#         if selected_extra_facility is None:
#             return jsonify({
#                 "status": False,
#                 "message": "Selected extra facility is not available for the specified event !!"
#             }), 400

#         # Calculate total event hours
#         event_hours = DateTimeConversions.calculate_event_hours(start_date, end_date, start_time, end_time, all_day)

#         overlapping_booking = Booking.query.filter(
#             (Booking.event_id == event_id) &
#             (Booking.start_date <= start_date) &
#             (Booking.end_date >= end_date) &
#             (Booking.start_time <= start_time) &
#             (Booking.end_time == end_time)
#         ).first()

#         if overlapping_booking:
#             return jsonify({
#                 "status": False,
#                 "message": "Event is already booked !!"
#             })
        
#         extra_facility_cost = 0
#         event = Event.query.filter_by(id=event_id).first()
#         subtotal = event_hours * event.rate
#         subtotal += extra_facility_cost

#         # Calculate tax (15% of the subtotal, not including extra_facility_cost)
#         tax_percentage = 0.15
#         tax_amount = subtotal * tax_percentage

#         # Calculate the final total price
#         total_price = subtotal + tax_amount
#         print(extra_facility_id,"This is ssss")
#         # Create and save the booking
#         if event and event_timings.available:
#             booking = Booking(
#                 user_id=user.id,
#                 full_name=full_name,
#                 email=email,
#                 guest_count=guest_count,
#                 additional_notes=additional_notes,
#                 start_date=start_date,
#                 end_date=end_date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 all_day=all_day,
#                 event_id=event_id,
#                 event_type=event_type,
#                 extra_facility_id=extra_facility_id
#             )
#             db.session.add(booking)
#             db.session.commit()

#             vendor = Vendor.query.filter_by(id=event.vendor_id).first()
#             if vendor:
#                 vendor.wallet += subtotal
#             db.session.commit()
#         for facility in extra_facilities:
#             facility_id = facility.get("extra_facility_id")
#             if facility_id :
#                 selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

#                 if selected_extra_facility is not None :
#                     unit_price_count = facility.get("unit_price_count")
#                     extra_facility_hours = facility.get("extra_facility_hours")
#                     apply_extra_facility_for_complete_event = facility.get("apply_extra_facility_for_complete_event")
#                     print(selected_extra_facility.unit," this is the unit")
#                     if selected_extra_facility.unit == "item":
#                             unit = "item"
#                             quantity = unit_price_count
#                             extra_facility_cost += unit_price_count * selected_extra_facility.rate
#                     else:
#                         if selected_extra_facility.unit == "hour":
#                             unit = "hour"
#                             quantity = extra_facility_hours
#                             extra_facility_cost += extra_facility_hours * selected_extra_facility.rate
#                         else:
#                             return jsonify({
#                                 "status": False,
#                                 "message": "Invalid input. This extra facility is not based on hours."
#                             }), 400
#                         if apply_extra_facility_for_complete_event:
#                            extra_facility_cost += selected_extra_facility.rate * event_hours
                        

#                 else:
#                     return jsonify({
#                     "status": False,
#                     "message": "Invalid input. Please provide either unit_price_count, extra_facility_hours, or apply_extra_facility_for_complete_event."
#                 }), 400

#                 booking_extra_facility = BookingExtraFacility(
#                         booking_id=booking.id,
#                         unit=unit,
#                         extra_facility_id=facility_id,
#                         quantity=quantity
#                         )
#                 db.session.add(booking_extra_facility)

            

            
#             else:
#                 return jsonify({
#                     "status":False,
#                     "message":"Specified facility for your seleceted event is not available "
#                 }), 404

      
#              # Notification Data for Cancellation
#             send_notification_data = {
#                 "device_token": user.device_token,
#                 "title": "Booking Alert",
#                 "body": "Exciting news! You have a new booking! A user has successfully booked your venue for their upcoming event. Check your calendar for the details. 🎉"
#             }

#             # Send Notification
#             send_notification_response = Notificationpush.send_notification(send_notification_data)

#             if send_notification_response:
#                 notification_status = "Notification sent successfully"
#             else:
#                 notification_status = "Failed to send notification"
#             notification = Notification(
#                 title="New Booking Alert",
#                 message="Exciting news! You have a new booking! A user has successfully booked your venue for their upcoming event. Check your calendar for the details. 🎉",
#                 message_type="booking",
#                 readed=False,
#                 user_id=user.id
#             )
#             db.session.add(notification)
#             db.session.commit()
#             return jsonify({
#                 "status": True,
#                 "Summary": {
#                     "event_hours": f"{event_hours} Hours",
#                     "guest_count": f"{guest_count}",
#                     "event_rate": f"{event.rate}$",
#                     "subtotal": f"{subtotal}$",
#                     "extra_facility_cost": f"{extra_facility_cost}",
#                     "tax": f"{tax_amount}$ (15%)",
#                     "total_price": f"{total_price} $"
#                 }
#             }), 200
#         else:
#             return jsonify({
#                 "status": False,
#                 "message": f"{event.location_name} is not operating today !!"
#             }), 400
        

#     except Exception as e:
#         return jsonify({
#             "status":False,
#             "message": str(e)
#         }), 500




# currently working 
@app.route('/create_booking', methods=["POST"])
@jwt_required()
def create_booking():
    try:
        data = request.get_json()
        user = get_current_user()

        if not user:
            return jsonify({
                "status": False,
                "message": "User not authenticated !!"
            }), 401

        if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can create bookings."
            }), 403

        full_name = data.get('full_name')
        email = data.get('email')
        guest_count = data.get('guest_count')
        additional_notes = data.get('additional_notes', '')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        all_day = data.get('all_day')
        event_id = data.get('event_id')
        event_type = data.get("event_type")
        apply_extra_facility_for_complete_event = data.get("apply_extra_facility_for_complete_event", False)
        extra_facilities = data.get("extra_facilities", [])

        desired_day_of_week = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
        event_timings = eventtiming.query.filter_by(event_id=event_id, day_of_week=desired_day_of_week).first()

        if not event_timings:
            return jsonify({
                "status": False,
                "message": "Event timings not found. Unable to create booking !!"
            }), 400

        if not all([full_name, email, guest_count, start_date, end_date, event_id, event_type]):
            return jsonify({
                "status": False,
                "message": "All necessary fields must be set !!"
            }), 400

        event = Event.query.filter_by(id=event_id).first()
        if event.guest_capacity is not None and guest_count > event.guest_capacity:
            return jsonify({
                "status": False,
                "message": f"Guest count exceeds the maximum capacity ({event.guest_capacity}) for this event."
            }), 400
        
        start_time = datetime.strptime(data.get("start_time", str(event_timings.start_time)), "%H:%M:%S").time()
        end_time = datetime.strptime(data.get("end_time", str(event_timings.end_time)), "%H:%M:%S").time()

        if start_time >= end_time:
            return jsonify({
                "status": False,
                "message": "Invalid booking timings. End time must be after start time."
            }), 400

        if start_time < event_timings.start_time or end_time > event_timings.end_time:
            return jsonify({
                "status": False,
                "message": "Booking timings out of range for this day."
            }), 400

        # If it's an all-day event, set start_time and end_time accordingly
        if all_day:
            start_time = event_timings.start_time
            end_time = event_timings.end_time
        else:
            start_time = start_time
            end_time = end_time

        # Calculate booking duration in hours
        booking_duration_hours = (datetime.combine(datetime.min, end_time) - datetime.combine(datetime.min, start_time)).seconds / 3600

        overlapping_booking = Booking.query.filter(
            (Booking.event_id == event_id) &
            (Booking.start_date <= start_date) &
            (Booking.end_date >= end_date) &
            (Booking.start_time <= start_time) &
            (Booking.end_time == end_time)
        ).first()

        if overlapping_booking:
            return jsonify({
                "status": False,
                "message": "Event is already booked !!"
            })

        extra_facility_cost = 0

        for facility in extra_facilities:
            facility_id = facility.get("extra_facility_id")

            if facility_id:
                selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

                if selected_extra_facility:
                    unit_price_count = facility.get("unit_price_count")
                    extra_facility_hours = facility.get("extra_facility_hours")
                    apply_extra_facility_for_complete_event = facility.get("apply_extra_facility_for_complete_event")

                    if unit_price_count is not None:
                        if selected_extra_facility.unit == "unit":
                            extra_facility_cost += unit_price_count * selected_extra_facility.rate

                    elif extra_facility_hours is not None:
                        if selected_extra_facility.unit == "hour":
                            extra_facility_cost += extra_facility_hours * selected_extra_facility.rate

                    elif apply_extra_facility_for_complete_event:
                        extra_facility_cost += selected_extra_facility.rate * booking_duration_hours

                else:
                    return jsonify({
                        "status": False,
                        "message": "Invalid input. Selected extra facility is not available for the specified event."
                    }), 400

        extra_facilities_event = event.extra_facilities
        subtotal = booking_duration_hours * event.rate
        subtotal += extra_facility_cost

        tax_percentage = 0.15
        tax_amount = subtotal * tax_percentage

        total_price = subtotal + tax_amount

        if event and event_timings.available:
            booking = Booking(
                user_id=user.id,
                full_name=full_name,
                email=email,
                guest_count=guest_count,
                additional_notes=additional_notes,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                all_day=all_day,
                event_id=event_id,
                event_type=event_type
            )

            db.session.add(booking)
            db.session.flush()

            for facility in extra_facilities:
                facility_id = facility.get("extra_facility_id")
                unit_price_count = facility.get("unit_price_count")
                extra_facility_hours = facility.get("extra_facility_hours")
                apply_extra_facility_for_complete_event = facility.get("apply_extra_facility_for_complete_event")

                if facility_id:
                    selected_extra_facility = ExtraFacility.query.filter_by(id=facility_id, event_id=event_id).first()

                    if selected_extra_facility:
                        if unit_price_count is not None:
                            unit = "unit"
                            quantity = unit_price_count
                        elif apply_extra_facility_for_complete_event or extra_facility_hours is not None:
                            unit = "hour"
                            quantity = extra_facility_hours
                        else:
                            return jsonify({
                                "status": False,
                                "message": "Unit is not specified !!"
                            }), 404

                        booking_extra_facility = BookingExtraFacility(
                            booking_id=booking.id,
                            unit=unit,
                            extra_facility_id=facility_id,
                            quantity=quantity
                        )
                        db.session.add(booking_extra_facility)

            vendor = Vendor.query.filter_by(id=event.vendor_id).first()

            if vendor:
                vendor.wallet += subtotal
                db.session.commit()

            return jsonify({
                "status": True,
                "Summary": {
                    "event_hours": f"{booking_duration_hours} Hours",
                    "guest_count": f"{guest_count}",
                    "event_rate": f"{event.rate}$",
                    "subtotal": f"{subtotal}$",
                    "extra_facility_cost": f"{extra_facility_cost}",
                    "tax": f"{tax_amount}$ (15%)",
                    "total_price": f"{total_price} $"
                }
            }), 200

        else:
            return jsonify({
                "status": False,
                "message": f"{event.location_name} is not operating today !!"
            }), 400

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500


######################### STRIPE PAYMENT INTENT #########################



# @app.route("/create_payment_intent", methods = ["POST"])
# @jwt_required()
# def create_payment_intent():
#     try:
#         data = request.get_json()
#         user = get_current_user()
#         print(user)
#         amount = data.get("amount")  # amount in cent (amount should be multiplied with 100-- for 10.99 it should be 10.99 * 100)
#         currency = data.get("currency", "usd") ## default currency is set for usd
#         user_type = user.get("role")
#         user_id = user.get("id")

#         intent = stripe.PaymentIntent.create(
#             amount=amount * 100,
#             currency=currency,
#             payment_method_types=["card"],
#         )

#         transaction_amount = amount 
#         transaction_time = datetime.utcnow()
#         transaction_type = data.get("transaction_type")
#         trans_id = intent.id

#         transaction = Transaction(
#             user_id=user_id,
#             user_type=user_type,
#             transaction_amount=transaction_amount,
#             trans_id=trans_id,
#             transaction_time=transaction_time,
#             transaction_type=transaction_type
#         )

#         db.session.add(transaction)
#         db.session.commit()



#         print(intent.cleint_secret)
#         print(intent.id)

#         return jsonify({
#             "status": True,
#             "client_secret": intent.client_secret,
#             "transaction_id": transaction.id  
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status":False,
#             "error":str(e)
#         })


@app.route("/create_payment_intent", methods=["POST"])
@jwt_required()
def create_payment_intent():
    try:
        data = request.get_json()
        user = get_current_user()  # Assuming get_current_user() returns the current user object
        print(user)
        amount = data.get("amount")  # amount in cent (amount should be multiplied with 100-- for 10.99 it should be 10.99 * 100)
        currency = data.get("currency", "usd")  # default currency is set for usd
        user_type = user.role  # Accessing role attribute directly
        user_id = user.id  # Accessing id attribute directly

        intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency=currency,
            payment_method_types=["card"],
        )

        transaction_amount = amount 
        transaction_time = datetime.utcnow()
        transaction_type = data.get("transaction_type")
        trans_id = intent.id

        transaction = Transaction(
            user_id=user_id,
            user_type=user_type,
            transaction_amount=transaction_amount,
            trans_id=trans_id,
            transaction_time=transaction_time,
            transaction_type=transaction_type
        )

        db.session.add(transaction)
        db.session.commit()

        print(intent.client_secret)
        print(intent.id)

        return jsonify({
            "status": True,
            "client_secret": intent.client_secret,
            "transaction_id": transaction.id  
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "error": str(e)
        })




##########################################################################

def calculate_event_hours(start_date, end_date, start_time, end_time, all_day):
    # If it's an all-day event, set start_time and end_time accordingly
    if all_day:
        start_time = "00:00:00"
        end_time = "23:59:59"

    # Convert start and end dates/times to datetime objects
    start_datetime = convert_to_datetime(start_date, start_time)
    end_datetime = convert_to_datetime(end_date, end_time)

    # If it's an all-day event, set end_datetime to 23:59:59 of the end_date
    if all_day:
        end_datetime = datetime.combine(end_datetime.date(), datetime.max.time())

    # Calculate total event hours for the specified time duration
    total_hours_for_duration = calculate_hours_for_duration(start_datetime, end_datetime)

    # Calculate the number of days involved
    total_days_involved = calculate_days_involved(start_datetime, end_datetime)

    # Use the minimum of total_hours_for_duration and total_days_involved as event_hours
    event_hours = max(total_hours_for_duration, total_days_involved * 24)

    return event_hours


def convert_to_datetime(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")


def calculate_hours_for_duration(start_datetime, end_datetime):
    return (end_datetime - start_datetime).total_seconds() / 3600


def calculate_days_involved(start_datetime, end_datetime):
    return (end_datetime.date() - start_datetime.date()).days + 1




###############################     Upload Profile Image      ######################################


# remaining work : don't ask for email 

@app.route('/upload_profile_image', methods=["POST"])
@jwt_required()
def upload_profile_image():
    UPLOAD_FOLDER = 'images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    data = request.get_json()
    profile_image = data.get("profile_image")

    try:    
        user_email = get_jwt_identity()

        if not profile_image:
            return jsonify({"status":False,"message": "No profile image provided!!"}), 400

        image_bytes = base64.b64decode(profile_image)

        # If images directory dont exist then make it !!
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        original_extension = data.get("extension", "png")

        # Generate a new unique filename using a UUID
        filename = str(uuid.uuid4())

        # Combine the folder path and the filename with the original extension
        output_file_name = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.{original_extension}") # images / uuid name
        filename_path = f"{filename}.{original_extension}" # just uuid name

        with open(output_file_name, "wb") as output_file: # wb is write binary
            output_file.write(image_bytes)

        print(f"Image saved as {output_file_name}")

        # Assuming you have a User model and a database connection
        # Update the user's profile_image field with the new file path
        user = User.query.filter_by(email=user_email).first()
        if user:
            user.profile_image = filename_path
            db.session.commit()

        return jsonify({"status":True,"message": "Image uploaded successfully", "file_path": output_file_name}), 200

    except Exception as e:
        return jsonify({"status":False,"message": str(e)}), 500 
    
###############################     Update Profile Image      ######################################


@app.route('/update_profile_image', methods=["POST"])
@jwt_required()
def update_profile_image():
    UPLOAD_FOLDER = 'images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    data = request.get_json()
    profile_image = data.get("profile_image")
    
    try:
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if not profile_image:
            return jsonify({"status":False,"message": "No profile image provided!!"}), 400

        if user.profile_image:
            # Delete the old image file if it exists
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_image)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        image_bytes = base64.b64decode(profile_image)

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        original_extension = data.get("extension", "png")

        filename = str(uuid.uuid4())
        output_file_name = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.{original_extension}")
        filename_path = f"{filename}.{original_extension}"

        with open(output_file_name, "wb") as output_file:
            output_file.write(image_bytes)

        user.profile_image = filename_path
        db.session.commit()

        return jsonify({"status":True,"message": "Profile image updated successfully", "file_path": filename_path}), 200

    except Exception as e:
        return jsonify({"status":False,"message": str(e)}), 500

@app.route("/read_all_notification",methods=["GET"])
@jwt_required()
def read_all_noti():
    user = get_current_user()
    Notification.query.filter_by(user_id=user.id).update({"readed": True}, synchronize_session=False)
    db.session.commit()
    return jsonify({"status":True})

@app.route("/notification_count", methods=["GET"])
@jwt_required()
def notification_count():
    user = get_current_user()
    notifications = Notification.query.filter_by(user_id=user.id,readed=False).all()
    return jsonify({"status":True,"notification_count":len(notifications)})

@app.route("/get_notifications", methods=["GET"])
@jwt_required()
def get_notifiationsss():
    user = get_current_user()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.creation_date.desc()).all()
    notifications_data = []
    for event in notifications:
        notification_dict = event.as_dict()
        notifications_data.append(notification_dict)
    return jsonify({"status":True,"notifications":notifications_data})

@app.route("/create_not", methods=["GET"])
def create_not():
    notification = Notification(
            title="Booking",
            message="Your veneus is getting booked",
            message_type="booking",
            readed=False,
            user_id=2
        )
    db.session.add(notification)
    db.session.commit()
    return jsonify({"status":True})

@app.route("/contact_us", methods=["POST"])
def contact_us():
    data = request.get_json()
    email=data.get("email")
    message=data.get("message")
    name = data.get("name")
    try:
        msg = Message('CUSTOMER CONTACT', sender='noreply@gmail.com', recipients=["razorshariq@gmail.com"])
        msg.body = f"NAME: {name}, EMAIL:{email}, message: {message}"
        mail.send(msg)
        return jsonify({"status":True}),200
    except Exception as e:
        return jsonify({"status":False,"message":str(e)}), 500


##################### FAVORITES SECTION ####################


@app.route("/wishlist", methods = ["GET"])
@jwt_required()
def wishlist():
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401

    if user.role != "user":
        return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can add the favorite "
            })
    
    favorites = Favorites.query.filter_by(user_id = user.id).all()

    # coverting each instance of the data to dictionary with key value -- present in the model.py
    favorite_events = [fav.event.as_dict() for fav in favorites]

    return jsonify({
        "status":True,
        "favorite_events":favorite_events
    }), 200
    

@app.route("/add_to_favorites", methods = ["POST"])
@jwt_required()
def add_to_favorites():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401


    if user.role != "user":
        return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can create bookings."
            })
    
    event_id = data.get("event_id")
    favorites = Favorites.query.filter_by(user_id=user.id , event_id=event_id).first()
    if favorites:
        return jsonify({
            "status":False,
            "message":"Event is already in the favorite list"
        }), 403
    
    # user = User.query.filter_by(id = user.id).first_or_404()
    event = Event.query.get_or_404(event_id)

    favorite = Favorites(user_id = user.id, event_id = event.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "status":True,
        "message":"Successfully Added the event to favorites !!"
    }), 200



@app.route("/get_my_favorite_event", methods = ["POST"])
@jwt_required()
def get_my_favorite_event():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401
    
    if user.role != "user":
        return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can get the favorite events"
            })
    
    favorite_id = data.get("favorite_id")

    favorites = Favorites.query.filter_by(id = favorite_id ,user_id = user.id).first()

    if favorites:
        # coverting each instance of the data to dictionary with key value -- present in the model.py
        favorite_events = [favorites.event.as_dict()]

        return jsonify({
            "status":True,
            "favorite_events":favorite_events
        }), 200
    
    else:
        return jsonify({
            "status":False,
            "message":"Favorite id not found !"
        }), 404
    


@app.route("/update_my_favorite_event", methods = ["PUT"])
@jwt_required()
def update_my_favorite_event():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401
    
    if user.role != "user":
        return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can update the favorite events"
            })
    
    favorite_id = data.get("favorite_id")
    new_event_id = data.get("new_event_id")

    favorites = Favorites.query.filter_by(id = favorite_id ,user_id = user.id).first()

    if favorites:
        favorites.event_id = new_event_id
        db.session.commit()

        return jsonify({
            "status":True,
            "message":"Successfully updated the favorite event !"
        }), 200
    
    else:
        return jsonify({
            "status":False,
            "message":"Favorite event not found !!"
        }),404 



@app.route("/delete_my_favorite_event", methods = ["DELETE"])
@jwt_required()
def delete_my_favorite_event():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({ "status":False,"message": "User not found"}), 401
    
    if user.role != "user":
        return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can delete the favorite event."
            })
    
    # favorite_id = data.get("favorite_id")
    event_id = data.get("event_id")

    favorites = Favorites.query.filter_by(event_id=event_id ,user_id = user.id).first()

    if favorites:
        db.session.delete(favorites)
        db.session.commit()

        return jsonify({
            "status":True,
            "message":"Successfully deleted the favorite event !"
        }), 200
    
    else:
        return jsonify({
            "status":False,
            "message":"Favorite event not found !!"
        }),404 


##################### FAVORITES SECTION END #####################



###############################     Delete Profile Image      ######################################

# No need for delete profile as while updating the image with the new one it will automatically delete the new one

###############################     Get Profile Image      ######################################

@app.route('/get_profile_image', methods=["GET"])
@jwt_required()
def get_profile_image():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if user and user.profile_image:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_image)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
    
    return jsonify({"message": "Profile image not found"}), 404



# getting the image

@app.route('/images/<image_name>')
def serve_image(image_name):
    print("dssdfsfsfsdf")
    return send_from_directory('images', image_name)


###############################     Route For Reset Password      ######################################


@app.route('/reset_password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User Not Found !!'}), 404

    reset_token = secrets.token_urlsafe(32)
    reset_token_obj = PasswordResetToken(user_id=user.id, token=reset_token, expires_in_minutes=60)
    db.session.add(reset_token_obj)
    db.session.commit()

    reset_link = url_for('reset_password', token=reset_token, _external=True)
    msg = Message('Password Reset', sender='noreply@gmail.com', recipients=[user.email])
    msg.body = f"Click on the following link to reset the password: {reset_link}"
    try:
        mail.send(msg)
        return jsonify({"message": "Password Reset Email Sent !!"})
    except Exception as e:
        return jsonify({"message": f"Email sending failed: {str(e)}"}), 500
    


###############################     Route For Reset Password After Getting Token      ######################################

@app.route("/forget_password", methods=["POST"])
def forgetPassword():
    data = request.get_json()
    user = data.get("email")
    user_update = User.query.filter_by(email=user).first()
    print(user, )
    if user_update==None:
        return jsonify({"status":False,"message":"Cannot find user with this email address"})
    else:
        try:
            gen_otp = ''.join(random.choices(string.digits, k=4))
            msg = Message('Password Reset', sender='noreply@gmail.com', recipients=[user])
            msg.body = f"Use the verification code reset the password OTP: {gen_otp}"
            mail.send(msg)
            user_update.otp = gen_otp
            db.session.commit()
            return jsonify({"message": "Password Reset Email Sent !!","status":True})
        except Exception as e:
            return jsonify({"message": f"Email sending failed: {str(e)}","status":False}), 500


@app.route('/forget_password_reset', methods=['POST'])
@jwt_required()
def frget_reset_password():
    user_d = get_current_user()
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    print(new_password,confirm_password)
    user = User.query.filter_by(email=user_d.email).first()
    if user.check_password(new_password):
        return jsonify({"status":False,"message":"same_password"})
    password_validation_result = Validations.is_valid_password(new_password)

    if new_password != confirm_password:
        return jsonify({
            "status":False,
            "message": "Password did not match."
        }), 400
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    return jsonify({"status":True,'message': 'Password reset successfully'}), 200

@app.route('/password_reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    current_password = data.get('current_password')
    email = data.get('email')
    print(new_password,confirm_password,current_password)
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(current_password):
        return jsonify({"status":False,'message': 'Invalid credentials'}), 401
    
    if user.check_password(new_password):
        return jsonify({"status":False,"message":"same_password"})



    password_validation_result = Validations.is_valid_password(new_password)

    if new_password != confirm_password:
        return jsonify({
            "status":False,
            "message": "Password did not match."
        }), 400
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    return jsonify({"status":True,'message': 'Password reset successfully'}), 200


# @app.route('/reset_password/<token>', methods=['POST'])
# def reset_password(token):
#     data = request.get_json()
#     new_password = data.get('new_password')
#     confirm_password = data.get('confirm_password')

#     password_validation_result = Validations.is_valid_password(new_password)

#     if new_password != confirm_password:
#         return jsonify({
#             "status":False,
#             "message": "Password did not match."
#         }), 400
    

#     reset_token_obj = PasswordResetToken.query.filter_by(token=token).first()
#     if not reset_token_obj:
#         return jsonify({"status":False,'message': 'Invalid reset token'}), 400

#     if reset_token_obj.expired_at < datetime.utcnow():
#         return jsonify({"status":False,'message': 'Reset token has expired'}), 400

#     user = User.query.get(reset_token_obj.user_id)
#     user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
#     db.session.delete(reset_token_obj)
#     db.session.commit()

#     return jsonify({"status":True,'message': 'Password reset successfully'}), 200


if __name__ == '__main__':
    app.run(debug=False,use_reloader=False)

