# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.models.device_config_schema_in import DeviceConfigSchemaIN

class TestDeviceConfigSchemaIN(unittest.TestCase):
    """DeviceConfigSchemaIN unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DeviceConfigSchemaIN:
        """Test DeviceConfigSchemaIN
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DeviceConfigSchemaIN`
        """
        model = DeviceConfigSchemaIN()
        if include_optional:
            return DeviceConfigSchemaIN(
                created_by_id = None,
                conf = phoenix_sdk.models.conf.Conf(),
                formatter = ''
            )
        else:
            return DeviceConfigSchemaIN(
        )
        """

    def testDeviceConfigSchemaIN(self):
        """Test DeviceConfigSchemaIN"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
