import json

import pytest

from jose.backends.native import HMACKey
from jose.constants import ALGORITHMS
from jose.exceptions import JOSEError


class TestHMACAlgorithm:
    def test_non_string_key(self):
        with pytest.raises(JOSEError):
            HMACKey(object(), ALGORITHMS.HS256)

    def test_RSA_key(self):
        key = "-----BEGIN PUBLIC KEY-----"
        key += "\n\n\n-----END PUBLIC KEY-----"
        with pytest.raises(JOSEError):
            HMACKey(key, ALGORITHMS.HS256)

        key = "-----BEGIN RSA PUBLIC KEY-----"
        key += "\n\n\n-----END RSA PUBLIC KEY-----"
        with pytest.raises(JOSEError):
            HMACKey(key, ALGORITHMS.HS256)

        key = "-----BEGIN CERTIFICATE-----"
        key += "\n\n\n-----END CERTIFICATE-----"
        with pytest.raises(JOSEError):
            HMACKey(key, ALGORITHMS.HS256)

        key = "ssh-rsa"
        with pytest.raises(JOSEError):
            HMACKey(key, ALGORITHMS.HS256)

    def test_to_dict(self):
        passphrase = "The quick brown fox jumps over the lazy dog"
        encoded = "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZw"
        key = HMACKey(passphrase, ALGORITHMS.HS256)

        as_dict = key.to_dict()
        assert "alg" in as_dict
        assert as_dict["alg"] == ALGORITHMS.HS256

        assert "kty" in as_dict
        assert as_dict["kty"] == "oct"

        assert "k" in as_dict
        assert as_dict["k"] == encoded

        # as_dict should be serializable to JSON
        json.dumps(as_dict)
