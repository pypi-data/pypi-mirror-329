import os

_loaded = False


def load(file=".env"):
    """Load env vars from given file - default is .env"""
    global _loaded
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f:
                # has equal sign and is not a comment
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    _loaded = True


def get(key, fallback=None):
    """Get an env var, or produce error if it is missing"""
    global _loaded
    if not _loaded:
        raise ValueError("Call snap_env.load() first to grab your .env vars!")

    value = os.environ.get(key)
    if value is None and fallback is None:
        raise ValueError(f'"{key}" is not defined! Define it or set a fallback')
    return value if value is not None else fallback
