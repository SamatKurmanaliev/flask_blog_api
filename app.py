from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='secret_key'
db.init_app(app)
migrate=Migrate(app,db)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)


# Модель Comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post=db.relationship('Post',backref=db.backref('comments',lazy='dynamic'))
    content = db.Column(db.Text)


# Модель Blog
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post', backref='blog', lazy=True)



# Создание таблиц в базе данных

# Создание нового объекта Post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data['title']
    content = data['content']

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'})


# Получение всех объектов Post
@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    results = []

    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content
        }
        results.append(post_data)

    return jsonify(results)


# Получение конкретного объекта Post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content
    }

    return jsonify(post_data)


# Обновление объекта Post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    post.title = data['title']
    post.content = data['content']

    db.session.commit()

    return jsonify({'message': 'Post updated successfully'})


# Удаление объекта Post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'})


# Запуск сервера Flask
with app.app_context():
    db.create_all()
    app.run(debug=True)
