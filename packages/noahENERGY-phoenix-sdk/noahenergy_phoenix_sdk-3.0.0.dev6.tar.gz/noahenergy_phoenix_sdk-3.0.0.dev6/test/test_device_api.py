# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.api.device_api import DeviceApi


class TestDeviceApi(unittest.TestCase):
    """DeviceApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DeviceApi()

    def tearDown(self) -> None:
        pass

    def test_configs_delete(self) -> None:
        """Test case for configs_delete

        Delete Device Config
        """
        pass

    def test_configs_get(self) -> None:
        """Test case for configs_get

        Get Device Config
        """
        pass

    def test_configs_list(self) -> None:
        """Test case for configs_list

        Get Device Configs
        """
        pass

    def test_configs_patch(self) -> None:
        """Test case for configs_patch

        Patch Device Config
        """
        pass

    def test_configs_post(self) -> None:
        """Test case for configs_post

        Create Device Config
        """
        pass

    def test_devices_delete(self) -> None:
        """Test case for devices_delete

        Delete Device
        """
        pass

    def test_devices_devicetype_post(self) -> None:
        """Test case for devices_devicetype_post

        Create Device Type
        """
        pass

    def test_devices_downlink_put(self) -> None:
        """Test case for devices_downlink_put

        Send Downlink
        """
        pass

    def test_devices_flush_queue_put(self) -> None:
        """Test case for devices_flush_queue_put

        Flush Queue
        """
        pass

    def test_devices_get(self) -> None:
        """Test case for devices_get

        Get Device
        """
        pass

    def test_devices_list(self) -> None:
        """Test case for devices_list

        Get Devices
        """
        pass

    def test_devices_patch(self) -> None:
        """Test case for devices_patch

        Patch Device
        """
        pass

    def test_devices_post(self) -> None:
        """Test case for devices_post

        Create Device
        """
        pass

    def test_devices_transfer_patch(self) -> None:
        """Test case for devices_transfer_patch

        Change Companies
        """
        pass

    def test_devices_translate_config_key_get(self) -> None:
        """Test case for devices_translate_config_key_get

        Translate Config Db Key
        """
        pass

    def test_devices_write_put(self) -> None:
        """Test case for devices_write_put

        Write Device
        """
        pass


if __name__ == '__main__':
    unittest.main()
