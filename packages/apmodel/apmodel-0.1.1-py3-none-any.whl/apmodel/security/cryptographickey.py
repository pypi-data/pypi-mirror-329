from pyfill import datetime
from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    PublicKeyTypes,
)


class CryptographicKey:
    def __init__(
        self,
        type: str = "CryptographicKey",
        id: Optional[str] = None,
        owner: Optional[str] = None,
        publicKeyPem: Optional[str] = None,
        **kwargs,
    ):
        self.type = type
        self.id = id
        if publicKeyPem:
            self.publicKeyPem: Optional[PublicKeyTypes] = (
                serialization.load_pem_public_key(
                    publicKeyPem.encode("utf-8")
                    if isinstance(publicKeyPem, str)
                    else publicKeyPem
                )
            )
        else:
            self.publicKeyPem = None
        self.owner = owner
        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self, _extras: Optional[dict] = None):
        instance_vars = vars(self).copy()
        data = {}

        for key, value in instance_vars.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat() + "Z"
                elif isinstance(value, PublicKeyTypes):
                    data[key] = value.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
                elif (
                    isinstance(value, list)
                    or isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)

        _extras = _extras or {}
        for key, value in self._extras.items():
            if value is not None:
                if isinstance(value, datetime.datetime.datetime):
                    data[key] = value.isoformat() + "Z"
                elif isinstance(value, list):
                    data[key] = [
                        item.to_dict(_extras=item._extras)
                        if hasattr(item, "to_dict")
                        else item
                        for item in value
                    ]
                elif (
                    isinstance(value, dict)
                    or isinstance(value, int)
                    or isinstance(value, bool)
                ):
                    data[key] = value
                else:
                    data[key] = str(value)
        return data
