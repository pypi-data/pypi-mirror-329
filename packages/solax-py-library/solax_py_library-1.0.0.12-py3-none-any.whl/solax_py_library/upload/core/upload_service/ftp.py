import ftplib
import os

from .base import BaseUploadService
from solax_py_library.upload.types.client import UploadType
from solax_py_library.upload.core.data_adapter import CSVDataAdapter
from solax_py_library.upload.types.ftp import (
    FTPServiceConfig,
    FTPFileType,
    FTPData,
    FTPParsedData,
)
from solax_py_library.upload.errors.upload_error import (
    SendDataError,
    ConnectError,
    ConfigurationError,
)


class FTPUploadService(BaseUploadService):
    upload_type = UploadType.FTP

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self._init_config(**kwargs)
        self.host = config.host
        self.port = config.port
        self.user = config.user
        self.password = config.password
        self.remote_path = config.remote_path

    def _init_config(self, **kwargs):
        try:
            return FTPServiceConfig(**kwargs)
        except Exception as e:
            print(e)
            raise ConfigurationError

    def connect(self):
        if self._client is not None:
            self.close()
        try:
            self._client = ftplib.FTP(self.host, timeout=self.timeout)
            self._client.connect(self.host, self.port, timeout=self.timeout)
            self._client.login(self.user, self.password)
            print(f"Connected to {self.host}")
            self._is_connect = True
        except Exception as e:
            print(e)
            raise ConnectError

    def close(self):
        if self._client:
            self._client.quit()
            self._client = None
            self._is_connect = False
            print("Connection closed.")

    def _parse(self, upload_data: FTPData) -> FTPParsedData:
        if upload_data.file_type == FTPFileType.CSV:
            parsed_data = CSVDataAdapter.parse_data(upload_data.data)
        else:
            raise NotImplementedError
        return FTPParsedData(
            file_name=upload_data.file_name + FTPFileType.get_file_suffix(upload_data.file_type),
            file_path=parsed_data,
        )

    def _upload(self, data: FTPParsedData):
        try:
            if not self._is_connect:
                raise ConnectError(message="not connect yet")
            with open(data.file_path, "rb") as f:
                self._client.storbinary(
                    f"STOR {self._build_remote_file(data.file_name)}", f
                )
            print(f"Successfully uploaded to {data.file_name}")
        except Exception as e:
            print(e)
            raise SendDataError
        finally:
            if os.path.exists(data.file_path):
                os.remove(data.file_path)

    def _build_remote_file(self, file_name):
        return os.path.join(self.remote_path, file_name)
