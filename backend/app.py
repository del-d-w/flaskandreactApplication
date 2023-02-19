# https://www.youtube.com/watch?v=msEmUtYqVV0
# pip install flask
# pip install Flask-SQLAlchemy
#  pip install psycopg2
# pip install flask-marshmallow
# pip install marshmallow-sqlalchemy
# pip install pipreqs  
# pipreqs
# pip install Flask-Cors


from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import datetime

app=Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:c98xa5@localhost/flaskapi'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)
ma=Marshmallow(app)

app.app_context().push()

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.Text())
    date=db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,title,body):
        self.title=title
        self.body=body

class ArticleSchema(ma.Schema):
    class Meta:
        fields=('id','title','body','date')

article_schema=ArticleSchema()
articles_schema=ArticleSchema(many=True)

@app.route("/get",methods=['GET'])
def get_articles():
    all_articles=Article.query.all()
    results=articles_schema.dump(all_articles)
    return jsonify(results)

@app.route("/get/<id>/",methods=['GET'])
def post_details(id):
    article=Article.query.get(id)
    results=article_schema.dump(article)
    return jsonify(results)
    
@app.route("/add",methods=['POST'])
def add_article():
    title=request.json['title']
    body=request.json['body']

    articles=Article(title,body)
    db.session.add(articles)
    db.session.commit()

    return article_schema.jsonify(articles)

@app.route("/update/<id>/",methods=['PUT'])
def update_article(id):
    article=Article.query.get(id)
    title=request.json['title']
    body=request.json['body']
    article.title=title
    article.body=body
    db.session.commit()

    results=article_schema.dump(article)
    return jsonify(results)

@app.route("/delete/<id>/",methods=['DELETE'])
def delete_article(id):
    article=Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    results=article_schema.dump(article)
    return jsonify(results)

if __name__=="__main__":
    app.run(debug=True)
