Asyncio Support
===============

With the rise of :keyword:`async`/:keyword:`await` in Python and popular web frameworks like FastAPI, it's important to support asyncio.
This section will cover how to use the asyncio client, as well as recommended patterns for using it with libraries like FastAPI.

Installation
------------

Async support is not included in the default installation. You can install it via:

.. code-block:: bash

    pip install git+https://github.com/justanotherbyte/autumn.git@main#egg=autumn[aio]

This will install the :mod:`aiohttp` library, which is required for async support. You may optionally choose to install some speedups provided by the :mod:`aiohttp` library.
Note that these speedups are not required for the library to work, but they may improve performance, but may not be available on all platforms.

.. code-block:: bash

    pip install aiohttp[speedups]

.. warning::
    View the :mod:`aiohttp` `documentation <https://docs.aiohttp.org/en/stable/speedups.html>`_ for more information on the speedups. Windows users may need to adjust their event loop.


Usage
-----

Autumn supports asyncio. You can use the :class:`~autumn.aio.client.AsyncClient` class to interact with the API asynchronously.

Basic Usage
^^^^^^^^^^^

The basic usage of the asyncio client is the same as the sync client. You can use the :class:`autumn.aio.client.AsyncClient` class to interact with the API asynchronously.

.. code-block:: python

    import asyncio

    from autumn.aio import AsyncClient

    async def main():
        client = AsyncClient(token="your_api_key")
        await client.attach(
            "customer_id",
            product_id="chat_messages"
        )

    asyncio.run(main())

FastAPI (and other frameworks)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

FastAPI is a popular web framework for Python. It's built on top of Starlette, which is a lightweight ASGI framework.

If you're looking for a similar experience to the official Next.js client-side implementation, or we recommend writing your own routes.
This will soon be natively supported by the library (hopefully) soon.

.. warning::
    Do **not** use the synchronous :class:`autumn.Client` in your ASGI application.
    You will not get the full benefits of an asynchronous application - the synchronous client will block the event loop.

.. code-block:: python

    from fastapi import FastAPI
    from pydantic import BaseModel
    from autumn.aio import AsyncClient

    app = FastAPI()
    autumn = AsyncClient(token="your_api_key")

    # Pydantic models are used to validate the request body.
    class CreateCustomerRequest(BaseModel):
        id: str
        name: str
        email: str

    @app.post("/api/autumn/customers")
    async def create_customer(request: CreateCustomerRequest):
        await autumn.customers.create(
            name=request.name,
            email=request.email
        )