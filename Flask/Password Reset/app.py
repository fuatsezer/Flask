from flask import Flask,flash,redirect,url_for,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash
import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager,UserMixin,login_user,login_required
from flask_mail import Message,Mail
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'test354509@gmail.com'
app.config['MAIL_PASSWORD'] = 'GBfvdcsxaz123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
app.config["SECRET_KEY"] = "mysecretkey"
app.config['SECURITY_PASSWORD_SALT'] = "mysecpasssalt"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.session_protection ="strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email,salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration)
    except:
        return False
    return email

def send_email(to,subject,template):
    msg = Message(subject,recipients=[to],html=template,
                  sender= 'test354509@gmail.com')
    mail.send(msg)
    

class User(db.Model,UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    registered_on = db.Column(db.DateTime,nullable=False)
    confirmed = db.Column(db.Boolean,nullable=False,default=False)
    confirmed_on = db.Column(db.DateTime,nullable=True)
    
    def __init__(self,email,password,confirmed,paid=False,confirmed_on=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on 
db.create_all()    
class RegistrationForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Register")    
class PasswordResetForm(FlaskForm):
    password = PasswordField("New Password",validators=[DataRequired()])
    submit = SubmitField("Reset")   
@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(user_id) 
@app.route("/",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user =User(email=form.email.data, password=form.password.data,
                   confirmed=False)
        db.session.add(user)
        db.session.commit()
        token = generate_reset_token(user.email)
        confirm_url = url_for("reset_password",token=token,_external=True)
        html=render_template("activate.html", confirm_url=confirm_url)
        subject="Reset Password"
        send_email(user.email, subject, html)
        login_user(user)
        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("home"))
    return render_template("register.html", form=form)
    
@app.route("/reset/<token>",methods=['GET', 'POST'])
@login_required
def reset_password(token):
    form = PasswordResetForm()
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("reset_password.html", form=form)
@app.route("/home")
@login_required 
def home():
    return "<h1>Your reset password request in your email</h1>"

if __name__=="__main__":
    app.run(debug=True,use_reloader=False)









        
        
        
        

