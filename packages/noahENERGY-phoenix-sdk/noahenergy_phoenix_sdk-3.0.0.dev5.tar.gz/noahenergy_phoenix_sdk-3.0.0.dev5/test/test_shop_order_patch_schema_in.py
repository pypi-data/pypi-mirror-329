# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.models.shop_order_patch_schema_in import ShopOrderPatchSchemaIN

class TestShopOrderPatchSchemaIN(unittest.TestCase):
    """ShopOrderPatchSchemaIN unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ShopOrderPatchSchemaIN:
        """Test ShopOrderPatchSchemaIN
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ShopOrderPatchSchemaIN`
        """
        model = ShopOrderPatchSchemaIN()
        if include_optional:
            return ShopOrderPatchSchemaIN(
                created_by_id = '',
                order_status = 'in_progress'
            )
        else:
            return ShopOrderPatchSchemaIN(
                created_by_id = '',
        )
        """

    def testShopOrderPatchSchemaIN(self):
        """Test ShopOrderPatchSchemaIN"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
