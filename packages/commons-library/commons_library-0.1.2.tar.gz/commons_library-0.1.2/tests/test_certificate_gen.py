import logging
import unittest
from pathlib import Path
import tempfile

TEMP_DIR: Path = Path(tempfile.mkdtemp())
logging.getLogger(__file__).warning(f"Temporary directory: {TEMP_DIR.resolve()}")


class TestSSL(unittest.TestCase):
    def test_local_cert_gen(self):
        from commons.net import certs

        files = certs.get_cert(TEMP_DIR)

        assert files.cert.exists()
        assert files.key.exists()
