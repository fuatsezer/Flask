# is_authenticated : Bu, mevcut kullanıcının kimliğinin doğrulanmış olup olmadığını kontrol eder
# is_active: Bu, bir kullanıcının aktif olup olmadığını kontrol eder
# is_anonymous: Bu, blogumuza anonim erişimi destekler
# get_id: Bu, kullanıcı kimliğini getirir

from flask import Flask,redirect,url_for,flash,render_template,request,abort
from urllib.parse import urlparse, urljoin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,UserMixin,login_user,login_required
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo,Email
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import URLSafeSerializer

app = Flask(__name__)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.session_protection ="strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
app.config["SECRET_KEY"] = "mysecretkey"
app.config['SECURITY_PASSWORD_SALT'] = "mysecpasssalt"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db=SQLAlchemy(app)
class Author(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True,nullable=False)
    specialisation = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    isVerified = db.Column(db.Boolean,nullable=False,default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    
    def __init__(self,name,email,specialisation,password,isVerified):
        self.name = name
        self.email = email
        self.specialisation = specialisation
        self.password_hash = generate_password_hash(password)
        self.isVerified = isVerified
        
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<Product {}>'.format(self.id)
db.create_all()

class RegistrationForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    specialisation = StringField("Specialisation",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("New Password",validators=[DataRequired(),EqualTo("confirm",
                                                                               message="Password must match")])
    confirm = PasswordField("Repeat Password",validators=[DataRequired()])
    accept_tos = BooleanField("I accept the contract",validators=[DataRequired()])
    submit = SubmitField("Register")
    def check_email(self,field):
        return Author.query.filter_by(email=field.data).first()

    
class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Log in")

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc     



@login_manager.user_loader 
def load_user(user_id):
    return Author.query.get(user_id)

@app.route("/") 
def index():
    return render_template("index.html")
    
@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.check_email(form.email):
            flash("Your email used")
        else:
            
            user = Author(name= form.name.data, email=form.email.data, 
                          specialisation= form.specialisation.data,password= form.password.data,
                          isVerified=False)
            db.session.add(user)
            db.session.commit()             
            flash("Thanks for registeration")
            return redirect(url_for("login"))
    return render_template("registration.html", form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Author.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('home'))
    return render_template('login.html', form=form)

@app.route("/home")
@login_required
def home():
    return render_template("home.html")
           
if __name__=="__main__":
    app.run(debug=True,use_reloader=False)


#%%
user = Author.query.all()
print(user)








