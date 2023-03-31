import json
import logging
import unittest
from uuid import uuid4

import redis

from app import settings
from app.server import create_app

log = logging.getLogger(__name__)


class TestMUDServer(unittest.TestCase):
    def setUp(self):
        self.world_id = str(uuid4())
        config = {
            "room": "Test Room",
            "objects": [{"test_object": "A test object"}],
            "world_id": self.world_id,
        }
        self.app = create_app(config).test_client()
        self.redis = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
        )
        self.redis.flushdb()

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

        self.assertEqual(
            len(json.loads(self.redis.get(f"{self.world_id}:users"))), 1
        )

        response2 = self.app.post(
            "/command",
            data=json.dumps({"command": "protocol_connect"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data["error"])
        self.assertIn("instructions", data.keys())

        self.assertEqual(
            len(json.loads(self.redis.get(f"{self.world_id}:users"))), 2
        )

    # def test_command_invalid_command(self):
    #     # Connect to the server first
    #     response = self.app.post(
    #         "/command",
    #         data=json.dumps({"command": "protocol_connect"}),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(
    #         len(json.loads(self.redis.get(f"{self.world_id}:users"))), 1
    #     )
    #     response2 = self.app.get(
    #         "/users",
    #         content_type="application/json",
    #     )
    #     import pdb

    #     pdb.set_trace()
    #     # Test an invalid command
    #     response = self.app.post(
    #         "/command",
    #         data=json.dumps(
    #             {"user_id": "User_1", "command": "invalid_command"}
    #         ),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertTrue(data["error"])
    #     self.assertIn("Unknown command", data["error"])

    # def test_command_protocol_disconnect(self):
    #     # Test protocol_disconnect command when not connected
    #     response = self.app.post(
    #         "/command",
    #         data=json.dumps(
    #             {"user_id": "user_1", "command": "protocol_disconnect"}
    #         ),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertTrue(data["error"])

    def test_command_look(self):
        # Test protocol_look command
        pass


if __name__ == "__main__":
    unittest.main()
