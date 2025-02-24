import pytest
from proto_test_consts import TEST_CONTENT

from momotor.rpc.hash import decode as decode_hash
from momotor.rpc.hash import encode_content, is_identity, is_identity_code


def test_asset_hash_identity():
    encoded = encode_content(TEST_CONTENT, use_identity=True)
    assert is_identity(encoded)
    digest, hash_code = decode_hash(encoded)
    assert is_identity_code(hash_code)
    assert TEST_CONTENT == digest


@pytest.mark.parametrize(["hash_value", "expected"], [
    pytest.param(
        encode_content(TEST_CONTENT, use_identity=False), False,
        id="normal content"
    ),
    pytest.param(
        encode_content(TEST_CONTENT, use_identity=True), True,
        id="identity encoded content"
    )
])
def test_asset_hash_is_identity(hash_value, expected):
    assert expected == is_identity(hash_value)
