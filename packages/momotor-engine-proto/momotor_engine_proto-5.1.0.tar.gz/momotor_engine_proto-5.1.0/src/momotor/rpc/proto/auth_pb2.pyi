from google.protobuf import empty_pb2 as _empty_pb2
from momotor.rpc.proto import exception_pb2 as _exception_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerInfoResponse(_message.Message):
    __slots__ = ("version", "protoVersion", "chunkSize", "maxIdHashLen", "hashFunc", "progressUpdateInterval")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PROTOVERSION_FIELD_NUMBER: _ClassVar[int]
    CHUNKSIZE_FIELD_NUMBER: _ClassVar[int]
    MAXIDHASHLEN_FIELD_NUMBER: _ClassVar[int]
    HASHFUNC_FIELD_NUMBER: _ClassVar[int]
    PROGRESSUPDATEINTERVAL_FIELD_NUMBER: _ClassVar[int]
    version: str
    protoVersion: str
    chunkSize: int
    maxIdHashLen: int
    hashFunc: _containers.RepeatedScalarFieldContainer[int]
    progressUpdateInterval: int
    def __init__(self, version: _Optional[str] = ..., protoVersion: _Optional[str] = ..., chunkSize: _Optional[int] = ..., maxIdHashLen: _Optional[int] = ..., hashFunc: _Optional[_Iterable[int]] = ..., progressUpdateInterval: _Optional[int] = ...) -> None: ...

class AuthenticateRequest(_message.Message):
    __slots__ = ("apiKey", "challengeResponse")
    APIKEY_FIELD_NUMBER: _ClassVar[int]
    CHALLENGERESPONSE_FIELD_NUMBER: _ClassVar[int]
    apiKey: str
    challengeResponse: bytes
    def __init__(self, apiKey: _Optional[str] = ..., challengeResponse: _Optional[bytes] = ...) -> None: ...

class Challenge(_message.Message):
    __slots__ = ("value", "salt")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SALT_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    salt: str
    def __init__(self, value: _Optional[bytes] = ..., salt: _Optional[str] = ...) -> None: ...

class AuthenticateResponse(_message.Message):
    __slots__ = ("challenge", "authToken", "exception")
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    AUTHTOKEN_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    challenge: Challenge
    authToken: str
    exception: _exception_pb2.Exception
    def __init__(self, challenge: _Optional[_Union[Challenge, _Mapping]] = ..., authToken: _Optional[str] = ..., exception: _Optional[_Union[_exception_pb2.Exception, _Mapping]] = ...) -> None: ...
