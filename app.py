from flask import Flask

app = Flask(__name__)

from config import Config
from extensions import db
app.config.from_object(Config)
db.init_app(app)

from models import *
from public import public_bp
from admin import admin_bp

app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    ##app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)