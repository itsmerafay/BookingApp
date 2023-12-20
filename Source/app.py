from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Message, Mail
# import pdfkit
from flask_migrate import Migrate
from config import Config
from json import JSONEncoder
from flask_cors import CORS

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
app.config["EVENT_ICON_FOLDER"] = "static/event_icons"


# app.config['WKHTMLTOPDF_PATH'] = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe' # specify the path to wkhtmltopdf here
# )

mail = Mail(app)


from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
