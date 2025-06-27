Asyncio Support
===============

With the rise of :keyword:`async`/:keyword:`await` in Python and popular web frameworks like FastAPI, it's important to support asyncio.
This section will cover how to use the asyncio client, as well as recommended patterns for using it with libraries like FastAPI.

Installation
------------

Async support is not included in the default installation. You can install it via:

.. code-block:: bash

    pip install autumn-py[aio]

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

The basic usage of the asyncio client is the same as the sync client. You can use the :class:`~autumn.aio.client.AsyncClient` class to interact with the API asynchronously.

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

ASGI compatible frameworks
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Python SDK now supports automatic mounting of backend routes that the `autumn-js <https://github.com/useautumn/autumn-js>`_ JavaSript library uses.
This means you can easily use a stack where you have a React frontend and a Python backend.

.. note::
    The ``starlette`` and ``aiohttp`` libraries are required for ASGI support. You can install them via pip.

You must provide an asynchronous ``identify`` method that takes in a Starlette ``Request`` object. You are required to return your logged in user's information, specifically their ``name``,
their internal ``user_id`` (the User ID on **your** systems) and their ``email``.

Examples have been provided below.

.. warning::
    You **must** mount the ``AutumnASGI`` app at ``/api/autumn``. Any other route will cause ``autumn-js`` to break.

.. tabs::

    .. tab:: Litestar

        .. code-block:: python

            from __future__ import annotations

            import os
            from typing import TYPE_CHECKING

            from litestar import Litestar
            from litestar.handlers import asgi
            from litestar.config.cors import CORSConfig

            from autumn.asgi import AutumnASGI

            if TYPE_CHECKING:
                from starlette.requests import Request
                from autumn.asgi import AutumnIdentifyData


            async def identify(request: Request) -> AutumnIdentifyData:
                # db = request.state.postgres
                # session = request.session

                return {
                    "customer_id": "user_123",
                    "customer_data": {"name": "John Doe", "email": "djohn@gmail.com"},
                }


            autumn = AutumnASGI(token=os.environ["AUTUMN_KEY"], identify=identify)


            async def close_autumn(_):
                await autumn.close()


            autumn_asgi = asgi(path="/api/autumn", is_mount=True, copy_scope=True)(autumn)

            # CORS must be configured correctly.
            # You must allow the GET, POST and OPTIONS methods at a minimum.
            # Pass your frontend url here.
            DOMAINS = ["<Your Frontend URL>"]
            app = Litestar(
                debug=True,
                route_handlers=[autumn_asgi],
                cors_config=CORSConfig(
                    allow_origins=DOMAINS,
                    allow_credentials=True,
                    allow_headers=["*"],
                    allow_methods=["*"],
                ),
                on_shutdown=[close_autumn],
            )


    .. tab:: Starlette/FastAPI

        .. code-block:: python

            from __future__ import annotations

            import os
            import contextlib
            from typing import TYPE_CHECKING

            from starlette.applications import Starlette
            from starlette.middleware.cors import CORSMiddleware
            from starlette.middleware import Middleware
            from autumn.asgi import AutumnASGI

            if TYPE_CHECKING:
                from starlette.requests import Request
                from autumn.asgi import AutumnIdentifyData


            async def identify(request: Request) -> AutumnIdentifyData:
                # db = request.state.postgres
                # session = request.session

                # This is where you are responsible for identifying the logged-in user.
                # You must return a dictionary in the format shown below.

                return {
                    "customer_id": "user_123",
                    "customer_data": {"name": "John Doe", "email": "djohn@gmail.com"},
                }


            autumn = AutumnASGI(token=os.environ["AUTUMN_KEY"], identify=identify)

            @contextlib.asynccontextmanager
            async def lifespan(_):
                yield
                await autumn.close()

            # CORS must be configured correctly.
            # You must allow the GET, POST and OPTIONS methods at a minimum.
            # Pass your frontend url here.
            DOMAINS = ["<Your Frontend URL>"]
            middleware = [
                Middleware(
                    CORSMiddleware,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    allow_credentials=True,
                    allow_origins=DOMAINS,
                )
            ]

            app = Starlette(debug=True, middleware=middleware, lifespan=lifespan)
            app.mount("/api/autumn", autumn)

Finally, on your frontend, simply adjust the ``<AutumnHandler />`` component's ``backendUrl`` attribute to the URL of your Python API.

For a complete example, check out the `python-ssr-autumn-template <https://github.com/justanotherbyte/python-ssr-autumn-template>`_.

That's it! Enjoy using Autumn!