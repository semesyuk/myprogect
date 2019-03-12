from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User, db, app, bcrypt


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        phone_numbe = request.form['phone_numbe']
        email = request.form['email']
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password)
        user = User(name=name,
                    last_name=last_name,
                    phone_numbe=phone_numbe,
                    email=email,
                    password=pw_hash)
        db.session.add(user)
        db.session.commit()
        return redirect("users")
    return render_template("registration.html")


@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash(f"hello {user.name}")
                return redirect(url_for('users'))
            return redirect(url_for('login'))
        flash('Credentials dont match')
        return redirect(url_for('registration'))
    return render_template('login.html')


@login_required
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
