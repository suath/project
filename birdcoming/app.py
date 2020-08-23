from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)

# URL 별로 함수명이 같거나,
# route('/') 등의 주소가 같으면 안됩니다.
client = MongoClient('localhost', 27017)
db = client.bird_comming


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/message', methods=["POST"])
def set_message():
    # 클라이언트가 전달한 username, contents를 변수에 저장한다.
    username_receive = request.form['username_give']
    contents_receive = request.form['contents_give']

    # DB에 저장할 대상을 만든다.
    doc = {
        'username': username_receive,
        'contents': contents_receive,
        # '지금 시각'을 created_at 이라는 이름으로 함께 저장한다.
        'created_at': datetime.now()
    }

    # DB에 메모를 저장한다.
    db.messages.insert_one(doc)

    # 성공 메시지를 반환한다.
    return jsonify({'result': 'success', 'msg': '메시지 작성에 성공하였습니다!'})


@app.route('/message', methods=["GET"])
def get_messages():
		# 지금 시각 구하기
    date_now = datetime.now()
		# 24시간 전 구하기
    date_before = date_now - timedelta(days=1)
    messages = list(db.messages.find({'created_at': {'$gte': date_before, '$lte': date_now}}, {'_id': False}).sort('created_at', -1))
    return jsonify({'result': 'success', 'messages': messages})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
