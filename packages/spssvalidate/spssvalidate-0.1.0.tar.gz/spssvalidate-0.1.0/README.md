Copyright © 2025 Sumedh Patil, Aipresso Limited, UK

The `spssvalidate` library is designed to validate the authenticity, integrity, and security of decoded star maps. It ensures that only legitimate star maps are accepted by performing session ID validation, blockchain verification, anti-tampering checks, time-based expiry, and encryption key validation.

## Installation

```bash
pip install -r requirements.txt
```

USAGE:
from spssvalidate.validator import Validator
from spssvalidate.ai_model import AIModel

validator = Validator(
expected_session_id="valid_session_id",
expiry_time=3600,
blockchain_network=MockBlockchainNetwork(),
encryption_module=MockEncryptionModule(),
ai_model=AIModel()
)

result, message = validator.validate(
decoded_data={"stars": [{"x": 1, "y": 2}]},
decoded_session_id="valid_session_id",
decoded_hash="valid_hash",
timestamp=time.time(),
decoded_key="valid_key"
)

print(result, message)
