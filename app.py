from flask import Flask
from config import Config
from extensions import db, migrate
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Development-only secret key (safe for this school project)
    app.secret_key = "123"  
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)