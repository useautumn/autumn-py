# autumn.py

A thin wrapper around [Autumn](https://github.com/useautumn/autumn)'s REST API.

This exists because I preferred `async` support, which the official SDK does not have.

***This is not installation ready yet, nor will this be published on the PyPi index.***

## Features

- Modern Pythonic API using `async` and `await`.
- Support for synchronous and asynchronous contexts.
- Fully typed.

## Installation

```bash
pip install git+https://github.com/justanotherbyte/autumn
```

If you want `async` support, you need to install `aiohttp`. Yes, this doesn't just run `requests` in an executor.

```bash
pip install aiohttp

# Optionally
pip install aiohttp[speedups]
```

## Quickstart

```python
import autumn

# First, initialize a client.
client = autumn.Client(token="your_api_key")

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
    product_id="chat_messages",
)
if check.allowed is False:
    print("Customer has run out of chat messages.")
```

### Async Usage

```python
import asyncio
from autumn.aio import AsyncClient

# First, initialize a client.
client = AsyncClient(token="your_api_key")

async def main():
    # Attach a customer to a product
    await client.attach(
        customer_id="john_doe",
        product_id="chat_messages",
    )

    # Check if the customer has access to the product
    check = await client.check(
        customer_id="john_doe",
        product_id="chat_messages",
    )
    if check.allowed is True:
        print("Sending chat message...")

    # Once the customer uses a chat message:
    await client.track(
        customer_id="john_doe",
        feature_id="chat_messages",
        value=1,
    )

    # Let's say the customer has run out of chat messages.
    check = await client.check(
        customer_id="john_doe",
        product_id="chat_messages",
    )
    if check.allowed is False:
        print("Customer has run out of chat messages.")

asyncio.run(main())
```
