from enum import Enum


# This exists here purely to avoid circular imports
class AppEnv(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"
    LIVE = "live"
