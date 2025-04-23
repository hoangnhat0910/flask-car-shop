from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres.qdyjelcdajiitecvomzi:%40%400840Nhat@aws-0-us-east-1.pooler.supabase.com:5432/postgres")


app.config['SECRET_KEY']='hoangnhat_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername =='sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
        
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u"Please login first!"

# es = Elasticsearch("http://localhost:9200")
from dotenv import load_dotenv
load_dotenv()

BONSAI_URL = os.getenv("BONSAI_URL")
es = Elasticsearch(
    os.getenv("BONSAI_URL"),
    headers={"Content-Type": "application/json"}
)


# res = es.search(index="products", body={"query": {"match_all": {}}})

# for hit in res["hits"]["hits"]:
#     print("ID:", hit["_id"])
#     print("Name:", hit["_source"]["name"])
#     print("Description:", hit["_source"]["description"])
#     print("---")

@app.template_filter('format_currency')
def format_currency(value):
    try:
        return "${:,}".format(int(value))
    except (ValueError, TypeError):
        return "$0"
    
# @app.template_filter('format_currency_int')
# def format_currency_int(value):
#     return f"{int(value):,}".replace(",", ",")


from shop.admin import routes
from shop.products import routes
from shop.products.routes import reindex_all
from shop.carts import carts
from shop.customers import routes
# from fake_product_import import create_fake_products

with app.app_context():
    reindex_all()
# create_fake_products()