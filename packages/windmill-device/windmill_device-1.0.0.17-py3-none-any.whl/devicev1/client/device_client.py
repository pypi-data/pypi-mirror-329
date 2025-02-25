# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import json
from typing import Optional

from baidubce.http import http_content_types
from baidubce.http import http_methods
from bceinternalsdk.client.bce_internal_client import BceInternalClient

from .device_api import (
    UpdateDeviceRequest,
    InvokeMethodHTTPRequest,
    ListDeviceRequest,
    GetConfigurationRequest,
    GetConfigurationResponse,
    InvokeMethodRequest,
)


class DeviceClient(BceInternalClient):
    """
    A client class for interacting with the windmill device service.
    """

    def get_configuration(
        self, req: GetConfigurationRequest
    ) -> GetConfigurationResponse:
        """
        Get configuration of a device.

        Args:
            req (GetConfigurationRequest): 获取设备配置请求
        Returns:
            HTTP request response
        """

        response = self._send_request(
            http_method=http_methods.GET,
            path=bytes(
                self._build_base_configuration_uri(
                    req.workspace_id,
                    req.device_hub_name,
                    req.local_name,
                ),
                encoding="utf-8",
            ),
            headers={b"Content-Type": http_content_types.JSON},
        )

        return GetConfigurationResponse.from_response(response)

    @staticmethod
    def _build_base_configuration_uri(
        workspace_id: str,
        device_hub_name: str,
        local_name: Optional[str] = None,
    ) -> str:
        """build the base uri for configurations.
        /v1/workspaces/:workspaceID/devicehubs/:deviceHubName/configurations/:localName
        /v1/workspaces/:workspaceID/devicehubs/:deviceHubName/configurations

        Args:
            workspace_id (str): _description_
            device_hub_name (str): _description_
            local_name (Optional[str], optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        base_uri = (
            f"/v1/workspaces/{workspace_id}/devicehubs/{device_hub_name}/configurations"
        )

        if local_name is not None and len(local_name) > 0:
            return base_uri + f"/{local_name}"

        return base_uri

    def list_device(self, req: ListDeviceRequest):
        """
        List devices in a device hub.

        Args:
            req (ListDeviceRequest): 列出设备请求
        Returns:
            HTTP request response
        """

        return self._send_request(
            http_method=http_methods.GET,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + req.workspace_id
                + "/devicehubs/"
                + req.device_hub_name
                + "/devices",
                encoding="utf-8",
            ),
            body=req.model_dump_json(exclude_defaults=True),
        )

    def update_device(self, request: UpdateDeviceRequest):
        """
        Update a device.

        Args:
            request (UpdateDeviceRequest): 更新设备请求
        Returns:
             HTTP request response
        """

        return self._send_request(
            http_method=http_methods.PUT,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + request.workspace_id
                + "/devicehubs/"
                + request.device_hub_name
                + "/devices/"
                + request.device_name,
                encoding="utf-8",
            ),
            body=request.model_dump_json(exclude_defaults=True),
        )

    def invoke_method(self, request: InvokeMethodRequest):
        """
        Invoke a method.
        """
        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + request.workspace_id
                + "/devicehubs/"
                + request.device_hub_name
                + "/devices/"
                + request.device_name
                + "/invokemethods",
                encoding="utf-8",
            ),
            body=request.model_dump_json(exclude_defaults=True),
        )

    def invoke_method_http(self, request: InvokeMethodHTTPRequest):
        """
        Invoke a method via HTTP.
        Args:
            request (InvokeMethodHTTPRequest): 调用方法HTTP请求
        Returns:
            HTTP request response
        """

        return self._send_request(
            http_method=http_methods.POST,
            headers={b"Content-Type": http_content_types.JSON},
            path=bytes(
                "/v1/workspaces/"
                + request.workspace_id
                + "/devicehubs/"
                + request.device_hub_name
                + "/devices/"
                + request.device_name
                + "/invokemethods/http/"
                + request.uri,
                encoding="utf-8",
            ),
            body=json.dumps(request.body).encode("utf-8"),
        )
