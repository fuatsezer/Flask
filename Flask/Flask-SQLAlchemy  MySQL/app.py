from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    
    def __init__(self,name,specialisation):
        self.name = name
        self.specialisation = specialisation
    def __repr__(self):
        return '<Product {}>'.format(self.id)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy=True))
    def __repr__(self):
        return '<Post %r>' % self.title
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return '<Category %r>' % self.name
# db.create_all()
#%%
king = Author(name="King", specialisation="Horor")
db.session.add(king)
db.session.commit()
#%%
py = Category(name='Python')
Post(title='Hello Python!', body='Python is pretty cool', category=py)
p = Post(title='Snakes', body='Ssssssss')
py.posts.append(p)
db.session.add(py)
db.session.commit()
#%%
print(py.posts)
#%%
print(Author.query.all())
print(Author.query.filter_by(name='King').first())
king = Author.query.filter_by(name='King').first()
print(king.specialisation)
#%%
db.session.delete(Author.query.filter_by(name='King').first())
db.session.commit()

#%%
Author.query.filter_by(name='King').update({'specialisation':"comedy"})
db.session.commit()
#%%
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
    
    
    
    
    
    
    
    