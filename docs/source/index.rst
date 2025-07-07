.. autumn.py documentation master file, created by
   sphinx-quickstart on Fri Jun  6 16:23:39 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Autumn-py!
=======================

Autumn-py is the Python SDK for interacting with the `Autumn API <https://useautumn.com/>`_, supporting both synchronous and asynchronous usage.

Features
--------

- Easily mount Autumn's routes onto your Python backend.
- Support for synchronous and asynchronous contexts.
- Fully typed.

Installation
------------

Currently, the latest Python SDK is not available on PyPi. It must be installed from our GitHub repository:

.. code-block:: shell

   python3 -m pip install -U autumn-py


If you would like support for our ``AsyncClient``, install ``aiohttp``:

.. code-block:: shell

   python3 -m pip install -U aiohttp

If you would like to mount our ASGI handler, install both ``aiohttp`` and ``starlette``.

.. code-block:: shell

   python3 -m pip install -U aiohttp starlette

.. note::

   The Python SDK officially supports Python 3.9 and above.

Quickstart
----------

To start using the SDK, you'll need your API key. You can find it in the `Autumn Dashboard <https://app.useautumn.com/sandbox/dev>`_.
The order of steps is the same as listed on the `Autumn docs <https://docs.useautumn.com/understanding>`_.

.. note::
   It is recommended to use a sandbox environment for testing. This can be controlled via the token you choose to give to the client.
   To securely store your API key, you can use environment variables.

This example shows an example flow using the Python SDK.
Of course, a real application would likely look vastly different.

.. code-block:: python

   import asyncio
   from autumn import Autumn

   # First, initialize a client.
   autumn = Autumn(token="am_sk_test_XESp2wyPE...")

   async def main():
      # Attach a customer to a product
      await autumn.attach(
         customer_id="john_doe",
         product_id="chat_messages",
      )

      # Check if the customer has access to the product
      check = await autumn.check(
         customer_id="john_doe",
         product_id="chat_messages",
      )
      if check.allowed is True:
         print("Sending chat message...")

      # Once the customer uses a chat message:
      await autumn.track(
         customer_id="john_doe",
         feature_id="chat_messages",
         value=1,
      )

      # Let's say the customer has run out of chat messages.
      check = await autumn.check(
         customer_id="john_doe",
         product_id="chat_messages",
      )
      if check.allowed is False:
         print("Customer has run out of chat messages.")

   asyncio.run(main())

Templates
---------

We've written 2 templates to aid usage with the Python SDK.

- `React + Python <https://github.com/justanotherbyte/react-python-autumn-template>`_ - A React frontend with a Python backend.
- `Python SSR <https://github.com/justanotherbyte/python-ssr-autumn-template>`_ - Python backend with a server-side rendered frontend.

Both of these templates employ ``FastAPI``, but the SDK supports any ``ASGI`` framework that supports mounting ``ASGI`` apps.


Getting Help
------------

- Report bugs and request features on the `GitHub repository <https://github.com/justanotherbyte/autumn/issues>`_.
- Join the `Autumn Discord <https://discord.gg/QDjfwGGWKT>`_ for help or open an issue on GitHub.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   asyncio
   api
