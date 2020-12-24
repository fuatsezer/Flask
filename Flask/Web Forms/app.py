from flask import Flask,render_template,redirect, url_for
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class NameForm(Form):
    name= StringField("What is your name?",validators=[DataRequired()])
    submit=SubmitField("Submit")

app= Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"

@app.route('/', methods=["GET","POST"])
def index():
    name = ""
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        # return redirect(url_for('index'))
        
    return render_template('index.html', form=form,name=name)

if __name__=="__main__":
    app.run(debug=True,use_reloader=False)
