from flask import Flask,request,redirect,render_template
from flask_bootstrap import Bootstrap

app= Flask(__name__)
Bootstrap(app)
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return "<p>Your browser is {}</p>".format(user_agent)

@app.route('/user/<name>')
def user(name):
    return "<h1>Hello {}</h1>".format(name)
@app.route('/google')
def google():
    return redirect('http://www.google.com')
@app.route('/getting/<name>')
def getting(name):
    return render_template("user.html",name=name)

if __name__=="__main__":
    app.run(debug=True,use_reloader=False)