from flask import redirect, url_for, render_template, flash, request, session, current_app, jsonify
from shop import db, app, photos, es
from .models import Brand, Category, Addproduct
from .forms import Addproducts
from sqlalchemy import func
import secrets, os
import math


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=18)
    return render_template("products/index.html", title="Product Page", products=products, brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_bra = Brand.query.filter_by(id=id).first_or_404()
    product_by_brand = Addproduct.query.filter_by(brand=get_bra).paginate(page=page, per_page=15)
    return render_template('products/index.html', product_bb=product_by_brand, brands=brands(), categories=categories(), get_bra=get_bra)

@app.route('/category/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    product_by_category = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=15)
    return render_template('products/index.html', product_bc=product_by_category, brands=brands(), categories=categories(), get_cat=get_cat)

@app.route('/product/<int:id>')
def single_product(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id==Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id==Addproduct.category_id)).all()
    return render_template('products/single_product.html', product=product, brands=brands, categories=categories)

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was add to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands=brands())

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'username' not in session:
        flash(f'Please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =='POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated!', 'success')
        db.session.commit()
        return redirect(url_for('brand'))
    return render_template('products/updatebrand.html', title='Update brand page', updatebrand=updatebrand)

@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'username' not in session:
        flash(f'Please login first', 'danger')
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =='POST':
        updatecategory.name = category
        flash(f'Your category has been updated!', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update category page', updatecategory=updatecategory)

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The Category {getcategory} was add to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcategory'))

    return render_template('products/addcategory.html', categories=categories())

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()

    form = Addproducts(request.form)
    if request.method=='POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, brand_id=brand, category_id=category, image_1=image_1,
                            image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to database', 'success')
        db.session.commit()
        index_product(addpro)
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add product page', form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.desc = form.desc.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        for img in ["image_1", "image_2", "image_3"]:
            if request.files.get(img):
                try:
                    os.unlink(os.path.join(current_app.root_path, "static/images/", getattr(product, img)))
                except Exception as e:
                    print(f'Can not delete {img}: {e}')
                setattr(product, img, photos.save(request.files.get(img), name=secrets.token_hex(10) + "."))

        db.session.commit()
        index_product(product)
        flash(f'Your product has been updated!', 'success')

    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc
    form.discount.data = product.discount
    return render_template('products/updateproduct.html', form = form, brands=brands, categories=categories, product=product)

@app.route('/deletebrand/<int:id>', methods = ['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} has been deleted from your database', 'success')
        return redirect(url_for('brand'))
    flash(f"The brand {brand.name} can' be deleted", 'warning')
    return redirect(url_for('brand')) 

@app.route('/deletecategory/<int:id>', methods = ['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} has been deleted from your database', 'success')
        return redirect(url_for('category'))
    flash(f"The category {category.name} can' be deleted", 'warning')
    return redirect(url_for('category')) 
    
@app.route('/deleteroduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        for img in ["image_1", "image_2", "image_3"]:  
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/", getattr(product, img)))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted!', 'success')
    else:
        flash(f"Can't not delete product {product.name}", 'success')
    return redirect(url_for('admin'))


@app.route('/clear_product', methods=['POST'])
def clearproduct():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    try:
        db.session.query(Addproduct).delete()
        db.session.commit()
        flash('All products have been deleted.', 'success')
    except Exception as e:
        flash(f'Error deleting products: {str(e)}', 'danger')

    return redirect(url_for('admin'))


@app.route("/about-us")
def about():
    return render_template("about.html", title="About Us")

@app.context_processor
def inject_common_data():
    brands = Brand.query.all()
    categories = Category.query.all()
    return dict(brands=brands, categories=categories)


def create_index():
    if es.indices.exists(index="products"):
        es.indices.delete(index="products")  # Xóa để tạo mới nếu cần

    mapping = {
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "description": {"type": "text"},
                "brand": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "category": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "price": {"type": "float"}
            }
        }
    }
    es.indices.create(index="products", body=mapping)

def index_product(product):
    doc = {
        'id':product.id,
        'name': product.name,
        'description': product.desc,
        'price': product.price,
        'brand': str(product.brand.name) if product.brand else None,
        'category': str(product.category.name) if product.category else None,
        'colors':product.colors,
        'image':product.image_1
    }
    es.index(index="products", id=product.id, body=doc)


def aggregate_field_counts(products, field):
    counts = {}
    for product in products:
        value = product['_source'].get(field)
        if value:
            counts[value] = counts.get(value, 0) + 1
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts[:5], sorted_counts[5:]

create_index()

def parse_price_arg(value, default):
    try:
        # Xóa ký tự $, dấu phẩy rồi parse float
        return float(str(value).replace('$', '').replace(',', ''))
    except (ValueError, TypeError):
        return default



@app.route("/reindex")
def reindex_all():
    products = Addproduct.query.all()
    for product in products:
        index_product(product)
    return "Re-indexed all products!"

def build_base_query(query):
    if query:
        return {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "description"]
                }
            },
            "size": 1000
        }
    return {
        "query": {"match_all": {}},
        "size": 1000
    }

def build_final_query(query, filters, from_, size):
    must_clause = {
        "multi_match": {
            "query": query,
            "fields": ["name", "description"]
        }
    } if query else {"match_all": {}}

    return {
        "query": {
            "bool": {
                "must": must_clause,
                "filter": filters
            }
        },
        "from": from_,
        "size": size
    }

def calculate_price_range(products):
    if not products:
        return 0, 200000
    prices = [p['_source']['price'] for p in products]
    return min(prices), max(prices)

@app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    from_ = (page - 1) * per_page

    query = request.args.get('q', '').strip()
    # brand = request.args.get('brand')
    # category = request.args.get('category')
    brand_selected = request.args.getlist('brand')
    category_selected = request.args.getlist('category')
    selected_min_price = parse_price_arg(request.args.get('min_price'), None)
    selected_max_price = parse_price_arg(request.args.get('max_price'), None)

    base_query = build_base_query(query)
    base_res = es.search(index="products", body=base_query)
    base_products = base_res['hits']['hits']

    search_min_price, search_max_price = calculate_price_range(base_products)

    if selected_min_price is None:
        selected_min_price = search_min_price
    if selected_max_price is None:
        selected_max_price = search_max_price

    filters = []
    if brand_selected:
        filters.append({"terms": {"brand.keyword": brand_selected}})
    if category_selected:
        filters.append({"terms": {"category.keyword": category_selected}})
    filters.append({
        "range": {
            "price": {
                "gte": selected_min_price,
                "lte": selected_max_price
            }
        }
    })

    final_query = build_final_query(query, filters, from_, per_page)
    res = es.search(index="products", body=final_query)
    products = res['hits']['hits']
    total_results = res['hits']['total']['value']
    total_pages = math.ceil(total_results / per_page)

    top_brands, more_brands = aggregate_field_counts(base_products, 'brand')
    top_categories, more_categories = aggregate_field_counts(base_products, 'category')

    return render_template(
        'products/search_results.html',
        results=products,
        query=query,
        top_brands=top_brands,
        more_brands=more_brands,
        top_categories=top_categories,
        more_categories=more_categories,
        brand_selected=brand_selected,
        category_selected=category_selected,
        search_min_price=search_min_price,
        search_max_price=search_max_price,
        min_price=selected_min_price,
        max_price=selected_max_price,
        page=page,
        total_pages=total_pages
    )
