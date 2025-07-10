from .client import *
from .error import *
from .types.meta import *
from .types.balance import *
from .types.customers import *
from .types.features import *
from .types.products import *
from .aio.client import AsyncClient as Autumn


__version__ = "1.3.2.post1"
__license__ = "MIT"
__author__ = "justanotherbyte"
__copyright__ = "Copyright 2025 justanotherbyte"


BASE_URL = "https://api.useautumn.com"
VERSION = "v1"
