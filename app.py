from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from models import db, Rep, Prospect, Commission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rapid.db'
app.config['SECRET_KEY'] = 'change-me'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Rep.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    prospects = Prospect.query.all()
    return render_template('index.html', prospects=prospects)

@app.route('/prospect/add', methods=['GET', 'POST'])
@login_required
def add_prospect():
    if request.method == 'POST':
        p = Prospect(
            name=request.form['name'],
            note=request.form.get('note'),
            color=request.form.get('color'),
            demo_date=request.form.get('demo_date') or None,
            review_date=request.form.get('review_date') or None,
            onboarding_date=request.form.get('onboarding_date') or None,
            price=float(request.form.get('price') or 0),
            product=request.form.get('product'),
            integration_fee=float(request.form.get('integration_fee') or 0),
            package_type=request.form.get('package_type'),
            closer_id=int(request.form.get('closer') or 0) or None,
            setter_id=int(request.form.get('setter') or 0) or None,
        )
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    reps = Rep.query.all()
    return render_template('prospect_form.html', reps=reps)

@app.route('/prospect/<int:pid>/sell', methods=['POST'])
@login_required
def sell_prospect(pid):
    prospect = Prospect.query.get_or_404(pid)
    prospect.sold = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        rep = Rep.query.filter_by(name=name).first()
        if rep:
            login_user(rep)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

