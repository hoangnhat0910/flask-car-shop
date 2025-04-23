from shop import db, app
from datetime import datetime
from sqlalchemy import event



class Addproduct(db.Model):
    __tablename__ = 'addproduct'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))
    
    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    # is_fake = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<Product %r>' % self.name
    
class Brand(db.Model):
    # __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False, unique=True)

    def __repr__(self):
        return '<Brand %r>' % self.name

class Category(db.Model):
    # __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False, unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


with app.app_context():
    db.create_all()

# from shop import es
# from shop.products.routes import index_product

# @event.listens_for(Addproduct, 'after_insert')
# def after_insert(mapper, connection, target):
#     index_product(target)

# @event.listens_for(Addproduct, 'after_update')
# def after_update(mapper, connection, target):
#     index_product(target)

# @event.listens_for(Addproduct, 'after_delete')
# def after_delete(mapper, connection, target):
#     es.delete(index="products", id=target.id, ignore=[400, 404])
    