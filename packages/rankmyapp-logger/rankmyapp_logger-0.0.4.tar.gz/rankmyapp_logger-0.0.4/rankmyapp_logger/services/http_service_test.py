import unittest
import json

from services.http_service import HttpService

class TestHttpService(unittest.TestCase):
    def test_http_service_defined(self):
        service = HttpService('https://jsonplaceholder.typicode.com')
        http = service.of()
        self.assertIsNotNone(http)

    def test_http_service_get_request(self):
        service = HttpService('https://jsonplaceholder.typicode.com')
        opts = {'method': 'GET', 'headers': {'Content-Type': 'application/json'}}
        data = service.request({
            'path': 'posts',
            **opts,
        })

        self.assertIsNotNone(data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertIsInstance(json.loads(data.get('body')), list)

    def test_http_service_post_request(self):
        service = HttpService('https://jsonplaceholder.typicode.com')
        opts = {'method': 'POST', 'headers': {'Content-Type': 'application/json'}}
        data = service.request({
            'path': 'posts',
            'body': {'title': 'foo', 'body': 'bar', 'userId': 1},
            **opts,
        })

        self.assertIsNotNone(data)
        self.assertEqual(data.get('status_code'), 201)
        self.assertIsInstance(json.loads(data.get('body')), dict)

if __name__ == '__main__':
    unittest.main()