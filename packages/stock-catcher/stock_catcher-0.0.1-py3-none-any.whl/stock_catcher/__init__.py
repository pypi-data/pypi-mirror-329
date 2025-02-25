# Standard library imports
from importlib import resources

print("Executing __init__.py")

try:
    import tomllib
except ModuleNotFoundError:
    # Third party imports
    import tomli as tomllib


# Version of realpython-reader package
__version__ = "0.0.1"

# Read the CAC40 stock ticker file path from the config file of package stock-catcher
_cfg = tomllib.loads(resources.read_text("stock_catcher", "config.toml"))



CAC40 = _cfg["stock"]["cac_40"]