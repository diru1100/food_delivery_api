from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import Config

# all major dependencies are defiend here itself maintaining modularity

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# avoiding circular imports
from . import routes, models