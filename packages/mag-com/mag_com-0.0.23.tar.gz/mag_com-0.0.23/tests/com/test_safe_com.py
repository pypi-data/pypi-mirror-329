import unittest

from mag_tools.bean.easy_map import EasyMap

from mag_com.com.safe_com import SafeCom


class TestHttpCom(unittest.TestCase):
    def setUp(self):
        prop = {"host": "192.168.0.198",
                "port": 9000,
                "ssl": False,
                "clientType": "Windows",
                "userType": "Org",
                "appId": "Hisim"}
        self.safe_com = SafeCom()
        self.safe_com.init(prop)

    def test_post_string(self):
        results = self.safe_com.post("", EasyMap(), str)
        print(results)