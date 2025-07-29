from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from autumn import Autumn


@pytest.mark.asyncio
async def test_customers(autumn: Autumn):
    customer = await autumn.customers.create(
        "test_customer_id",
        name="John Yeo",
        email="johnyeo@gmail.com"
    )

    await autumn.customers.update(
        customer.id, # type: ignore
        name="ay-rod",
        email="ay-rod@gmail.com"
    )

    updated_customer = await autumn.customers.get(customer.id) # type: ignore
    assert updated_customer.name == "ay-rod"

    await autumn.customers.get_billing_portal(customer.id) # type: ignore

    await autumn.customers.delete(customer.id) # type: ignore

@pytest.mark.asyncio
async def test_products(autumn: Autumn):
    default = await autumn.products.create(
        "some_product_id",
        name="Some Epic Product",
        is_add_on=False,
        is_default=True,
    )

    add_on = await autumn.products.create(
        "some_add_on",
        name="Some addon",
        is_add_on=True,
        is_default=False,
    )

    await autumn.products.update(default.id, name="A not so epic product")
    updated_default = await autumn.products.get(default.id)

    assert updated_default.name == "A not so epic product"

    await autumn.products.delete(default.id) # type: ignore
    await autumn.products.delete(add_on.id) # type: ignore
