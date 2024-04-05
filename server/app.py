from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.order_by('created_at').all()
        result = []
        for message in all_messages:
            result.append(message.to_dict())
        return result, 200
    elif request.method == 'POST':
        json_data = request.get_json()
        new_msg = Message(
            body = json_data.get('body'),
            username = json_data.get('username')
        )
        db.session.add(new_msg)
        db.session.commit()
        return new_msg.to_dict(), 201

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter_by(id=id).first()
    if request.method == 'GET':
        return msg.to_dict(), 200
    elif request.method == 'PATCH':
        json_data = request.get_json()
        setattr(msg, 'body', json_data['body'])
        db.session.add(msg)
        db.session.commit()
        return msg.to_dict(), 200
    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        return {}, 204

if __name__ == '__main__':
    app.run(port=5555)
