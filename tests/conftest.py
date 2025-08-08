import os
import asyncio

import pytest

from autumn import Autumn

@pytest.fixture
async def autumn():
    async with Autumn(token=os.environ["AUTUMN_TEST_KEY"]) as autumn:
        yield autumn
