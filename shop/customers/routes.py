from flask import redirect, url_for, render_template, flash, request, session, current_app, make_response
from shop import db, app, photos, bcrypt, login_manager
from flask_login import login_required, current_user, login_user, logout_user
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
import secrets
import os
import json
import pdfkit
import stripe


publishable_key='pk_test_51RBvbGRd4xpbA37DqeVzujzU0acYsL1GyxJCLrxZhUiLrxu6oiI6J4Nxr5HCmdUbNwHs7PfS7KXda4DXc6tdOCTu00iG6XJe1v'
stripe.api_key='sk_test_51RBvbGRd4xpbA37DWbfLlDp0KseTRv7f6LmlRAObdoDB5icr35mU8xGtNdRI7yBzfWCkQgFLMkYt8ERrB4DJJDDW00ogTLcNpH'


@app.route('/purchase', methods=['POST'])
@login_required
def purchase():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source= request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        description='my_first_website',
        amount=amount,
        currency='usd',
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))


@app.route('/thanks')
@login_required
def thanks():
    return render_template('customers/thanks.html', discount_code='THANKYOU10')


@app.route('/customers/register', methods=['GET', 'POST'])
def customerRegister():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        profile = photos.save(request.files.get('profile'), name=secrets.token_hex(10) + ".")
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, 
                            password=hash_password, country=form.country.data, city=form.city.data,
                            address = form.address.data, contact=form.contact.data, zipcode=form.zipcode.data, profile=profile)
        db.session.add(register)
        flash(f'Welcome {form.name.data}. Thank you for register!', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('/customers/register.html', form=form)


@app.route('/customers/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now.', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email or password', 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('customers/login.html',form=form)


@app.route('/customers/info', methods=['GET', 'POST'])
@login_required
def customerInfo():
    customer_id = current_user.id
    user = Register.query.get_or_404(customer_id)
    return render_template('customers/info.html', user=user)


@app.route('/change_profile_image', methods=['POST'])
@login_required
def change_profile_image():
    profile = request.files.get('profile')
    if not profile:
        flash('No image selected.', 'warning')
        return redirect(url_for('customerInfo'))

    allowed_extensions = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    filename = profile.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        flash('Unsupported file format. Only PNG and JPEG allowed.', 'danger')
        return redirect(url_for('customerInfo'))

    ext = filename.rsplit('.', 1)[1]
    new_filename = secrets.token_hex(10) + '.' + ext
    save_path = os.path.join(app.root_path, 'static/images', new_filename)
    profile.save(save_path)

    current_user.profile = new_filename
    db.session.commit()
    flash('Profile image updated successfully.', 'success')
    return redirect(url_for('customerInfo'))


@app.route('/customers/logout')
def  customerLogout():
    logout_user()
    return redirect(url_for('home'))


# remove unwanted details from shopping cart
def updateshoppingcart():
    for _key, product in session['Shoppingcart'].items():
        session.modified=True
        del product['image']
        del product['colors']
    return updateshoppingcart


@app.route('/getorder/')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong when get order', 'danger')
            return redirect(url_for('getCart'))
        

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            # tax = ("%.2f" % (.06 * float(subTotal)))
            # grandTotal = ("%.2f" % (1.06 * float(subTotal)))
            tax = int(subTotal/10)
            grandTotal = str(int(1.1 * subTotal))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customers/order.html', invoice=invoice, tax=tax, subTotal=subTotal, 
                           grandTotal=grandTotal, customer=customer, orders=orders)


@app.route('/get_pdf/<invoice>', methods=['GET','POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                # tax = ("%.2f" % (.06 * float(subTotal)))
                # grandTotal = ("%.2f" % (1.06 * float(subTotal)))
                tax = int(subTotal/10)
                grandTotal = str(int(1.1 * subTotal))
            rendered= render_template('customers/pdf.html', invoice=invoice, tax=tax, 
                                    grandTotal=grandTotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline; filename='+invoice+'.pdf'
            # response.headers['content-Disposition']='atteched; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))