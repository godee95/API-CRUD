from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from time import time

from pymongo import MongoClient
client = MongoClient('')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework/click", methods=["DELETE"])
def remove_comment():
    num_receive = request.form['num_give']
    db.fanbook.delete_one({'num': int(num_receive)})

    return jsonify({'msg': '삭제 완료!'})

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    count = time() * 10000000

    doc = {
        'num':count,
        'name':name_receive,
        'comment':comment_receive,
    }
    db.fanbook.insert_one(doc)

    return jsonify({'msg':'기록 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    fanbook_list = list(db.fanbook.find({}, {'_id': False}))
    return jsonify({'fanbooks':fanbook_list})

@app.route("/homework", methods=["PUT"])
def override_comment():
    num_receive = request.form['num_give']
    update_comment_receive = request.form['update_comment']
    update_name_receive = request.form['update_name']
    db.fanbook.update_one({'num':int(num_receive)}, {'$set':{'comment':update_comment_receive}})
    db.fanbook.update_one({'num': int(num_receive)}, {'$set': {'name': update_name_receive}})
    return jsonify({'result':'success', 'msg':'메세지 변경에 성공하였습니다'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)