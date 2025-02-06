from flask_sqlalchemy import SQLAlchemy
from models.model import Model


db = SQLAlchemy(model_class=Model)

