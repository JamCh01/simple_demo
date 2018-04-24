import requests
import unittest
import datetime

base_url = 'http://127.0.0.1:5000/{}'



class Test(unittest.TestCase):
    def test_add(self):
        r = requests.post(
            url=base_url.format('add'),
            data='{"value_array":[{"value":12},{"value":18},{"value":10}]}')
        self.assertEqual(r.json().get('result'), 40)

    def test_date(self):
        r = requests.get(url=base_url.format('get_date'))
        self.assertEqual(r.json().get('date'),
                         datetime.datetime.now().strftime('%Y-%m-%d'))

    def test_chat(self):
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
            r = requests.post(url=base_url.format('chat'), data=data)
            self.assertEqual(r.json().get('result'), y)


if __name__ == '__main__':
    unittest.main()
