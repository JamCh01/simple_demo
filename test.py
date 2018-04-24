import requests


class Test():
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000/{}'

    def api_add(self):
        r = requests.post(
            url=self.base_url.format('add'),
            data='{"value_array":[{"value":12},{"value":18},{"value":10}]}')
        assert r.json().get('result') == 40

    def api_date(self):
        import datetime
        r = requests.get(url=self.base_url.format('date'))
        assert r.json().get('date') == datetime.datetime.now().strftime(
            '%Y-%m-%d')

    def api_chat(self):
        import json
        msgs = [
            '输入的句子中含有中文 “您好”，输出回复“您好，您吃了吗？”',
            '输入的句子中含有中文 “再见”，输出回复“回见了您内。”',
            '输入的句子如果同时含有中文 “再见”和“您好”，输出回复“天气不错。”',
        ]
        results = [
            '您好，您吃了吗？',
            '回见了您内。',
            '天气不错。',
        ]
        for x, y in zip(msgs, results):
            data = json.dumps({'msg': x})
            r = requests.post(url=self.base_url.format('chat'), data=data)
            assert r.json().get('result') == y