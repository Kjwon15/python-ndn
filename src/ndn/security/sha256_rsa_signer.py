from typing import List
from ..encoding.signer import Signer
from ..encoding.ndn_format_0_3 import KeyLocator, SignatureType
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15


class Sha256WithRsaSigner(Signer):
    def write_signature_info(self, signature_info, **kwargs):
        signature_info.key_locator = KeyLocator()
        signature_info.key_locator.name = kwargs['key_name']

    def get_signature_value_size(self, **kwargs):
        key = RSA.import_key(kwargs['key_der'])
        return key.size_in_bytes()

    def write_signature_value(self, wire: memoryview, contents: List[memoryview], **kwargs):
        key = RSA.import_key(kwargs['key_der'])
        h = SHA256.new()
        for blk in contents:
            h.update(blk)
        signature = pkcs1_15.new(key).sign(h)
        wire[:] = signature


def register():
    Signer.register(SignatureType.SHA256_WITH_RSA, Sha256WithRsaSigner())
