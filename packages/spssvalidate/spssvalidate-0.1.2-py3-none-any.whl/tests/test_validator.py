import unittest
import time
from spssvalidate.validator import Validator
from spssvalidate.ai_model import AIModel

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator(
            expected_session_id="valid_session_id",
            expiry_time=3600,
            blockchain_network=MockBlockchainNetwork(),
            encryption_module=MockEncryptionModule(),
            ai_model=AIModel()
        )

    def test_validate_session_id(self):
        self.assertTrue(self.validator.validate_session_id("valid_session_id"))
        self.assertFalse(self.validator.validate_session_id("invalid_session_id"))

    def test_verify_blockchain_hash(self):
        self.assertTrue(self.validator.verify_blockchain_hash("valid_hash"))
        self.assertFalse(self.validator.verify_blockchain_hash("tampered_hash"))

    def test_detect_tampering(self):
        self.assertTrue(self.validator.detect_tampering({"stars": [{"x": 1, "y": 2}]}))

    def test_check_expiry(self):
        self.assertTrue(self.validator.check_expiry(time.time() - 1000))
        self.assertFalse(self.validator.check_expiry(time.time() - 4000))

    def test_validate_encryption_key(self):
        self.assertTrue(self.validator.validate_encryption_key("valid_key"))
        self.assertFalse(self.validator.validate_encryption_key("invalid_key"))

class MockBlockchainNetwork:
    def verify(self, decoded_hash):
        return decoded_hash == "valid_hash"

class MockEncryptionModule:
    def verify(self, decoded_key):
        return decoded_key == "valid_key"

if __name__ == "__main__":
    unittest.main()