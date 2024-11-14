from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from models import User

def register_routes(app, db, bcrypt):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            first_name = request.form.get('firstname')
            last_name = request.form.get('lastname')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            
            
            if User.query.filter((User.username == username) | (User.email == email)).first():
                return 'User with that username or email already exists'
            
            if password != confirm_password:
                flash("password do not match. Please try again")
                return redirect(url_for('signup'))
            
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)
            
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful")
            return redirect(url_for('login'))
        
    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter(User.username == username).first()
            
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('Dashboard'))
            else:
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))
            
    
    @app.route('/Dashboard')
    def Dashboard():
        return render_template('Dashboard.html')
            
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
