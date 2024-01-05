from sqlalchemy import func, or_, and_ 
from sqlalchemy.orm import joinedload
from utils import Validations, Ratings, DateTimeConversions, BookingAvailability, Filterations, BookingCount, Notification
from random import sample 
from geopy.distance import geodesic
from app import app, db, mail
from flask import request, jsonify, url_for, current_app, send_file, send_from_directory
from datetime import datetime, timedelta
from model import User, PasswordResetToken, Vendor, Event, Booking , Review, Preferences, Favorites
import secrets
from sqlalchemy.exc import IntegrityError
import uuid
import base64
from flask_mail import Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from model import bcrypt   
from werkzeug.utils import secure_filename
import os


import sys
sys.dont_write_bytecode = True

###############################     Route For SignUp     ######################################


@app.route('/signup', methods=['POST'])  # Updated route
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
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

        user = User(email=email, password=password, role=role)  # Pass the role during user creation

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
        return jsonify({"status":False,"message":"errro"})

###############################     Route For SignIn      ######################################


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"status":False,'message': 'Invalid credentials'}), 401

    if not user.role:  # This line is not necessary, as 'role' should always be present due to your database model
        return jsonify({"status":False,"message": "Please specify if you are signing in as a user or a vendor"}), 400

    # Generate the access token
    access_token = create_access_token(identity=email)

    # Update the user's access_token column with the new access token
    user.access_token = access_token
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


###############################     Route For Security In The Internal App      ######################################


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

###############################    Complete Vendor Profile        ######################################


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


@app.route("/create_event", methods=["POST"])
@jwt_required()
def create_event():
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
    print(thumbnail)
    other_images = data.get("other_images")
    video_showcase = data.get("video_showcase")
    location_name = data.get("location_name")
    address = data.get("address")
    rate = data.get("rate")
    fixed_price = data.get("fixed_price")

    # Additional fields
    details = data.get("details")
    services = data.get("services")
    print(services)

    facilities = data.get("facilities")
    description = data.get("description")
    event_type = data.get("event_type")
    latitude=   data.get("latitude")
    longitude = data.get("longitude")

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
        services=services,
        facilities=facilities,
        description=description,
        event_type=event_type,
        latitude=latitude,
        longitude=longitude,
        vendor=vendor  # Associate the event with the vendor
    )

    # Handle thumbnail image if provided
    if thumbnail:
        thumbnail_filename = f"{uuid.uuid4()}.png"
        thumbnail_path = os.path.join(app.config['VENDOR_IMAGES_FOLDER'], thumbnail_filename)
        save_image_from_base64(thumbnail, thumbnail_path)
        event.thumbnail = thumbnail_filename

    # Handle other images if provided
    if other_images:
        event.other_images = save_multiple_images_from_base64(other_images)

    if facilities:
        event.facilities = save_multiple_images_from_base64(facilities)

    db.session.add(event)  # Add the event to the session
    db.session.commit()  # Commit the transaction

    return jsonify({"status":True,"message": "Event created successfully"})


###############################     Get My Events     ######################################

# @app.route("/get_my_events", methods=["GET"])
# @jwt_required()
# def getmyevents():
#     try:
#         user = get_current_user()
#         vendor = user.vendor
#         events = Event.query.filter_by(vendor=vendor).all()
#         print(events,"ll")
#         events_data = []

#         for event in events:
#             event_dict = event.as_dict()
#             event_dict['total_bookings'] = event.get_total_bookings()
#             event_dict['total_bookings_value'] = event.earnings_per_month()  # Total earnings for the current month
#             event_dict["event_icon"] = booking.event_icon
#             events_data.append(event_dict)

#         return jsonify({"status": True, "events": events_data})
#     except Exception as e:
#         print(e)
#         return jsonify({"status": False, "events": []})


# @app.route("/get_my_events", methods=["GET"])
# @jwt_required()
# def getmyevents():
#     try:
#         user = get_current_user()
#         vendor = user.vendor
#         print(vendor)
#         events = Event.query.filter_by(vendor=vendor).all()
#         print(events, "ll")
#         events_data = []

#         for event in events:
#             event_dict = event.as_dict()
#             event_dict['total_bookings'] = event.get_total_bookings()
#             event_dict['total_bookings_value'] = event.earnings_per_month()  # Total earnings for the current month

#             events_data.append(event_dict)

#         return jsonify({"status": True, "events": events_data})
#     except Exception as e:
#         print(e)
#         return jsonify({"status": False, "events": []})


@app.route("/get_my_events", methods=["GET"])
@jwt_required()
def getmyevents():
    try:
        user = get_current_user()
        vendor = user.vendor
        events = Event.query.filter_by(vendor=vendor).all()
        events_data = []

        for event in events:
            event_dict = event.as_dict()
            event_dict['total_bookings'] = event.get_total_bookings()
            event_dict['total_bookings_value'] = event.earnings_per_month()  # Total earnings for the current month

            # Replace event_type with the event_type from Booking
            event_dict['event_type'] = event.bookings[0].event_type if event.bookings else None

            events_data.append(event_dict)

        return jsonify({"status": True, "events": events_data})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "events": []})


###############################     Update My Event     ######################################


@app.route("/update_event/<int:event_id>", methods = ["PUT"])
@jwt_required()
def update_event(event_id):
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
    event.rate = data.get("rate", event.rate)
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


###############################     Delete Event     ######################################



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

        db.session.delete(event)
        db.session.commit()
        return jsonify({
        "status":True,
        "message":"Event Deleted Successfully !!!"
        })
    except Exception as e:
        print(e)
        return jsonify({
        "status":False,
        "message":"booking"
        })



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

    if not user:
            return jsonify({
                "status":False,
                "message": "User not authenticated !!"
            }), 401
            
    if user.role != "user":
            return jsonify({
                "status": False,
                "message": "Unauthorized access: Only users can get events."
            })
    event = Event.query.get(event_id) 
    
    if event:
        event_details = {
            "id": event.id,
            "thumbnail": event.thumbnail,
            "other_images": event.other_images,
            "video_showcase": event.video_showcase,
            "address": event.address,
            "rate": event.rate,
            "fixed_price": event.fixed_price,
            "details": event.details,
            "services": event.services,
            "facilities": event.facilities,
            "description": event.description,
            "event_type": event.event_type,
            "vendor_id": event.vendor_id,  # You can include vendor details if needed
            "location_name":event.location_name,
            "longitude":event.longitude,
            "latitude":event.latitude,
            "event_icon":event.event_icon
        }
        # Fetch vendor details
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
                # Include other vendor fields as necessary
            }

            event_details['vendor_details'] = vendor_details
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


###############################     Search Events API        ######################################

@app.route("/top_venues/<int:vendor_id>", methods=["GET"])
def top_venues(vendor_id):
    try:
        total_bookings = (db.session.query(func.count(Booking.id))
                        .join(Event)
                        .filter(Event.vendor_id == vendor_id)
                        .scalar())

        venue_bookings = (db.session.query(
                                Event.location_name,
                                Event.thumbnail,
                                func.count(Booking.id).label('booking_count'),
                                Booking.event_icon
                            )
                            .join(Booking, Event.id == Booking.event_id)
                            .filter(Event.vendor_id == vendor_id)
                            .group_by(Event.location_name, Event.thumbnail, Booking.event_icon)
                            .order_by(func.count(Booking.id).desc())
                            .all()
                        )

        venues_list = []

        for location_name, thumbnail, count, event_icon in venue_bookings:
            percentage = (count / total_bookings) * 100 if total_bookings > 0 else 0
            venues_list.append({
                "venue": location_name,
                "thumbnail": thumbnail,
                "bookings": count,
                "percentage": round(percentage, 2),
                "event_icon": event_icon
            })

        return jsonify({"status": True, "top_venues": venues_list})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "error": str(e)})



@app.route("/bookings_today/<int:vendor_id>", methods=["GET"])
@jwt_required()
def bookings_today(vendor_id):
    try:
        today = datetime.now().date()
        bookings = Booking.query.join(Event, Booking.event_id == Event.id)\
                                .filter(Event.vendor_id == vendor_id)\
                                .filter(Booking.start_date <= today, Booking.end_date >= today)\
                                .all()

        bookings_data = [booking.booking_today() for booking in bookings]
        return jsonify({"status": True, "bookings": bookings_data})
    except Exception as e:
        print(e)
        return jsonify({"status": False, "error": str(e)})



######################### Event Preferences #################### 

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

        if not user_preference:
            user_preference = Preferences(user_id=user.id , event_preference=event_preference, vendor_preference=vendor_preference)
            db.session.add(user_preference)
        else:
            user_preference.event_preference = event_preference
            user_preference.vendor_preference = vendor_preference

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



################### Home Events ###############################


# corrected home_events
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
        max_distance = 3

        event_types = Event.query.with_entities(Event.event_type).distinct().all()

        events_by_types = {}
        for event_type in event_types:
            events = (
                Event.query.join(Event.vendor)
                    .join(Vendor.user)
                    .filter(Event.event_type == event_type[0])
                    .order_by(func.random())
                    .limit(15)
                    .all()
            )

            events_data = []
            for event in events:
                current_date_time = datetime.now()

                if requested_availability:
                    is_event_available = any(
                        BookingAvailability.check_availability(booking, current_date_time)
                        for booking in event.bookings
                        if not booking.all_day
                    )

                    if not is_event_available:
                        continue

                # Check the condition from Booking table before adding to the response
                if any(booking.all_day for booking in event.bookings):
                    continue  # Skip this event if the condition is met

                # Calculate total bookings
                # total_bookings = sum(1 for booking in event.bookings)
                total_bookings = sum(1 for booking in event.bookings)

                serialized_event = {
                    "event_id": event.id,
                    "vendor_id": event.vendor_id,
                    "event_type": event.event_type,
                    "event_rate": event.rate,
                    "event_address": event.address,
                    "event_latitude":event.latitude,
                    "event_longitude":event.longitude,
                    "event_ratings": Ratings.get_average_rating(event.id),
                    "total_bookings": total_bookings  # Include total bookings in the response
                    # Add other necessary event details
                }
                events_data.append(serialized_event)

            prefered_filter = data.get("prefered_filter")
            if prefered_filter:
                events_data = Filterations.apply_filters(events_data, prefered_filter, user_location, max_distance)

            else:
                continue
            
            events_by_types[event_type[0]] = events_data

        return jsonify({
            "status": True,
            "events_by_events_types": events_by_types
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500

##################################################            Favorites             #############################################################
    
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
    # user = User.query.filter_by(id = user.id).first_or_404()
    event = Event.query.get_or_404(event_id)
    
    favorite = Favorites(user_id = user.id, event_id = event.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "status":True,
        "message":"Successfully Added the event to favorites !!"
    }), 200


    
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

    # coverting each instance of the data to dictionary with key value -- present in the model.py
    favorite_events = [favorites.event.as_dict()]

    return jsonify({
        "status":True,
        "favorite_events":favorite_events
    }), 200
    



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
    
    favorite_id = data.get("favorite_id")

    favorites = Favorites.query.filter_by(id = favorite_id ,user_id = user.id).first()

    if favorites:
        db.session.delete(favorites)
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





################### Search Event ###############################

# ################### Custom Event Search ###########################

@app.route("/search_event", methods=["POST"])
@jwt_required()
def search_event():
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
    event_list = []

    for result in paginated_results:
        event = result[0]
        within_radius = result[1]

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
            "vendor_details": vendor_details
        }
        event_list.append(event_info)

    return jsonify({
        "status": True,
        "Total_Events": total_events_found,
        "Events": event_list
    }), 200



@app.route("/custom_event_search", methods=["POST"])
@jwt_required()
def custom_event_search():
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
            (Booking.end_time >= start_time)
        ).distinct()

        query = query.filter(~Event.id.in_(subquery))

    results = query.all()
    user_location = (latitude, longitude)
    results_with_distance = []

    for event in results:
        if event.latitude is not None and event.longitude is not None:
            event_location = (event.latitude, event.longitude)
            distance = geodesic(event_location, user_location).kilometers <= 3
            results_with_distance.append((event, distance))

    sorted_results = sorted(results_with_distance, key=lambda x: Ratings.get_average_rating(x[0].id), reverse=True)

    serialized_results = []

    for event_tuple in sorted_results:
        event = event_tuple[0]
        vendor_details = []

        if event.latitude is not None and event.longitude is not None:
            event_location = (event.latitude, event.longitude)
            distance = geodesic(event_location, user_location).kilometers <= 3

            if distance:
                vendor_profile_image = event.vendor.user[0].profile_image  # Assuming only one user for the vendor

                serialized_event = {
                    "id": event.id,
                    "thumbnail": event.thumbnail,
                    "event_type": event.event_type,
                    "rate": event.rate,
                    "event_rating": Ratings.get_average_rating(event.id),
                    "fixed_price": event.fixed_price,
                    "distance_km": geodesic(event_location, user_location).kilometers,
                    "address": event.vendor.location,  # Modify as per the actual address field in your model
                    "custom_event_name": event.location_name,  # Modify as per the actual field name
                    "vendor_details": {
                        "vendor_profile_image": vendor_profile_image,
                        "vendor_id": event.vendor.id
                    }
                }
                serialized_results.append(serialized_event)

    return jsonify({
        "status": True,
        "Search Result Found": f"{len(serialized_results)} vendors found for {location_name} with {ratings} star rating",
        "Search results": serialized_results
    })







###############################   Create Booking      #####################################

# @app.route('/send_notification', methods=['POST'])
# def send_notification():
#     data = request.get_json()
#     device_token = data.get("device_token")
#     title = data.get("title")
#     body = data.get("body")

#     if not all([device_token, title, body]):
#         return jsonify({
#             "status": False,
#             "message": "Missing parameters !!"
#         }), 400
    
#     success = Notification.send_push_notification(device_token, title, body)

#     if success:
#         return jsonify({
#             "status": True,
#             "message": "Message sent successfully!!"
#         }), 200
#     else:
#         return jsonify({
#             "status": False,
#             "message": "Failed to send notifications !!"
#         }), 500




###############################   Create Booking      ######################################

@app.route('/create_booking', methods=["POST"])
@jwt_required()
def create_booking():
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

        if not all([full_name, email, guest_count, start_date, end_date, event_id,event_type]):
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
        event_hours = DateTimeConversions.calculate_event_hours(start_date, end_date, start_time, end_time, all_day)

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

        # if event_type:
        #     event_icon_filename = f"{event_type.lower()}_icon_{uuid.uuid4()}.png"
        #     event_icon_path = os.path.join(app.config["EVENT_ICON_FOLDER"], event_icon_filename)
        #     if os.path.exists(event_icon_path):
        #         booking.event_icon = event_icon_filename

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
            # event_icon = event_icon_filename
        )


        db.session.add(booking)
        db.session.commit()

        return jsonify({
            "status":True,
            "Summary": {
                "event_hours": f"{event_hours} Hours",
                "guest_count": f"{guest_count}",
                "event_rate": f"{event.rate}$",
                "subtotal": f"{subtotal}$",
                "tax": "15%",
                "total_price": f"{total_price} $"
            }
        })

    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500




###############################   Upload Event Icon   ######################################

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





###############################    Cancel Booking By User      ######################################

# @app.route("/cancel_booking", methods = ["POST"])
# @jwt_required()
# def cancel_booking():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status":False,
#                 "message": "User not authenticated !!"
#             }), 401
            
#         if user.role != "user":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only users can cancel bookings."
#             })

#         booking_id = data.get("booking_id")

#         booking_to_cancel = Booking.query.filter_by(id=booking_id, user_id = user.id).first()

#         if not booking_to_cancel:
#             return jsonify({
#                 "message":"Booking not found"
#             })
        
#         booking_to_cancel.cancelled = True  
#         db.session.commit()

#         return jsonify({
#             "status":True,
#             "message":"Booking cancelled successfully !!",
#             "event_id":Booking.event_id,
#             # "event_icon":Booking.even,
#             "vendor_id":Booking.event.vendor.id
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status":False,
#             "message": str(e)
#         }), 500


###############################    Cancel Booking By Vendor      ######################################


# @app.route("/cancel_booking_by_vendor", methods = ["POST"])
# @jwt_required()
# def cancel_booking_by_vendor():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status":False,
#                 "message": "User not authenticated !!"
#             }), 401
            
#         if user.role != "vendor":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only vendors can cancel bookings."
#             })
        
#         booking_id = data.get("booking_id")

#         booking_to_cancel = Booking.query.filter_by(id=booking_id).first()

#         if booking_to_cancel.cancelled == 1:
#             return jsonify({
#                 "message":"Booking is already cancelled !1"
#         })

#         if not booking_to_cancel or booking_to_cancel.event.vendor.id != user.vendor.id:
#             return jsonify({
#                 "message":"Booking not found or unauthorized to cancel"})

#         booking_to_cancel.cancelled = True  
#         db.session.commit()

#         return jsonify({
#             "status":True,
#             "message":"Successfully cancelled the booking !!",
#             "event_id":booking_to_cancel.event_id,
#             "vendor_id":booking_to_cancel.event.vendor.id
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status":False,
#             "message": str(e)
#         }), 500




###############################    Cancel Booking By User      ######################################

# @app.route("/cancel_booking", methods = ["POST"])
# @jwt_required()
# def cancel_booking():
#     try:
#         data = request.get_json()
#         user = get_current_user()

#         if not user:
#             return jsonify({
#                 "status":False,
#                 "message": "User not authenticated !!"
#             }), 401
            
#         if user.role != "user":
#             return jsonify({
#                 "status": False,
#                 "message": "Unauthorized access: Only users can cancel bookings."
#             })

#         booking_id = data.get("booking_id")

#         booking_to_cancel = Booking.query.filter_by(id=booking_id, user_id = user.id).first()

#         if not booking_to_cancel:
#             return jsonify({
#                 "message":"Booking not found"
#             })
        
#         booking_to_cancel.cancelled = True  
#         db.session.commit()

#         return jsonify({
#             "status":True,
#             "message":"Booking cancelled successfully !!",
#             "event_id":Booking.event_id,
#             # "event_icon":Booking.even,
#             "vendor_id":Booking.event.vendor.id
#         })
    
#     except Exception as e:
#         return jsonify({
#             "status":False,
#             "message": str(e)
#         }), 500


@app.route("/cancel_booking", methods=["POST"])
@jwt_required()
def cancel_booking():
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
                "message": "Unauthorized access: Only users can cancel bookings."
            })

        booking_id = data.get("booking_id")

        booking_to_cancel = Booking.query.filter_by(id=booking_id, user_id=user.id).first()

        if not booking_to_cancel:
            return jsonify({
                "status": False,
                "message": "Booking not found"
            }), 404

        # Check if the booking is already canceled
        if booking_to_cancel.cancelled:
            return jsonify({
                "status": False,
                "message": "Booking is already canceled"
            }), 400

        booking_to_cancel.cancelled = True
        db.session.commit()

        # Notification Data for Cancellation
        send_notification_data = {
            "device_token": "<YOUR_DEVICE_TOKEN_HERE>",
            "title": "Booking Canceled by User",
            "body": "Your booking has been canceled"
        }

        # Send Notification
        send_notification_response = Notification.send_notification(send_notification_data)

        if send_notification_response:
            notification_status = "Notification sent successfully"
        else:
            notification_status = "Failed to send notification"

        return jsonify({
            "status": True,
            "message": "Booking cancelled successfully !!",
            "event_id": booking_to_cancel.event_id,
            # "event_icon": Booking.event.icon,  # Add the necessary field here
            "vendor_id": booking_to_cancel.event.vendor.id,
            "notification_status": notification_status
        }), 200

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500


###############################    Cancel Booking By Vendor      ######################################


@app.route("/cancel_booking_by_vendor", methods=["POST"])
@jwt_required()
def cancel_booking_by_vendor():
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
                "message": "Unauthorized access: Only vendors can cancel bookings."
            }), 403
        
        booking_id = data.get("booking_id")

        booking_to_cancel = Booking.query.filter_by(id=booking_id).first()

        if booking_to_cancel.cancelled == 1:
            return jsonify({
                "status": False,
                "message": "Booking is already cancelled!"
            }), 400

        if not booking_to_cancel or booking_to_cancel.event.vendor.id != user.vendor.id:
            return jsonify({
                "status": False,
                "message": "Booking not found or unauthorized to cancel"
            }), 404

        booking_to_cancel.cancelled = True  

        send_notification_data = {
            "device_token": "emjWuhv2Tqa9R5k867wLUE:APA91bGx1TkzLVNpz2UfA_FOqOMVCZWaFEOMjPbUGsT0_1Mnhn9Rj8zAsBC77efdtQUZ9OzZj3D1FJvl3wlqtdIS5f7ABJF2BNkL9fP8wnqnxkKtI3BWPKQIq_hQpuKh81E9zQXBWCim",
            "title": "Booking Canceled by Vendor",
            "body": "Booking has been canceled by the vendor"
        }

        send_notification_response = Notification.send_notification(send_notification_data)

        db.session.commit()

        if send_notification_response:
            return jsonify({
                "status": True,
                "message": "Booking canceled by vendor and notification sent successfully!!",
                "event_id": booking_to_cancel.event_id,
                "vendor_id": booking_to_cancel.event.vendor.id
            }), 200
        else:
            return jsonify({
                "status": False,
                "message": "Failed to send notification after canceling the booking by vendor!!"
            }), 500

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        }), 500

###############################   Vendor's Events      ######################################


# calender
# Bookings
# Events taking place 

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
            (~Booking.cancelled)
        ).all()

        events_on_date_dict = []
        for booking in events_on_date:
            events_dict = {
                "location_name":booking.event.location_name,
                "event_thumbnail":booking.event.thumbnail,
                "booking_event_type":booking.event_type,
                # "event_icon":booking.event_icon,
                "booking_id":booking.id,
                "user_profile_image":booking.user.profile_image,
                # "other_details":booking.as_dict()
            }
            # print(booking.as_dict())

            events_on_date_dict.append(events_dict)


        events_after_date_dict = []
        for booking in events_for_month_afterwards:
            events_dict = {
                "location_name":booking.event.location_name,
                "event_thumbnail":booking.event.thumbnail,
                "event_icon":booking.event_icon,
                "booking_event_type":booking.event_type,
                "booking_id":booking.id,
                "user_profile_image":booking.user.profile_image,
                # "other_details":booking.as_dict()
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
            }), 401
            
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
                "event_thumbnail": booking.event.thumbnail,
                # "event_icon":booking.event_icon,
                "event_type":booking.event.event_type,
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
        }), 200

    except Exception as e:
        return jsonify({
            "status":False,
            "message": str(e)
        }), 500


###############################################################     Reviews Section      ###############################################################



##############################     Submit Review      ####################################


@app.route("/submit_review", methods=["POST"])
@jwt_required()
def submit_review():
    data = request.get_json()
    user = get_current_user()

    if user.role != "user":
        return jsonify({
            "status": False,
            "message": "Unauthorized access: Only users can submit reviews."
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
        return jsonify({"message": "Booking Does Not Exist!"}), 400

    # Check if the booking belongs to the authenticated user
    if booking.user_id != user.id:
        return jsonify({"message": "Unauthorized: You can only review your own bookings!"}), 403

    booking_end_time = datetime.combine(booking.end_date, booking.end_time)

    if datetime.utcnow() >= booking_end_time:
        user_email = get_jwt_identity()  # Assuming get_jwt_identity() returns email
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({"message": "User not found!"}), 401

        existing_review = Review.query.filter_by(booking_id=booking_id, user_id=user.id).first()

        if existing_review:
            return jsonify({"message": "You have already reviewed this event!"}), 400

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
                "message": "Successfully reviewed !!"
            }), 200

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "message": f"You have already reviewed this event !! {str(e)}"
            }), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": f"Failed to rate {str(e)}"
            }), 500

    else:
        return jsonify({"message": "Booking has not been completed yet. Can't rate the event now."}), 400

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
                    location_name = event.location_name if event.location_name else "Unknown Custom Event Name"

                    pending_reviews_info.append({
                        "booking_id":booking.id,
                        "location_name":booking.event.location_name,
                        # "event_icon":booking.event_icon,
                        "event_id": event.id,
                        "event_rate": event_rate,
                        "event_type": event_type,
                        "event_address": event_address,
                        "event_thumbnail": event_thumbnail,
                        # "custom_event_name": custom_event_name,
                        "booking_date": booking.start_date.isoformat(), # date format in georgian calender
                        "booking_time": booking.start_time.isoformat(),
                        "event_type":booking.event_type,
                    })

        return jsonify({
            "Pending Reviews": pending_reviews_info,
            "Pending Reviews Length": len(pending_reviews_info)
        })

    except Exception as e:
        print(f"Error fetching pending reviews: {str(e)}")
        return jsonify({"error": "An error occurred while fetching pending reviews."}), 500


##############################     All Rated Reviews      ####################################


# @app.route('/all_reviews', methods=["GET"])
# @jwt_required()
# def all_reviews():
#     try:
#         email = get_jwt_identity()
#         user = User.query.filter_by(email=email).first()

#         if user.role == "user":
#             # Fetch all reviews given by the user
#             reviews = (
#                 db.session.query(Review, Event, Vendor)
#                 .join(Event, Review.event_id == Event.id)
#                 .join(Vendor, Event.vendor_id == Vendor.id)
#                 .filter(Review.user_id == user.id)
#                 .all()
#             )
#         elif user.role == "vendor":
#             reviews = (
#                 db.session.query(Review, Event, Vendor)
#                 .join(Event, Review.event_id == Event.id)
#                 .join(Vendor, Event.vendor_id == Vendor.id)
#                 .filter(Event.vendor_id == user.vendor_id)
#                 .all()
#             )
#         else:
#             return jsonify({"message": "Invalid user role."}), 400

#         if not reviews:
#             return jsonify({"message": "Reviews Not Found !!"}), 400

#         review_data = []

#         for review, event, vendor in reviews:
#             vendor_user = User.query.filter_by(vendor_id=vendor.id).first()
#             vendor_profile_image = getattr(vendor_user, 'profile_image', None)
#             review_user = User.query.get(review.user_id)
#             user_profile_image = getattr(review_user ,"profile_image", None)
#             print(review_user)

#             # Fetch all bookings for this event
#             bookings = Booking.query.filter_by(event_id=event.id).all()

#             # Calculate total amount earned for the event
#             total_amount = 0
#             for booking in bookings:
#                 # Calculate event hours for each booking
#                 event_hours = DateTimeConversions.calculate_event_hours(
#                     booking.start_date, booking.end_date,
#                     booking.start_time, booking.end_time,
#                     booking.all_day
#                 )

#                 subtotal = event.rate * event_hours
#                 print(f"Subtotal : {subtotal}")
#                 tax_percentage = 0.15
#                 tax_amount = subtotal * tax_percentage
#                 print(f"tax amount : {tax_amount}")
#                 total_price = subtotal + tax_amount
#                 total_amount += total_price
#                 print(f"Total amount : {total_amount}")

#                 print(total_amount)

#             review_data.append({
#                 "event_id": event.id,
#                 "event_thumbnail": event.thumbnail,
#                 "event_name": event.location_name,
#                 "event_rate": event.rate,
#                 "total_event_hours": event_hours,
#                 "total_amount_earned_by_the_vendor": total_amount,
#                 "tax_amount": tax_amount, 
#                 "event_address": event.address,
#                 "user_profile_image":user_profile_image,
#                 # "event_icon": booking.event_icon,
#                 "vendor_profile_image": vendor_profile_image,
#                 "user_review": review.user_review,
#                 "cleanliness_rating": review.cleanliness_rating,
#                 "price_value_rating": review.price_value_rating,
#                 "service_value_rating": review.service_value_rating,
#                 "location_rating": review.location_rating
#             })

#         return jsonify({
#             "rated_reviews": review_data,
#             "total_rated_reviews": len(review_data)
#         })
    
#     except Exception as e:
#         print(f"Error in fetching rated reviews: {str(e)}")
#         return jsonify({"error": "An error occurred while fetching rated reviews."}), 500


@app.route('/all_reviews', methods=["GET"])
@jwt_required()
def all_reviews():
    try:
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if user.role == "user":
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
            return jsonify({"message": "Reviews Not Found !!"}), 400

        review_data = []

        for review, event, vendor in reviews:
            vendor_user = User.query.filter_by(vendor_id=vendor.id).first()
            vendor_profile_image = getattr(vendor_user, 'profile_image', None)
            review_user = User.query.get(review.user_id)
            user_profile_image = getattr(review_user, "profile_image", None)

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
                tax_percentage = 0.15
                tax_amount = subtotal * tax_percentage
                total_price = subtotal + tax_amount
                total_amount += total_price

            review_data.append({
                "event_id": event.id,
                "event_thumbnail": event.thumbnail,
                "event_name": event.location_name,
                "event_rate": event.rate,
                "total_event_hours": event_hours,
                "total_amount_earned_by_the_vendor": total_amount,
                "tax_amount": tax_amount,
                "event_address": event.address,
                "user_profile_image": user_profile_image,
                "vendor_profile_image": vendor_profile_image,
                "user_review": review.user_review,
                "cleanliness_rating": review.cleanliness_rating,
                "price_value_rating": review.price_value_rating,
                "service_value_rating": review.service_value_rating,
                "location_rating": review.location_rating,
                # Update event_type to fetch from Booking table
                "event_type": bookings[0].event_type if bookings else None
            })

        return jsonify({
            "rated_reviews": review_data,
            "total_rated_reviews": len(review_data)
        })

    except Exception as e:
        print(f"Error in fetching rated reviews: {str(e)}")
        return jsonify({"error": "An error occurred while fetching rated reviews."}), 500



###############################     Upload Profile Image      ######################################

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
            return send_file(file_path)
    
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

# @app.route('/password_reset', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     new_password = data.get('new_password')
#     confirm_password = data.get('confirm_password')
#     current_password = data.get('current_password')
#     email = data.get('email')
#     print(new_password,confirm_password,current_password)
#     user = User.query.filter_by(email=email).first()

#     if not user or not user.check_password(current_password):
#         return jsonify({"status":False,'message': 'Invalid credentials'}), 401
    
#     if user.check_password(new_password):
#         return jsonify({"status":False,"message":"same_password"})



#     password_validation_result = Validations.is_valid_password(new_password)

#     if new_password != confirm_password:
#         return jsonify({
#             "status":False,
#             "message": "Password did not match."
#         }), 400
#     user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
#     db.session.commit()
#     return jsonify({"status":True,'message': 'Password reset successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)

