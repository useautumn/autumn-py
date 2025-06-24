import asyncio
from autumn import Autumn

autumn = Autumn(token="am_sk_test_cRzmvdOAIbGmS2BFdU1CsfXdkJMMHceiLaQtrttwkL")


async def main():

    customer = await autumn.customers.create(
        id="test",
        email="test@test.com",
        name="Test",
    )

    result = await autumn.attach(customer_id='test', product_id="pro")
    print(result.checkout_url)


asyncio.run(main())
