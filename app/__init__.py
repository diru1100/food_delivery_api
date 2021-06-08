from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from .config import Config
# all major dependencies are defiend here itself maintaining modularity

# engine = create_engine('sqlite:///application.db',
#                        convert_unicode=True, echo=False)
# Base = declarative_base()
# Base.metadata.reflect(engine)


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
db.create_all()
# avoiding circular imports
from . import routes, models