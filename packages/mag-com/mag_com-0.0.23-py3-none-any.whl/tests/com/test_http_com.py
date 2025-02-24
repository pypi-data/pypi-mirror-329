import unittest
from io import BytesIO

from mag_com.com.http_com import HttpCom


class TestHttpCom(unittest.TestCase):
    def setUp(self):
        self.http_com = HttpCom()

    def test_get(self):
        response = self.http_com.get("https://jsonplaceholder.typicode.com/posts")
        self.assertIsNotNone(response)
        self.assertIn("userId", response)

    def test_post_with_data(self):
        response = self.http_com.post_with_data("https://jsonplaceholder.typicode.com/posts", data='{"title": "foo", "body": "bar", "userId": 1}')
        self.assertIsNotNone(response)
        self.assertIn("id", response)

    def test_download_to_file(self):
        self.http_com.download_to_file("https://via.placeholder.com/150", "downloaded_image.png")
        with open("downloaded_image.png", "rb") as f:
            content = f.read()
        self.assertGreater(len(content), 0)

    def test_download_to_stream(self):
        stream = BytesIO()
        self.http_com.download_to_stream("https://via.placeholder.com/150", stream)
        self.assertGreater(stream.tell(), 0)

if __name__ == "__main__":
    unittest.main()
