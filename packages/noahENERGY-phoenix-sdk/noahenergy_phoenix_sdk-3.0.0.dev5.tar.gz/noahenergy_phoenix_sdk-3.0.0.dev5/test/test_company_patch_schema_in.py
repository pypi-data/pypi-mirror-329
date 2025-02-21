# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.models.company_patch_schema_in import CompanyPatchSchemaIn

class TestCompanyPatchSchemaIn(unittest.TestCase):
    """CompanyPatchSchemaIn unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CompanyPatchSchemaIn:
        """Test CompanyPatchSchemaIn
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CompanyPatchSchemaIn`
        """
        model = CompanyPatchSchemaIn()
        if include_optional:
            return CompanyPatchSchemaIn(
                name = '',
                conf = phoenix_sdk.models.conf.Conf(),
                members = [
                    ''
                    ]
            )
        else:
            return CompanyPatchSchemaIn(
        )
        """

    def testCompanyPatchSchemaIn(self):
        """Test CompanyPatchSchemaIn"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
