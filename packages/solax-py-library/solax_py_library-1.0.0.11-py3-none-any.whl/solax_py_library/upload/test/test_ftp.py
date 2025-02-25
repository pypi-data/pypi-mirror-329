import asyncio
import unittest

from solax_py_library.upload.api.service import upload
from solax_py_library.upload.types.client import UploadType, UploadData
from solax_py_library.upload.types.ftp import FTPFileType


class FTPTest(unittest.TestCase):
    def test_ftp_upload(self):
        ftp_config = {
            "host": "10.1.31.181",  # 测试host
            "port": 21,
            "user": "solax",
            "password": "123456",
            "remote_path": "/xixi",
        }
        asyncio.run(
            upload(
                upload_type=UploadType.FTP,
                configuration=ftp_config,
                upload_data=UploadData(
                    upload_type=UploadType.FTP,
                    data=dict(
                        file_type=FTPFileType.CSV,
                        file_name="new_file",
                        data=[
                            {
                                "EMS1000序列号": "XMG11A011L",
                                "EMS1000本地时间": "2025-02-11 15:39:10",
                                "EMS1000版本号": "V007.11.1",
                                "电站所在国家和地区": None,
                                "电站所在当前时区": None,
                                "电站系统类型": None,
                            }
                        ],
                    ),
                ),
            )
        )
