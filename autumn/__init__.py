from .aio.client import AsyncClient as Autumn
from .client import *
from .error import *
from .models.balance import *
from .models.customers import *
from .models.entities import *
from .models.features import *
from .models.meta import *
from .models.products import *

__title__ = "autumn"
__version__ = "3.1.6"
__license__ = "MIT"
__author__ = "justanotherbyte"
__copyright__ = "Copyright 2025 justanotherbyte"

BASE_URL = "https://api.useautumn.com"
VERSION = "v1"
LATEST_API_VERSION = "1.4"
