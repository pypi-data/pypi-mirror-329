# CHANGELOG


## v5.1.0 (2025-02-24)


## v5.1.0-rc.4 (2025-02-11)

### Bug Fixes

- Enum value 0 is special and cannot be used for normal values
  ([`0c4fd6d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0c4fd6d66b9026e4187e197e63953775461bc9d0))

### Chores

- Update pytest options
  ([`9998f6a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/9998f6a7912722c57bf26ff0ec5ce1ea52316d02))

### Refactoring

- Update type hint for toolsets_to_message function
  ([`8843b15`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/8843b154cb80ddea4c1b26bb09eb31a7908832a8))


## v5.1.0-rc.3 (2024-12-17)

### Bug Fixes

- Add missing reference to stats.proto
  ([`c1ab04e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/c1ab04e913938288a6f7786288c8abd34ea28f19))

- Python 3.9 compatibility regression
  ([`a7488bc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a7488bcfb91d1c9bc7fb2564359a90598a8b5b8a))

### Features

- Add rank field to GetTaskRequest
  ([`8bcb7d8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/8bcb7d877fe56269a342eb0beb8c6697833a6244))

### Refactoring

- Improve type hinting across multiple files
  ([`b9e3564`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/b9e3564a89123e879b368f12e8b3cbf46b442967))


## v5.1.0-rc.2 (2024-11-29)

### Chores

- Add VSCode task for compiling Protobuf files
  ([`4e3bfe1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/4e3bfe18f1498fc926881d6e1a985a85121f0c7b))

### Features

- Add statistics RPC method and corresponding protobuf definitions
  ([`f58f7b6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/f58f7b688b7af233b20217cdddcc815977f24e57))


## v5.1.0-rc.1 (2024-11-26)

### Features

- Add resource management functionality with update request and response
  ([`c734461`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/c734461fb153221dd2af117af05e54de2fd394bd))

- Add stub files for generated protobuf files
  ([`07f50e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/07f50e0a98df7b8aa21d25b4e97f8d92e57f550e))


## v5.0.0 (2024-04-16)


## v5.0.0-rc.2 (2024-03-21)

### Chores

- Update dependencies
  ([`e4877cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/e4877cb9da2f603b18a0bf2dead3dd1c9cb60d92))

### Features

- Convert to PEP420 namespace packages
  ([`96e50c1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/96e50c14c79526071eaab3527b4c1dc922c0097f))

requires all other momotor.* packages to be PEP420 too

BREAKING CHANGE: convert to PEP420 namespace packages

- Upgrade to latest GRPC version
  ([`8e2d7ef`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/8e2d7ef5b69f045928da34c0e24a46d907ed3ea4))

### Refactoring

- Replace all deprecated uses from typing (PEP-0585)
  ([`67e3b4f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/67e3b4ffcc10db8d1db5f4cb625c6ccaabc280d2))


## v5.0.0-rc.1 (2024-02-05)

### Chores

- Add Python 3.10 and 3.11 classifiers
  ([`0294e4a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0294e4ab9b570519eba6f0f4db8b3d6f2b7905fa))

### Features

- Drop Python 3.8 support, test with Python 3.12
  ([`c4ddf3e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/c4ddf3e51998a5d5b82b78d5390e31897ec11ca3))

BREAKING CHANGE: Requires Python 3.9+

### Refactoring

- Update type hints for Python 3.9
  ([`d075761`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/d075761af9a246be88a41f37eca23bc0a93b4c3d))

### Testing

- Update to latest Pytest
  ([`0cbae15`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0cbae150213857f8c2df03f836801342e31fc8b3))

### Breaking Changes

- Requires Python 3.9+


## v4.4.0 (2022-03-14)

### Bug Fixes

- Handle missing tool message
  ([`f85d5a6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/f85d5a6451264fee98e39323f6a1b817b58a844f))

### Chores

- Cleanup CHANGELOG.md [skip-ci]
  ([`be95be9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/be95be97949ed68a5fa37bd387a6ddc553398086))

- Link to documentation with the correct version number
  ([`aeaf50f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/aeaf50f56650236abd5ddf6132de8cbff65b7dcf))

### Features

- Add tool list to GetTaskResponse message
  ([`baf21b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/baf21b2f5dd63460d0725c0e1f3c18f8a49d836b))

- Change tool message into toolset
  ([`16b77aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/16b77aa2730cf9b57279c2e104ebea7bd2fcd87e))

- Move `tools_to_message` from cli package to proto package
  ([`f943211`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/f9432114feb2975673797789ad323c9675fccc68))

- Use a dataclass to represent tools and aliases
  ([`081e9cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/081e9cbb4ebf22beea7aaa7022eac2af09f39aad))


## v4.3.0 (2021-10-22)

### Chores

- Revert version number
  ([`9d86913`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/9d86913aac924dbc64e2c42eeb0553e41a21d277))

- Update version pin of base58 package
  ([`9abd691`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/9abd6913c4bda31cca9ccf32177c954f60e582aa))

### Features

- Add `taskNumber` field to AssetQuery message
  ([`bd88832`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/bd888327a88d210673e79fbea50559294299f278))

- Extend TaskId message with `taskNumber` field, add helpers to convert step-id with task-number to
  step-task-id (Closes #12)
  ([`35a9c67`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/35a9c6755e37a99a157c8a98a737cdc46d50388d))


## v4.2.1 (2021-10-01)

### Bug Fixes

- Use async logging
  ([`ca7e454`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/ca7e4540f810a5057ccbc58f810be791443f847f))

### Chores

- Project file updated
  ([`a8d6431`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a8d6431c8bc23add9de6918297eb4576ee4223bd))

- Update project files
  ([`11ee9a1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/11ee9a1c5e5e401e3277ea4f716dd69b51214ed5))

- Update project files
  ([`d240cdc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/d240cdce1bde081ba62bffb458a1382a742ec4c3))


## v4.2.0 (2021-03-15)

### Bug Fixes

- Remove unused GetJobRequest/GetJobResponse. Add validator for GetTaskRequest
  ([`7881b14`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/7881b14a134b18ce716ac2f0eef50e545744299e))

### Chores

- Correct url to commit in CHANGELOG.md
  ([`0d3b9a9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0d3b9a9341af01cefe6778878f40a4d8e84d7fdc))

- List Python 3.9 in the classifiers
  ([`e78c1de`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/e78c1deceabf1b7d83ba97fdcf7d7237cc07389a))

- Update protobuf dependency to ~3.15.6, update grpcio-tools dependency to ~1.36.1
  ([`59a2756`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/59a27564c228235663f12d712e76654db3a3910f))

### Features

- Add priority field to CreateJobRequest, JobStatus and GetTaskResponse
  ([`34b35e4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/34b35e4045b2c83364ea9042114950ed0a08f7d4))


## v4.1.1 (2020-11-13)

### Bug Fixes

- Always send pings, even if there was no data
  ([`e004f60`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/e004f6042aec9ddb3c678549e25296159f51a8e0))

### Chores

- Fix url in CHANGELOG.md
  ([`375e8c0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/375e8c01deeb42f5ded75769410ad86b7f6fc968))


## v4.1.0 (2020-11-05)

### Chores

- Rebuild pb2 files
  ([`b724317`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/b724317cce23066e51a4ea6058ce8ec5f98f0ad7))

- Update/move PyCharm module files
  ([`1efb674`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/1efb674da280938f6c4f4e6bbf4d299f0bccec1c))

### Features

- Update grpclib to latest, set a low keepalive time, make it configurable
  ([`7c94095`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/7c94095cb8f02cdf4de39de9caae7b940e9e8de0))


## v4.0.1 (2020-10-23)

### Bug Fixes

- The loop parameter is deprecated
  ([`024d0d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/024d0d317bd07b3d4511568cfd323ef37abeb872))

### Chores

- Update Python SDK
  ([`bf9641a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/bf9641a9b020584d586fdd14cb30da26bd65cdfc))

- Update Python version classifiers
  ([`244b0a8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/244b0a8ba16150100cd7c52a0ac324412564ef18))


## v4.0.0 (2020-08-17)

### Features

- Changed minimum Python requirement to 3.7
  ([`8fcc8b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/8fcc8b20ec150bcc68981716a4fb396aeb981d1c))

BREAKING CHANGE: Requires Python 3.7 or higher

### Breaking Changes

- Requires Python 3.7 or higher


## v3.0.1 (2020-06-29)

### Bug Fixes

- Bump grpclib, grpcio, and protobuf versions
  ([`0108a35`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0108a359b74177abef92ebf2086939a9803f0143))


## v3.0.0 (2020-04-23)

### Chores

- Increase default chunk size from 256KiB to 8MiB
  ([`8f680af`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/8f680afc4ac9f89ded47a0ca6365ab4b705fa13b))

### Features

- Move query related validators into momotor.rpc.validate.query
  ([`0fc268c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0fc268c6476dd3af2269075605d723bb5b3e96c3))

doc: document validators

- Move query related validators into momotor.rpc.validate.query, document validators
  ([`a8ab9e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a8ab9e0ec44db1cec26c42117bf96bef5092d9c5))

BREAKING CHANGE: renamed momotor.rpc.validate.shared to momotor.rpc.validate.base, renamed
  momotor.rpc.validate.types to momotor.rpc.validate.query, moved
  momotor.rpc.validate.shared.validate_query_field() to momotor.rpc.validate.query

### Breaking Changes

- Renamed momotor.rpc.validate.shared to momotor.rpc.validate.base, renamed
  momotor.rpc.validate.types to momotor.rpc.validate.query, moved
  momotor.rpc.validate.shared.validate_query_field() to momotor.rpc.validate.query


## v2.12.0 (2020-03-19)

### Features

- Subclass h2's DummyLogger for compatibility
  ([`5a3f515`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/5a3f51554e3d4648fd0bf2066ce8304603a1422f))


## v2.11.0 (2020-03-13)

### Features

- Add file_reader() and file_writer() utils
  ([`591ae2b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/591ae2b2131bdc804c092d3d6e267caa73a64aa5))

### Refactoring

- Calling task.result() is redundant
  ([`4ee30e5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/4ee30e5a4dc7ac3a558c2dcc9f3166bb52bbbf52))

- Use file_reader() and file_writer() to streamline file I/O (closes
  momotor/engine-py3/momotor-engine-broker#40)
  ([`2f7a6d4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/2f7a6d4725e805759355e25e5c8b64f8c4fa574e))


## v2.10.0 (2020-02-28)

### Bug Fixes

- Do not check for existence of identity encoded content in cache (Closes #8)
  ([`a00be3c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a00be3c9aee40370746c7ea9bfd5509d1262f971))

### Features

- Deprecated ID_HASH_CODE constant, use is_identity_code() instead
  ([`aa6e141`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/aa6e1414b7f67fbf583b5801a4b72e5f17f4ad5c))


## v2.9.0 (2019-10-28)

### Features

- Add 'exclusive' option to SharedLockRequest (closes #7)
  ([`a9733cc`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a9733cc0b8e33dcd931ad1fc699932efc90cc8b3))


## v2.8.0 (2019-10-14)

### Features

- Export DEFAULT_PORT and DEFAULT_SSL_PORT
  ([`0469d14`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/0469d146a71665fcc66791df2486565b133e27f2))


## v2.7.0 (2019-10-14)

### Features

- Add SSL Support
  ([`5812a41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/5812a41c2e6a051d2a69d92dc1166d853c98a221))

### Refactoring

- Typo in comments fixed
  ([`c39027e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/c39027e6c3cc2403e1491a46d07d29df9264980b))


## v2.6.0 (2019-10-10)

### Features

- Upgrade grpclib to version 0.3
  ([`710c99f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/710c99f5c55330deb217ecbb1c674724fcc2ac27))

### Refactoring

- Reduce debug log spam
  ([`d23d0d8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/d23d0d8ba1d6d6a65dd729165fa42fe28cc18263))

- Reduce debug log spam further
  ([`6804e63`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/6804e639f970864a14f0f380d08c586336831e56))

- Use contextlib.asynccontextmanager on Python>=3.7
  ([`9baf0ae`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/9baf0ae4e2eb2a1c694d52df84d5428e48ab2080))


## v2.5.1 (2019-09-26)

### Bug Fixes

- Remove ResourceUnavailableException as a worker cannot report this as an exception
  ([`6326a5c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/6326a5c600796e34bc6fe1cb1cf56e3b17da5b17))


## v2.5.0 (2019-09-24)


## v2.4.0 (2019-09-24)

### Features

- Add resource unavailable RPC exception
  ([`682f821`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/682f82164dad336365d1642ce72c81845da2f364))


## v2.3.1 (2019-09-24)

### Bug Fixes

- Conversion from Resources to ResourceMessages is wrong
  ([`ed26bee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/ed26bee24a22f8f531879cd2e681e1061c7bd2cd))

### Features

- Add resource field to GetTaskResponse
  ([`d750178`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/d7501781c9829b2b645651e41e92eae5660f44d8))

### Refactoring

- Logging changes
  ([`808a8c7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/808a8c7fb402b4eceb434c3007361d76f1125078))

* no uppercase initial characters


## v2.3.0 (2019-09-09)

### Features

- Add methods to convert resources field in rpc messages to and from Resources
  ([`8481420`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/84814200c3d9c5656f2e57d83d94e2228b3649bc))


## v2.2.2 (2019-09-05)

### Bug Fixes

- Move before_script to test base
  ([`a479e48`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a479e483b5e2b6b46fc36568b606199f7536418c))


## v2.2.1 (2019-09-05)

### Bug Fixes

- Move StateABC and LockFailed classes to shared package
  ([`b7af7e4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/b7af7e4164d05f90b1b468e2516c019506f272ea))


## v2.2.0 (2019-08-22)

### Features

- Add resource fields to jobs and tasks
  ([`a304999`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/a30499946790e26cb9c0603ae969752e409d16b1))

### Refactoring

- Updated generated pb2 files for latest version of protobuf compiler
  ([`17edd4a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/17edd4afefd43bd46dfc190beeecef1ed2170a8d))


## v2.1.2 (2019-06-25)


## v2.1.1 (2019-06-25)

### Bug Fixes

- **lock**: End stream when releasing shared lock
  ([`2da3424`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/2da34244ddab84370302b714cd594f2c1009929f))

- **lock**: Sharedlock is a streamStreamMethod, so it expects and returns sequences
  ([`e5e0060`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/e5e006083450d22c5d67387e63bc5437670adf85))


## v2.1.0 (2019-06-25)

### Features

- **auth**: Add `momotor.rpc.auth.client.get_authenticated_channel`
  ([`e35df74`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/e35df7401288dd5eb36d9cd6a8175a4d9f52781b))

This provides all the plumbing needed to connect and authenticate a client using grpclib.

Also re-exports grpclib's exceptions for use in dependencies


## v2.0.0 (2019-06-21)

### Bug Fixes

- Get_file_multihash content encoding maximum size is one-off
  ([`66f6c77`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/66f6c77d579c2bd91c27cb80469bbcd6040a2135))

### Code Style

- Add missing newline at end of file
  ([`c7fc40b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/c7fc40b09868fea08c0ceb0765d2f6cb7f5a3f1a))

### Features

- **hash**: Simplify hashing API
  ([`5985e3e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/5985e3edb2372e4fd7175bb06009584f19484ade))

BREAKING CHANGE: hashing API changes

- **hash**: Switch to better supported py-multihash library for asset hashes
  ([`afa14ec`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/afa14ec23464a0fec414b8ba9c1650ba84177f36))

BREAKING CHANGE: hashing API changes

`momotor.rpc.asset_hash` was changed to `momotor.rpc.hash` and most methods have changed
  `momotor.rpc.identity_hash` has been merged with `momotor.rpc.hash`
  `momotor.rpc.const.SUPPORTED_HASH_FUNCS` is now a list of integers
  `momotor.rpc.const.HASH_ENCODING` has been removed. `base58` encoding is required
  `momotor.rpc.const.MAX_HASH_LEN` has been changed to 1024 `momotor.rpc.const.MAX_IDENTITY_LENGTH`
  has been changed to 747

### Refactoring

- Import hash decode and encode functions as decode_hash and encode_hash
  ([`9a403f7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-proto/-/commit/9a403f7fd2bb57789da9d775c24a7664188ef2e7))

### Breaking Changes

- **hash**: Hashing API changes


## v1.1.0 (2019-03-05)
