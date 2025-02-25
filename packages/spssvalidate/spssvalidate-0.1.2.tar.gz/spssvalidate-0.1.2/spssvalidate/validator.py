import time
from hashlib import sha256

class Validator:
    def __init__(self, expected_session_id, expiry_time, blockchain_network=None, encryption_module=None, ai_model=None):
        self.expected_session_id = expected_session_id
        self.expiry_time = expiry_time
        self.blockchain_network = blockchain_network
        self.encryption_module = encryption_module
        self.ai_model = ai_model

    def validate_session_id(self, decoded_session_id):
        """Validate the session ID."""
        return decoded_session_id == self.expected_session_id

    def verify_blockchain_hash(self, decoded_hash):
        """Verify the embedded blockchain hash against the network."""
        if not self.blockchain_network:
            return True  # Blockchain verification is optional
        return self.blockchain_network.verify(decoded_hash)

    def detect_tampering(self, decoded_data):
        """Detect anomalies in decoded data using AI models."""
        if not self.ai_model:
            return True  # AI model is optional
        return self.ai_model.analyze(decoded_data)

    def check_expiry(self, timestamp):
        """Ensure the star map is used within the valid time window."""
        current_time = time.time()
        return current_time <= timestamp + self.expiry_time

    def validate_encryption_key(self, decoded_key):
        """Verify cryptographic signatures or encryption keys."""
        if not self.encryption_module:
            return True  # Encryption module is optional
        return self.encryption_module.verify(decoded_key)

    def validate(self, decoded_data, decoded_session_id, decoded_hash, timestamp, decoded_key):
        """Orchestrate the entire validation process."""
        if not self.validate_session_id(decoded_session_id):
            return False, "Invalid session ID"
        
        if not self.verify_blockchain_hash(decoded_hash):
            return False, "Blockchain hash verification failed"
        
        if not self.detect_tampering(decoded_data):
            return False, "Tampering detected"
        
        if not self.check_expiry(timestamp):
            return False, "Star map expired"
        
        if not self.validate_encryption_key(decoded_key):
            return False, "Invalid encryption key"
        
        return True, "Validation successful"