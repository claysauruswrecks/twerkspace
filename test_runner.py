import logging
import sys
import unittest

if __name__ == "__main__":
    if "--debug" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
        sys.argv.remove("--debug")
    test_suite = unittest.defaultTestLoader.discover("app.tests")
    unittest.TextTestRunner().run(test_suite)
