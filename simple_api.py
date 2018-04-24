from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Add(Resource):
    def post(self):
        nums = request.get_json(force=True)
        values = nums.get('value_array')
        return jsonify(result=sum([i.get('value') for i in values]))


class Now(Resource):
    def get(self):
        import datetime
        return jsonify(date=datetime.datetime.now().strftime('%Y-%m-%d'))


class Chat(Resource):
    def post(self):
        msg = request.get_json(force=True).get('msg')
        action = ''
        if '您好' in msg and '再见' in msg:
            action = '天气不错。'
        elif '您好' in msg:
            action = '您好，您吃了吗？'
        elif '再见' in msg:
            action = '回见了您内。'

        return jsonify(result=action)


api.add_resource(Now, '/get_date')
api.add_resource(Add, '/add')
api.add_resource(Chat, '/chat')

if __name__ == '__main__':
    app.run(debug=True)