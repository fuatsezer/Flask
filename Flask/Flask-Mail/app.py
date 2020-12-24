from flask import Flask
from flask_mail import Mail,Message
app=Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'test354509@gmail.com'
app.config['MAIL_PASSWORD'] = 'GBfvdcsxaz123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

@app.route("/")
def index():
    msg = Message("Hello",sender="test354509@gmail.com",
                  recipients=["fuatsezer199696@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return "<h1>Sending</h1>"
if __name__=="__main__":
    app.run(debug=True,use_reloader=False)