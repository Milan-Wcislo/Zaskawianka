import os
from flask import Flask, render_template, url_for, redirect, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv 

from forms import RegisterForm, LoginForm, SponsorForm, TeamForm, ProjectForm, ManagementForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

upload_folder = os.path.join('static', 'uploads')
 
app.config['UPLOAD'] = upload_folder

Bootstrap4(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DB_URI"]

db = SQLAlchemy()
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Sponsor(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=True)


class Management(db.Model):
    __tablename__ = "management"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(250), nullable=False)
    vintage = db.Column(db.String(20), nullable=False)
    trainer = db.Column(db.String(50), nullable=False)
    trainer_phone = db.Column(db.String(20), nullable=True)
    order = db.Column(db.Integer, nullable=False)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/nowy', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Użytkownik już istnieje!")
            return redirect(url_for('register'))
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=15)
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Utworzono i Zalogowano Użytkownika!")
        return redirect(url_for('home'))
    return render_template("forms.html", form=form, registered=False, is_register=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Zalogowano Użytkownika!")
                return redirect(url_for('home'))
            else:
                flash("Nieprawidłowy Email lub Hasło!")
                return redirect(url_for('login'))
        else:
            flash("Nieprawidłowy Email lub Hasło!")
            return redirect(url_for('login'))
    return render_template("forms.html", form=form, registered=False, is_login=True)


@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash("Wylogowano!")
    return redirect(url_for('home'))


# Sponsors


@app.context_processor
def inject_sponsors():
    sponsors = Sponsor.query.all()
    return dict(sponsors=sponsors)


@app.route('/dodaj-sponsora', methods=['GET', 'POST'])
@login_required
def add_sponsor():
    form = SponsorForm()
    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)
            
            new_sponsor = Sponsor(
                name=form.name.data,
                url=form.website_url.data,
                img=img,
            )

            db.session.add(new_sponsor)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("forms.html", form=form, is_add_sponsor=True)


@app.route('/edycja-sponsora/<int:sponsor_id>', methods=['GET', 'POST'])
@login_required
def edit_sponsor(sponsor_id):
    
    sponsor = Sponsor.query.get_or_404(sponsor_id)
    form = SponsorForm(
        name=sponsor.name,
        website_url=sponsor.url,
    )
    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)

            sponsor.name = form.name.data
            sponsor.img = img
            sponsor.url = form.website_url.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("forms.html", form=form, is_edit_sponsor=True)


@app.route('/delete_sponsor/<int:sponsor_id>')
@login_required
def delete_sponsor(sponsor_id):
    sponsor = Sponsor.query.get_or_404(sponsor_id)

    image_path = sponsor.img

    if image_path and os.path.exists(image_path):
      try:
          os.remove(image_path)
      except OSError as e:
          print(f"Error deleting image: {e}")
          pass

    db.session.delete(sponsor)
    db.session.commit()
    return redirect(url_for('home'))


# Club


# History
@app.route('/historia')
def club_history():
    return render_template("history.html")


# Statute
@app.route('/statut')
def club_statute():
    return render_template("statute.html")


# Managment
@app.route('/zarzad')
def club_management():
    members = Management.query.order_by(Management.order)
    return render_template("management.html", members=members)


@app.route('/dodaj-czlonka-zarzadu', methods=['GET', 'POST'])
@login_required
def add_management():
    form = ManagementForm()
    if form.validate_on_submit():
        new_member = Management(
            name=form.name.data,
            position=form.position.data,
            order=form.order.data,
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('club_management'))
    return render_template("forms.html", form=form, is_add_management=True)


@app.route('/edytuj-czlonka-zarzadu/<int:management_id>', methods=['GET', 'POST'])
@login_required
def edit_management(management_id):
    management_member = Management.query.get_or_404(management_id)
    form = ManagementForm(
        name=management_member.name,
        position=management_member.position,
    )
    if form.validate_on_submit():
        management_member.name = form.name.data
        management_member.position = form.position.data
        management_member.order = form.order.data
        db.session.commit()
        return redirect(url_for('club_management'))
    return render_template("forms.html", form=form, is_edit_management=True)


@app.route('/usun-czlonka-zarzadu/<int:management_id>')
@login_required
def delete_management(management_id):
    management_member = Management.query.get_or_404(management_id)
    db.session.delete(management_member)
    db.session.commit()
    return redirect(url_for('club_management'))


# Teams


@app.route('/druzyny')
def teams():
    teams = Team.query.order_by(Team.order)
    return render_template("teams.html", teams=teams)


@app.route('/dodaj-druzyny', methods=['GET', 'POST'])
@login_required
def add_team():
    form = TeamForm()
    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)

            new_team = Team(
                name=form.name.data,
                img=img,
                vintage=form.vintage.data,
                trainer=form.trainer.data,
                trainer_phone=form.trainer_phone.data,
                order=form.order.data
            )

            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for('teams'))
    return render_template("forms.html", form=form, is_add_team=True)


@app.route('/edycja-druzyny/<int:team_id>', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    
    team = Team.query.get_or_404(team_id)
    form = TeamForm(
        name=team.name,
        vintage=team.vintage,
        trainer=team.trainer,
        trainer_phone=team.trainer_phone,
        order=team.order
    )
    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)

            team.name = form.name.data
            team.img = img
            team.vintage = form.vintage.data
            team.trainer = form.trainer.data
            team.trainer_phone = form.trainer_phone.data
            team.order = form.order.data
        db.session.commit()
        return redirect(url_for('teams'))
    return render_template("forms.html", form=form, is_edit_team=True)


@app.route('/delete_team/<int:team_id>')
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)

    image_path = team.img

    if image_path and os.path.exists(image_path):
      try:
          os.remove(image_path)
      except OSError as e:
          print(f"Error deleting image: {e}")
          pass

    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('teams'))


# Regulations


@app.route('/regulations')
def regulations():
    return render_template("regulations.html")


# Projects


@app.route('/projekty')
def projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)


@app.route('/dodaj-projekt', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()

    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)

            new_project = Project(
                img=img,
                name=form.name.data,
                description=form.description.data,
            )

            db.session.add(new_project)
            db.session.commit()

            return redirect(url_for('projects'))
    return render_template("forms.html", form=form, is_add_project=True)


@app.route('/edycja-projektu/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(
        name=project.name,
        description=project.description
    )

    if form.validate_on_submit():
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD'], filename))
            img = os.path.join(app.config['UPLOAD'], filename)

            project.img=img
            project.name=form.name.data
            project.description=form.description.data
            
            db.session.commit()

        return redirect(url_for('projects'))
    return render_template("forms.html", form=form, is_edit_project=True)


@app.route('/delete_project/<int:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    image_path = project.img

    if image_path and os.path.exists(image_path):
      try:
          os.remove(image_path)
      except OSError as e:
          print(f"Error deleting image: {e}")
          pass

    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects'))


# Contact


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False)
