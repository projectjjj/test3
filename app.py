from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock2

from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def save_post():
    post_url_receive = request.form['post_url_give']
    post_comment_receive = request.form['post_comment_give']
    views_receive = request.form['views_give']
    time = datetime.today().strftime("%Y.%m.%d %H:%M:%S")
    doc = {'제목': post_url_receive, '내용': post_comment_receive, '날짜' : time, '조회수' : views_receive}
    db.users.insert_one(doc)
    return {"result": "포스팅 성공!"}


@app.route('/post', methods=['GET'])
def get_post():
    post_list = list(db.users.find({}, {'_id': False}).sort('날짜', -1))
    return {"result": post_list}

@app.route('/post', methods=['DELETE'])
def delete_post():
    titie_receive = request.form['delete_give']
    db.users.delete_one({'제목': titie_receive})
    return {"result": "삭제하였습니다!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)