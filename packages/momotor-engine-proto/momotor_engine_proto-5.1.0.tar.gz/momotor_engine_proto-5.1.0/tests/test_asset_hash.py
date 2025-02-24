import pytest

from momotor.rpc.hash import decode as decode_hash, encode as encode_hash
from momotor.rpc.exception import AssetException

from multihash.constants import CODE_HASHES

from proto_test_consts import TEST_CONTENT, INVALID_HASH_VALUES


@pytest.mark.parametrize(["hash_value", "msg"], [
    pytest.param(hash_value, msg, id=id_)
    for (hash_value, msg, id_) in INVALID_HASH_VALUES
])
def test_asset_hash_decode_invalid_values(hash_value, msg):
    with pytest.raises(AssetException, match=r'RPC Exception \(asset\) {}'.format(msg)):
        decode_hash(hash_value)


def make_test_hash_encode_decode_params():
    from momotor.rpc.hash.funcs import SUPPORTED_HASH_FUNCS, _MH_CODE_TO_ALGO

    for code, algo in _MH_CODE_TO_ALGO.items():
        yield pytest.param(
            algo,
            code,
            id=CODE_HASHES[code],
            marks=pytest.mark.xfail(
                condition=code not in SUPPORTED_HASH_FUNCS,
                reason='Unsupported hash function',
                strict=False,
            )
        )


@pytest.mark.parametrize(["hash_algo", "hash_code"], list(make_test_hash_encode_decode_params()))
def test_asset_hash_encode_decode(hash_algo, hash_code):
    hash_func = hash_algo(TEST_CONTENT)
    hash_value = encode_hash(hash_func)

    decoded_digest, decoded_hash_code = decode_hash(hash_value)

    assert decoded_hash_code == hash_code
    assert hash_func.digest() == decoded_digest
