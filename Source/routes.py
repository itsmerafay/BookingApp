import re
import random
from sqlalchemy import func
from validations import Validations
from app import app, db, mail
from flask import request, jsonify, url_for, current_app, send_file, send_from_directory
from datetime import datetime
from models import User, PasswordResetToken, Vendor, Event, Booking 
import secrets
import io
import colorama
import uuid
import base64
from flask_mail import Message
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from models import bcrypt   
from werkzeug.utils import secure_filename
import os

import sys
sys.dont_write_bytecode = True

###############################     Route For SignUp     ######################################


@app.route('/signup', methods=['POST'])  # Updated route
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # Get the user's role from the request

    # Validate email and password using your Validations class
    email_validation_result = Validations.is_valid_email(email)
    password_validation_result = Validations.is_valid_password(password)

    if email_validation_result is None:
        return jsonify({"message": "Invalid Email Address"}), 400

    if password_validation_result is not None:
        return password_validation_result, 400 # json response result according to the error

    if not email or not password or not role:
        return jsonify({'message': 'Email, password, and role are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    if role not in ['user', 'vendor']:
        return jsonify({"message": "Invalid Role"}), 400

    user = User(email=email, password=password, role=role)  # Pass the role during user creation
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered Successfully !!"})






###############################     Route For SignIn      ######################################




@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    if not user.role:
        return jsonify({"message": "Please specify if you are signing in as a user or a vendor"}), 400

    # Generate the access token
    access_token = create_access_token(identity=email)

    # Update the user's access_token column with the new access token
    user.access_token = access_token
    db.session.commit()

    return jsonify({
        "access_token": access_token,
        "message": "Successfully Logged In !!"
    })









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
        return jsonify({"message": "This route is protected and accessible to authenticated users"})
    else:
        return jsonify({"message": "Authentication failed"}), 401





###############################     Route For Vendor Profile Complete       ######################################


@app.route('/complete_vendor_profile', methods=["POST"])
@jwt_required()
def complete_vendor_profile():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({"message": "User not found"}), 401

    if user.role != "vendor":
        return jsonify({"message": "User Auth Error, not a vendor"}), 401

    full_name = data.get("full_name")
    phone_number = data.get("phone_number")
    location = data.get("location")
    biography = data.get("biography")

    if not all([full_name, phone_number, location, biography]):
        return jsonify({"message": "All fields are required for the vendor profile"}), 400

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
        return jsonify({"message": "Vendor profile created successfully"})
    
    # else update the existing
    else:
        vendor.full_name = full_name
        vendor.phone_number = phone_number
        vendor.location = location
        vendor.biography = biography
        db.session.commit()
        return jsonify({"message": "Vendor profile completed successfully"})
    



VENDOR_IMAGES_FOLDER = 'images'
app.config["VENDOR_IMAGES_FOLDER"] = VENDOR_IMAGES_FOLDER




###############################     Route For Event Management      ######################################



# @app.route('/complete_vendor_profile_2', methods=["POST"])
# @jwt_required()
# def complete_vendor_profile_2():
    # data = request.get_json()
    # user = get_current_user()

    # if not user:
    #     return jsonify({"message": "User not found"}), 401

    # if user.role != "vendor":
    #     return jsonify({"message": "User Auth Error, not a vendor"}), 401

    # full_name = data.get("full_name")
    # phone_number = data.get("phone_number")
    # location = data.get("location")
    # biography = data.get("biography")
    # thumbnail = data.get("thumbnail")
    # other_images = data.get("other_images")
    # video_showcase = data.get("video_showcase")
    # location_name = data.get("location_name")
    # address = data.get("address")
    # rate = data.get("rate")
    # fixed_price = data.get("fixed_price")

    # if not all([full_name, phone_number, location, biography, thumbnail, video_showcase, address, location_name, fixed_price, rate]):
    #     return jsonify({"message": "All required fields are necessary for the vendor profile"}), 400


    # # check for vendor profile is already created or not so that it can be added else updated
    # # relation
    # vendor = user.vendor

    # # If not already present(vendor) then create profile part 2 for it

    # if not vendor:
    #     vendor = Vendor(
    #         full_name=full_name,
    #         phone_number=phone_number,
    #         location=location,
    #         biography=biography,
    #         video_showcase=video_showcase,
    #         location_name=location_name,
    #         address=address,
    #         rate=rate,
    #         fixed_price=fixed_price
    #     )

    #     # Handle thumbnail image
    #     if thumbnail:
    #         thumbnail_filename = f"{uuid.uuid4()}.png"
    #         thumbnail_path = os.path.join(app.config['VENDOR_IMAGES_FOLDER'], thumbnail_filename)

    #         # Thumbnail contains the base64 data and on func we passed filename so that main image can be accessed and can be conveted to bytes
    #         save_image_from_base64(thumbnail, thumbnail_path)

    #         # make the image name in thumbnail column
    #         vendor.thumbnail = thumbnail_filename

    #     # Handle other images
    #     if other_images:
    #         vendor.other_images = save_multiple_images_from_base64(other_images)

    #     user.vendor = vendor
    #     db.session.commit()
    #     return jsonify({"message": "Successfully completed the part of the profile"})

    # else:
    #     vendor.full_name = full_name
    #     vendor.phone_number = phone_number
    #     vendor.location = location
    #     vendor.biography = biography
    #     vendor.video_showcase = video_showcase
    #     vendor.location_name = location_name
    #     vendor.address = address
    #     vendor.rate = rate
    #     vendor.fixed_price = fixed_price

    #     # Handle thumbnail image if provided
    #     if thumbnail:
    #         thumbnail_filename = f"{uuid.uuid4()}.png"
    #         thumbnail_path = os.path.join(app.config['VENDOR_IMAGES_FOLDER'], thumbnail_filename)
    #         save_image_from_base64(thumbnail, thumbnail_path)
    #         vendor.thumbnail = thumbnail_filename

    #     # Handle other images if provided
    #     if other_images:
    #         # here other images contains base64 images
    #         # so after calling the function the other images will return multiple base 64 images
    #         vendor.other_images = save_multiple_images_from_base64(other_images)

    #     db.session.commit()
    #     return jsonify({"message": "Successfully completed the 2nd part of the profile"})

###############################     Create Event       ######################################



# First vendor will be registered or complete his profile then can create event

@app.route("/create_event", methods=["POST"])
@jwt_required()
def create_event():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({"message": "User not found"}), 401

    if user.role != "vendor":
        return jsonify({"message": "User Auth Error, not a vendor"}), 401

    # Ensure the user is associated with a vendor profile
    if not user.is_vendor or not user.vendor:
        return jsonify({"message": "User is not associated with a vendor profile"}), 400

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
    facilities = data.get("facilities")
    description = data.get("description")
    event_type = data.get("event_type")

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
        event_type =  event_type,
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

    return jsonify({"message": "Event created successfully"})


###############################     Update Event     ######################################



@app.route("/update_event/<int:event_id>", methods = ["PUT"])
@jwt_required()
def update_event(event_id):
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({
            "message":"User Not Found !!"
        })

    if user.role != "vendor":
        return jsonify({
            "message":"User Authentication Error !!!"
        })

    # Ensuring that user is associated with a vendor profile
    if not user.vendor:
        return jsonify({
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
        "message":"Event Updated Successfully !!!"
    })


###############################     Delete Event     ######################################



@app.route("/delete_event/<int:event_id>", methods = ["DELETE"])
@jwt_required()
def delete_event(event_id):
    user = get_current_user()
    
    if not user:
        return jsonify({
            "message":"User Not Found !!"
        })

    if user.role != "vendor":
        return jsonify({
            "message":"User Auth Error, Not a vendor !!"
        })

    
    # Basically used this here so that we should know that the user is associated with a vendor profile or not
    # Here we are actually retrieving the vendor profile associated with a user
    vendor = user.vendor
    
    event = Event.query.filter_by(id = event_id , vendor=vendor).first()
    if not event:
        return jsonify({
            "message":"User Not Found !!"
        })
    
    db.session.delete(event)
    db.session.commit()

    return jsonify({
        "message":"Event Deleted Successfully !!!"
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
        return jsonify({'message': 'Invalid refresh token'}), 401



###############################     Search Events API        ######################################


@app.route('/search_event', methods=["POST"])
@jwt_required()
def search_event():
    data = request.get_json()
    event_type = data.get("event_type")
    location_name = data.get("location_name")

    # Pagination
    # Events Per Page
    events_per_page = 5

    # default set to page 1
    # In summary, offset helps you figure out where to start displaying items (pages) on a specific page, just like you would turn to a certain page in a book to read.
    
    # page will be passed as ?page = 1,2 .. it should be integer so we set for int.
    # By default page is set for 1
    page = int(request.args.get("page", 1))

    offset = (page - 1) * events_per_page

    if event_type and not location_name:
        events = Event.query.filter_by(event_type = event_type).offset(offset).limit(events_per_page).all()

    elif not event_type and location_name:
        events = Event.query.filter_by(location_name = location_name).offset(offset).limit(events_per_page).all()
    
    else:
        events = Event.query.filter_by(event_type=event_type, location_name=location_name).offset(offset).limit(events_per_page).all()


    if not event_type.strip() or not location_name.strip():
        if not event_type.strip() and not location_name.strip():

            # fetch all the events
            all_events = Event.query.all()

            # shuffled them for random records 
            random.shuffle(all_events)

            random_events = all_events[offset:offset + events_per_page]

            # random_events = Event.query.order_by(func.random()).offset(offset).limit(events_per_page).all()
            total_events_found = len(random_events)

            event_list = []
            for event in random_events:
                event_info = {
                    "thumbnail":event.thumbnail,
                    "event_type":event.event_type,
                    "rate":event.rate,
                    "fixed_price":event.fixed_price
                }
                event_list.append(event_info)

            return jsonify({
                "Total Random Events":"",
                "Event Information":event_list
            }), 200


    if not events:
        return jsonify({
            "message": "Events Not Found !!"
        })
    
    total_events_found = len(events)

    event_list = []
    for event in events:
        event_info = {
            # "id": event.id,
            "thumbnail": event.thumbnail,
            "event_type": event.event_type,
            "rate": event.rate,
            "fixed_price": event.fixed_price,
        }

        event_list.append(event_info)

    return jsonify({
        "Total Events": total_events_found ,
        "Events":event_list
    }), 200


# @app.route("/custom_event_search")
# @jwt_required()
# def custom_event_search():
#     data =  request.get_json()
#     event_type = data.get("event_type")
#     location_name = data.get("location_name")
#     min_price = 
#     max_price = 
#     start_date = 




#     # Building the base query to use for customize one .
#     query = db.session.query(Event)



###############################   Create Booking      ######################################

@app.route('/create_booking', methods=["POST"])
@jwt_required()
def create_booking():
    data = request.get_json()
    user = get_current_user()

    if not user:
        return jsonify({
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

    
    if all_day:
        start_time = "00:00:00"
        end_time = "23:59:59"

    else:
        start_time = data.get('start_time')
        end_time = data.get('end_time')
    


    if not all([full_name, email, guest_count, additional_notes, start_date, end_date, start_time, end_time, event_id]):
        return jsonify({
            "message": "All fields must be set !!"
        })

    print(full_name, email, guest_count, additional_notes, start_date, end_date, start_time, end_time, all_day, event_id)

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
        event_id=event_id
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "Event booked successfully !!"
    })



###############################     Upload Profile Image      ######################################



# remaining work : don't ask for email 

@app.route('/upload_image', methods=["POST"])
@jwt_required()
def upload_image():
    UPLOAD_FOLDER = 'images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    data = request.get_json()
    profile_image = data.get("profile_image")

    if not profile_image:
        return jsonify({"message": "No profile image provided!!"}), 400

    try:
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
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            user.profile_image = filename_path
            db.session.commit()

        return jsonify({"message": "Image uploaded successfully", "file_path": output_file_name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

# getting the image

@app.route('/images/<image_name>')
def serve_image(image_name):
    return send_from_directory('images', image_name)






###############################     Get Profile Image      ######################################




# @app.route('/get_profile_image', methods = ['GET'])
# @jwt_required()
# def get_profile_image():
#     user = get_current_user

#     if user and user.profile_image:
#         return send_file(io.BytesIO(user.profile_image), mimetype = 'image/png')

#     if not user or user.profile_image:
#         return jsonify({
#             "message": " Profile Image Not Available !!"
#         }) , 404




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


@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    password_validation_result = Validations.is_valid_password(new_password)

    if new_password != confirm_password:
        return jsonify({
            "message": "Password did not match."
        }), 400
    

    reset_token_obj = PasswordResetToken.query.filter_by(token=token).first()
    if not reset_token_obj:
        return jsonify({'message': 'Invalid reset token'}), 400

    if reset_token_obj.expired_at < datetime.utcnow():
        return jsonify({'message': 'Reset token has expired'}), 400

    user = User.query.get(reset_token_obj.user_id)
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.delete(reset_token_obj)
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)

