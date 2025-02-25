# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import unittest

from .client.device_api import (
    InvokeMethodHTTPRequest,
    UpdateDeviceRequest,
    ListDeviceRequest,
)


class TestDevice(unittest.TestCase):
    """
    Test Device
    """

    def test_list_request(self):
        """
        Test list request
        """

        req = ListDeviceRequest(
            workspaceID="wsvykgec",
            deviceHubName="default",
            # selects=["dbsh3000snc24g0022"],
            deselects=["dbsh3000snc24g0022"],
            pageNo=1,
            pageSize=3,
        )
        print("ListDeviceRequest")
        print(req.model_dump(by_alias=True, exclude_defaults=True))
        self.assertEqual(req.get_page_no(), 1)
        self.assertEqual(req.get_page_size(), 3)
        # device_endpoint = "172.25.110.51:80"
        # device_client = DeviceClient(endpoint=device_endpoint,
        #                              context={"OrgID": "org_id", "UserID": "user_id"})
        # resp = device_client.list_device(req=req)
        # print("resp")
        # print(resp)

    def test_device_invoke_request(self):
        """
        Test invoke request
        """
        req = InvokeMethodHTTPRequest(
            workspaceID="wsvykgec",
            deviceHubName="default",
            deviceName="dev01",
            uri="/test",
            body={"hello": "world"},
        )
        print(req.model_dump_json(by_alias=True))

    def test_update_device(self):
        """
        Test update request
        """
        req = UpdateDeviceRequest(
            workspaceID="wsvykgec",
            deviceHubName="default",
            deviceName="dbsh3000snc24g0022",
            status="Connected",
        )
        print("update device request")
        print(req.model_dump_json(by_alias=True))
        # device_endpoint = "172.25.110.51:80"
        # device_client = DeviceClient(endpoint=device_endpoint,
        #                              context={"OrgID": "org_id", "UserID": "user_id"})
        # resp = device_client.update_device(request=req)
        # print("update evice resp")
        # print(resp)


if __name__ == "__main__":
    unittest.main()
