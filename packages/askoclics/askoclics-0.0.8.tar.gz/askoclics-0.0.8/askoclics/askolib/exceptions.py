from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


class AskoclicsApiError(Exception):
    """Raised when the API returns an error"""
    pass


class AskoclicsConnectionError(Exception):
    """Raised when the connection to the Askomics server fails"""
    pass


class AskoclicsAuthError(Exception):
    """Raised when the login with the provided api key failed"""
    pass


class AskoclicsParametersError(Exception):
    """Raised when parameters are missing"""
    pass


class AskoclicsNotImplementedError(Exception):
    """Raised when the endpoint does not exists"""
    pass
