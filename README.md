# 🚗 Flask Car Shop

A simple e-commerce website for buying cars, built with Flask, SQLite, SQLAlchemy, Elasticsearch, and Bootstrap. Includes search and filter features, shopping cart, Stripe test payment, and profile management.

## Features:
- Full-text product search using Elasticsearch
- Filter by brand, category, color, and price range
- Shopping cart with quantity control
- Stripe test checkout
- 🖼Profile image upload
- User login and account info management
- Admin panel to add/update/delete products

## Technologies Used:
- Flask + Jinja2
- SQLite + SQLAlchemy
- Elasticsearch 8.13.4
- Bootstrap 5
- Stripe API (Test Mode)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone git@github.com:hoangnhat0910/fllask-car-shop.git
cd fllask-car-shop
```
2. Create and activate virtual environment
```bash
python3 -m venv venv
source myvenv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Start Elasticsearch (must be done manually before running app)
```bash
cd ~/elasticsearch-8.13.4
./bin/elasticsearch
```
5. Run the Flask app
```bash
cd ~/fllask-car-shop
flask run
```
Notes
Elasticsearch must always be running before you use the app.
For payment, use Stripe test cards. (4242 4242 4242 4242)

Secrets (e.g. Stripe keys) should not be pushed to GitHub. Use environment variables or .env file (and add .env to .gitignore).
fllask-car-shop/
