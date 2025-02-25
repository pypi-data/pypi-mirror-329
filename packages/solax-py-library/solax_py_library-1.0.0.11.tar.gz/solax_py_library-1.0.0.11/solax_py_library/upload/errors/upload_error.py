from .base import UploadBaseError


class ConnectError(UploadBaseError):
    code = 0x1001
    message = "connect error"


class LoginError(UploadBaseError):
    code = 0x1002
    message = "authentication error"


class SendDataError(UploadBaseError):
    code = 0x1003
    message = "send data error"


class ConfigurationError(UploadBaseError):
    code = 0x1004
    message = "server configuration error"
