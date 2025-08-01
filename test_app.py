import unittest
from app import app, processed_warnings # Importieren der App und die Liste aus app.py

class NotificationServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        processed_warnings.clear()  # jeder Test soll bereinigt werden

    def test_warning_notification_forwarded(self):
        response = self.app.post('/notify', json={
            "Type": "Warning",
            "Name": "Test Warning",
            "Description": "TEST WARNING FOR FORWARDED NOTIFICATION"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("WARNING notification forwarded", response.get_json()['message'])
        self.assertEqual(len(processed_warnings), 1)
        self.assertEqual(processed_warnings[0]["Name"], "Test Warning")

if __name__ == '__main__':
    unittest.main()