# autumn-py

The Python SDK for [Autumn](https://github.com/useautumn/autumn)'s REST API.

[![PyPI - Version](https://img.shields.io/pypi/v/autumn-py.svg)](https://pypi.org/project/autumn-py)
[![pypi](https://img.shields.io/pypi/pyversions/autumn-py.svg)](https://pypi.org/pypi/autumn-py)
[![Discord](https://img.shields.io/badge/Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/53emPtY9tA)

## Documentation

The Python SDK's documentation can be found on [ReadTheDocs](https://autumn-py.readthedocs.io).

## Features

- Easily mount Autumn's routes onto your Python backend.
- Support for synchronous and asynchronous contexts.
- Fully typed.

## Installation

> [!NOTE]
> Python 3.9+ is required.

```bash
pip install autumn-py
```

If you want `async` support, you need to install `aiohttp`.

```bash
pip install aiohttp

# Optionally
pip install aiohttp[speedups]

# You can also install it via the "aio" optional dependency.
pip install autumn-py[aio]
```

## Quickstart

```python
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
        feature_id="chat_messages",
    )
    if check.allowed is False:
        print("Customer has run out of chat messages.")

asyncio.run(main())
```

# ASGI framework usage

*Usage with a FastAPI/Starlette application*

```python
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
```

## Synchronous Usage

```python
import autumn

# First, initialize a client.
client = autumn.Client(token="am_sk_test_XESp2wyPE...")

# Attach a customer to a product
client.attach(
    customer_id="john_doe",
    product_id="chat_messages",
)

# Check if the customer has access to the product
check = client.check(
    customer_id="john_doe",
    product_id="chat_messages",
)
if check.allowed is True:
    print("Sending chat message...")

# Once the customer uses a chat message:
client.track(
    customer_id="john_doe",
    feature_id="chat_messages",
    value=1,
)

# Let's say the customer has run out of chat messages.
check = client.check(
    customer_id="john_doe",
    feature_id="chat_messages",
)
if check.allowed is False:
    print("Customer has run out of chat messages.")
```

## License

`autumn-py` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Authors

Originally written by [@justanotherbyte](https://github.com/justanotherbyte).

Maintained by [@johnyeocx](https://github.com/johnyeocx) and [@justanotherbyte](https://github.com/justanotherbyte).
