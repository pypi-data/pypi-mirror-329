# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from phoenix_sdk.api.pandadoc_api import PandadocApi


class TestPandadocApi(unittest.TestCase):
    """PandadocApi unit test stubs"""

    def setUp(self) -> None:
        self.api = PandadocApi()

    def tearDown(self) -> None:
        pass

    def test_pandadoc_webhook_post(self) -> None:
        """Test case for pandadoc_webhook_post

        Pandadoc Web Hook
        """
        pass


if __name__ == '__main__':
    unittest.main()
