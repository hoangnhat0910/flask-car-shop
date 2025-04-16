from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt, photos
from .forms import RegistrationForm, LoginForm
from .models import User, Image
from shop.products.models import Addproduct, Category, Brand
import secrets


@app.route('/admin')
def admin():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)


@app.route('/brands')
def brand():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title = 'Brand page', brands=brands)


@app.route('/categories')
def category():
    if 'username' not in session:
        flash(f'Please login first!', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/category.html', title = 'Category page', categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thank you for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Welcome {form.username.data}, You are login now', 'success')
            return redirect(url_for('admin'))
        else:
            flash(f'Wrong password, pls try again!', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html', title='Login Page', form=form)
  

@app.route('/logout')
def logout():
    session.pop('username', None) 
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))


@app.route('/admin/upload', methods=['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        # Upload profile image
        profile_file = request.files.get('profile')
        if profile_file:
            profile_name = secrets.token_hex(10) + "." + profile_file.filename.rsplit('.', 1)[-1]
            photos.save(profile_file, name=profile_name)
            img = Image(filename=profile_name, type='profile')
            db.session.add(img)

        # Upload gallery images
        gallery_files = request.files.getlist('gallery')
        for file in gallery_files:
            if file:
                gallery_name = secrets.token_hex(10) + "." + file.filename.rsplit('.', 1)[-1]
                photos.save(file, name=gallery_name)
                img = Image(filename=gallery_name, type='gallery')
                db.session.add(img)

        db.session.commit()
        flash('Images uploaded successfully!', 'success')
        return redirect(url_for('upload_images'))

    profile_images = Image.query.filter_by(type='profile').all()
    gallery_images = Image.query.filter_by(type='gallery').all()
    return render_template('admin/upload.html', profile_images=profile_images, gallery_images=gallery_images)