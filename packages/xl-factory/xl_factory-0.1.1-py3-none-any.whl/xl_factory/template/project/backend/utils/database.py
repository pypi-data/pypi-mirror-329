from xl_database import db
from xl_database.model import Model
from backend.config import APP_CONFIG


engine, metadata = db.init(APP_CONFIG['SQLALCHEMY_DATABASE_URI'])
