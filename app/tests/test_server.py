import json
import unittest
import logging
from app.server import create_app

log = logging.getLogger(__name__)


class TestMUDServer(unittest.TestCase):
    def setUp(self):
        config = {
            "room": "Test Room",
            "objects": {"test_object": "A test object"},
        }
        self.app = create_app(config).test_client()

    def test_command_protocol_connect(self):
        # Test protocol_connect command
        response = self.app.post(
            "/command",
            data=json.dumps({"command": "protocol_connect"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data["error"])
        self.assertIn("instructions", data.keys())

    def test_command_invalid_command(self):
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
        self.assertTrue(data["error"])
        self.assertIn("Unknown command", data["error"])

    def test_command_protocol_disconnect(self):
        # Test protocol_disconnect command
        response = self.app.post(
            "/command",
            data=json.dumps({"command": "protocol_disconnect"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data["error"])


if __name__ == "__main__":
    unittest.main()
