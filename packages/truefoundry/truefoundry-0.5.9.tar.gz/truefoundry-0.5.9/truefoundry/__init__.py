from truefoundry.common.warnings import (
    suppress_truefoundry_deprecation_warnings,
    surface_truefoundry_deprecation_warnings,
)
from truefoundry.deploy.core import login, logout

surface_truefoundry_deprecation_warnings()
__all__ = [
    "login",
    "logout",
    "suppress_truefoundry_deprecation_warnings",
]
