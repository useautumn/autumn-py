import asyncio
from autumn import Autumn


async def main():
    client = Autumn(token="")

    res = await client.checkout(customer_id="123", product_id="pro")
    print(res)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
