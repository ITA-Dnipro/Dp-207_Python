from flask_hotels_service.main import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_response(self):
        tester = create_app().test_client(self)
        response = tester.get('/api/get_all_hotels')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_content_type(self):
        tester = create_app().test_client(self)
        response = tester.get('/api/get_all_hotels')
        self.assertEqual(response.content_type, "application/json")

    def test_data_return(self):
        tester = create_app().test_client(self)
        response = tester.get('/api/get_all_hotels')
        self.assertIn(b'hotels', response.data)

if __name__ == '__main__':
    unittest.main()
