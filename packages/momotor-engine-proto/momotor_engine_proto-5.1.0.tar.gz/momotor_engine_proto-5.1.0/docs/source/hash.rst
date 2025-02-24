====
Hash
====

Assets are identified by their base58_ encoded hash. Momotor uses the multihash_ format for these hashes
to support multiple hashing algorithms.

The multihash_ format allows to easily upgrade the hashing function in the future and only uses hashing
algorithms both client and server can support.

For short content (less than :py:data:`~momotor.rpc.const.MAX_IDENTITY_LENGTH` bytes),
the content itself is encoded as an `identity hash`_.

Functions
=========

.. automodule:: momotor.rpc.hash.funcs
   :members:
   :undoc-members:

.. _identity hash:

Identity hash
=============

.. automodule:: momotor.rpc.hash.identity
   :members:
   :undoc-members:
