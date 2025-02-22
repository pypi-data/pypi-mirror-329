# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.models.unit_schema_out import UnitSchemaOut

class TestUnitSchemaOut(unittest.TestCase):
    """UnitSchemaOut unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UnitSchemaOut:
        """Test UnitSchemaOut
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UnitSchemaOut`
        """
        model = UnitSchemaOut()
        if include_optional:
            return UnitSchemaOut(
                created_by_id = '',
                id = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                name = '',
                conf = phoenix_sdk.models.conf.Conf(),
                address_id = '',
                parent_id = '',
                company_id = '',
                unit_group_id = '',
                unit_platform = 'ems'
            )
        else:
            return UnitSchemaOut(
                created_by_id = '',
                id = '',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                name = '',
                company_id = '',
        )
        """

    def testUnitSchemaOut(self):
        """Test UnitSchemaOut"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
