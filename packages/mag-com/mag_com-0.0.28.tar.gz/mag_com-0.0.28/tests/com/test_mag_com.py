import unittest
from mag_com.com.mag_com import MagCom


class TestMagCom(unittest.TestCase):
    def test_get_password_info(self):
        client_id = 'root'

        password_info = MagCom.get_password_info(client_id)
        print(password_info)


if __name__ == '__main__':
    unittest.main()