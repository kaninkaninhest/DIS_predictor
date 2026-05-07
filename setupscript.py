from app1 import app, db
import models
with app.app_context():
    db.create_all()