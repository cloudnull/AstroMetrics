# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


class NoTenantIdFound(Exception):
    """Tenant not found."""

    pass


class NotAuthenticated(Exception):
    """User not Authorization for action."""

    pass


class NotAuthorized(Exception):
    """Authorization not permitted."""

    pass


class SystemError(Exception):
    """General Error While performing actions."""

    pass


class NoLogLevelSet(Exception):
    """Logger Level was Not Set."""

    pass


class RetryError(Exception):
    """Error Performing Retry."""

    pass
