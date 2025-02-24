from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.contact import Contact
from app.models.user import User