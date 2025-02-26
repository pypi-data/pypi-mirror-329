class HubspaceError(Exception):
    pass


class DeviceNotFound(HubspaceError):
    pass


class DeviceUpdateError(HubspaceError):
    pass


class ExceededMaximumRetries(HubspaceError):
    pass


class InvalidAuth(HubspaceError):
    pass


class InvalidResponse(HubspaceError):
    pass
