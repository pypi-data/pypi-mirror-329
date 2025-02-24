TEST_CONTENT = b'123456789'

INVALID_HASH_VALUES = [
    (b'', r'multihash must be greater than 3 bytes', 'empty string'),
    (b'$$$', r'illegal hash value', 'invalid base58'),
    (b'5dqfkrAhhaZVunZXPHwVY13p5XPHGC', r'Inconsistent multihash length 20 != 19', 'Invalid (too short) size'),
    (b'5dxoUL5KGWaADxURLzxCHp6jvQTw9z', r'Inconsistent multihash length 20 != 21', 'Invalid (too long) size'),
    (b'ztU41qKSJ8ZdVmMjwRg75an4', r'Unsupported hash code 24 \(shake-128\)', "Unsupported codec shake_128"),
    (b'fzhnMYSx49yDxjxu59u9wdfxV8', r'Unsupported hash code 213', "Unsupported codec md5"),
    (b'FL8X6Ae', r'Unsupported hash code 127', "Undefined codec 127"),
    (b'3Bz6wHvpA', r'Unsupported hash code 255', "Undefined codec 255"),
]
