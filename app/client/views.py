import json
from box import Box

from flask import Blueprint, flash, redirect, render_template, url_for, request, session
from flask_login import login_required

from client.forms import CustomerForm
from .models import pocket


app = Blueprint('app', __name__)


@app.get('/')
@login_required
def get_index():
    return render_template('home.html')


@app.get('/admin')
def get_admin():
    # Forward to PocketBase admin
    return redirect("http://127.0.0.1:8090/_")


# ------------------ CUSTOMERS ----------------- #


@app.get('/customers')
@login_required
def get_customers():
    data = pocket.records_get_list('customers', 1, 20, sort='+first')
    customers = data['items']
    return render_template('customers/index.html', customers=customers)


@app.get('/customers/<uid>')
@login_required
def get_customer(uid):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/show.html', customer=customer)


@app.route('/customers/create', methods=['GET', 'POST'])
@login_required
def create_customer():
    customer = {}
    form = CustomerForm()
    if form.validate_on_submit():
        form.populate_obj(customer)
        customer = pocket.records_update('customers', customer)
        flash(f'Created Customer: {customer.first}')
        return redirect(url_for('app.get_customers'))
    return render_template('customers/edit.html', form=form)


@app.route('/customers/<uid>/edit', methods=['GET', 'POST'])
@login_required
def update_customer(uid):
    customer = pocket.records_get_one('customers', uid)
    orders = pocket.records_get_list('orders', filters=f"customer='{uid}'")
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        customer = pocket.records_update('customers', uid, customer)
        flash(f'Updated Customer: {customer.first}')
        return redirect(url_for('app.get_customers', uid=uid))
    return render_template('customers/edit.html', form=form, orders=orders)


# ------------------- ORDERS ------------------- #


@app.get('/orders')
@login_required
def get_orders():
    data = pocket.records_get_list('orders', 1, 20, sort='+title')
    orders = data['items']
    return render_template('orders/index.html', orders=orders)


@app.route('/orders/<uid>/update', methods=['GET', 'POST'])
@login_required
def update_order(uid):
    return 'order'