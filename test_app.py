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

    def test_info_notification_not_forwarded(self):
        response = self.app.post('/notify', json={
            "Type": "Info",
            "Name": "Test Info",
            "Description": "TEST INFO"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Info notification received but not forwarded", response.get_json()['message'])
        self.assertEqual(len(processed_warnings), 0)

    def test_missing_required_field(self):
        response = self.app.post('/notify', json={
            "Type": "Warning",
            "Name": "Test Name"
            # "Description" keine
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required field: 'Description'", response.get_json()['error'])
        self.assertEqual(len(processed_warnings), 0)

    def test_empty_json_payload(self):
        response = self.app.post('/notify', json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual("Something is wrong with the JSON payload", response.get_json()['error'])
        self.assertEqual(len(processed_warnings), 0)

    def test_unknown_type_ignored(self):
        response = self.app.post('/notify', json={
            "Type": "Critical",
            "Name": "System Crash",
            "Description": "The system crashed unexpectedly"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Notification of type 'Critical' received but not forwarded", response.get_json()['message'])
        self.assertEqual(len(processed_warnings), 0)

    def test_health_check(self):
        response = self.app.get('/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], "healthy")

if __name__ == '__main__':
    unittest.main()