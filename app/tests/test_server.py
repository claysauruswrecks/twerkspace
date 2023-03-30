import json
import unittest
from app.server import create_app


class TestMUDServer(unittest.TestCase):
    def setUp(self):
        config = {
            "room": "Test Room",
            "objects": {"test_object": "A test object"},
        }
        self.app = create_app(config).test_client()

    def test_command(self):
        # Test a valid command
        response = self.app.post(
            "/command",
            data=json.dumps(
                {"user_id": "user_1", "command": "protocol_connect"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('"instructions":', data)

        # Test an invalid command
        response = self.app.post(
            "/command",
            data=json.dumps(
                {"user_id": "user_1", "command": "invalid_command"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("Unknown command", data)


if __name__ == "__main__":
    unittest.main()
