from flask import Flask
from flask_sqlalchemy import SQLAlchemy


config_file="..\\instance\\config.py"
#databaseobject
db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config.from_pyfile(config_file)
    #initialize database file
    db.init_app(app)

    from .auth import bp_auth
    from .inventory import bp_inventory
    from .transactions import bp_transactions
    from .views import bp_home
    from .writer import bp_writer
    

    app.register_blueprint(bp_inventory,url_prefix="/inventory")
    app.register_blueprint(bp_transactions,url_prefix="/transactions")
    app.register_blueprint(bp_writer,url_prefix="/generate")
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_home)

    # from .models import Users,Items,Transactions
    return app