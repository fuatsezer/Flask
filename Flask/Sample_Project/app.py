from flask import Flask,render_template,url_for,redirect,flash
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    fruits = ["Apple","Mango"]
    return render_template("index.html",fruits = fruits)
    # return redirect(url_for('about'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/css')
def css():
    return render_template("css.html")
@app.errorhandler(404)
def page_not_found(e):
    return "This page was not found"

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)