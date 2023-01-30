from flask import Blueprint, session, redirect, flash, render_template, url_for, request
from flask_login import LoginManager, UserMixin, login_required, logout_user, login_user, current_user

from client.forms import LoginForm
from client.models import pocket

import time


auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_message = 'Please log in first'
login_manager.login_view = 'auth.login'


class User(UserMixin):

    def get_id(self):
        return self.token

    def sign_in(self, email='', password=''):
        data, code = pocket.admin_auth_via_email(email, password)
        if code != 200:
            session['token'] = None
            return False
        session['token'] = {
            'value': data.get('token'),
            'user': data.get('id'),
            'email': data.get('email'),
            'avatar': data.get('avatar'),
            'issued': time.time()
        }
        return True

    @property
    def token(self):
        return session.get('token', None)

    @property
    def is_authenticated(self):
        if not self.token:
            return False
        issued = self.token.get('issued')
        elapsed = time.time() - issued
        # Invalidate token if 2 weeks old
        if elapsed >= 1209600:
            session['token'] = None
            return False
        else:
            return True


@login_manager.user_loader
def load_user(user_id):
    return User()


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to home if already auth'd
    if current_user.is_authenticated:
        return redirect(url_for('app.get_index'))

    # Submitted valid form
    form = LoginForm()
    if form.validate_on_submit():
        user = User()

        # Try to authenticate user
        if not user.sign_in(form.email.data, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user)  # Mark session as auth'd

        page = request.args.get('next')  # Go to next page or home
        return redirect(page) if page \
            else redirect(url_for('app.get_index'))

    # Return form with errors or send a fresh one
    return render_template('admin/login.html', form=form)