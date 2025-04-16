from flask import redirect, url_for, render_template, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct
from shop.products.routes import brands, categories

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        color = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()

        if request.method=='POST':
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,
                                    'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
        if 'Shoppingcart' in session:
            print(session['Shoppingcart'])
            if product_id in session['Shoppingcart']:
                session['Shoppingcart'][product_id]['quantity'] += quantity
                session.modified = True
            else:
                session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                session.modified = True
                return redirect(request.referrer)
        else:
            session['Shoppingcart'] =  DictItems
            session.modified = True
            return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    
@app.context_processor
def cart_quantity():
    def total_cart_quantity():
        if 'Shoppingcart' in session:
            return sum(int(item['quantity']) for item in session['Shoppingcart'].values())  
        return 0
    return dict(total_cart_quantity=total_cart_quantity)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        # session.modified = True
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100)*float(product['price'])
        subtotal += (float(product['price']) - float(discount)) * int(product['quantity']) 
        # tax = ("%.2f" % (.06*float(subtotal)))
        # grandtotal = float("%.2f" % (1.06 * subtotal))
        tax = int(subtotal/10)
        grandtotal = float("%.2f" % (1.06 * subtotal))

    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, categories=categories(), brands=brands())

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = int(request.form.get('quantity'))
        color = request.form.get('color')
        try:
            session.modified=True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    session.modified = True
                    flash(f'Cart is updated!', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))
        
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
    
@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)