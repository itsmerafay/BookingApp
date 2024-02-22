from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Message, Mail
# import pdfkit
from flask_migrate import Migrate
from config import Config
from json import JSONEncoder
from flask_cors import CORS
# from push_notification import setup_push_notifications, send_push_notification


app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes
app.json_encoder = JSONEncoder
app.config.from_object(Config)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdulrafayatiq.03@gmail.com'
app.config['MAIL_PASSWORD'] = 'todp ilxm pjdf wdwa'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51OL25jCvNBqAG6fPGBNbOuZDVlm74liMRkTByZ4YxYJvkggMRW5wFLIooDyMSxlGgPpGlGUDECYZ3hKkFuEiByu000aZhNzZ2C'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51OL25jCvNBqAG6fPkHTZzZnl8vHk0kjfcM4t0Lt7MGQNVkPIfy8TMtNrB1mKfWCLbOAQ1gW9EeYpIPsShWm6wwk900FngUWdTx'
app.config["EVENT_ICON_FOLDER"] = "static/event_icons"


# app.config['WKHTMLTOPDF_PATH'] = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe' # specify the path to wkhtmltopdf here
# )

mail = Mail(app)


from routes import *


if __name__ == '__main__':
    with app.app_context():
        # setup_push_notifications()
        db.create_all()
    app.run(debug=True)
