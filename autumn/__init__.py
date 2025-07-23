from .client import *
from .error import *
from .models.meta import *
from .models.balance import *
from .models.customers import *
from .models.features import *
from .models.products import *
from .aio.client import AsyncClient as Autumn


__version__ = "1.5.0"
__license__ = "MIT"
__author__ = "justanotherbyte"
__copyright__ = "Copyright 2025 justanotherbyte"


BASE_URL = "https://api.useautumn.com"
VERSION = "v1"
