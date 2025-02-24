=============================================
Momotor Engine Protocol Library documentation
=============================================

The `momotor-engine-proto` package provides the Momotor RPC protocol for communication between the Momotor
broker and clients, and also for the communication between the Momotor broker and workers.

The Momotor RPC protocol uses `gRPC <https://grpc.io/>`_. This package contains the gRPC protocol definitions,
as well as the generated Python stub files to use the protocol.

This package also contains higher level functions that communicate using the RPC channels to provide functionality
available to both Momotor server and clients.

Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   auth
   asset
   exception
   hash
   proto
   resources
   shared
   status
   task
   validate
   const


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
