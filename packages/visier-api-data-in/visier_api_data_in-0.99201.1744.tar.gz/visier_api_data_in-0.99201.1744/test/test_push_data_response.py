# coding: utf-8

"""
    Visier Data In APIs

    Visier APIs for sending data to Visier and running data load jobs.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501


import unittest

import visier_api_data_in.models
from visier_api_data_in.models.push_data_response import PushDataResponse

class TestPushDataResponse(unittest.TestCase):
    """PushDataResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PushDataResponse:
        """Test PushDataResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """

        if include_optional:
            return PushDataResponse(
                message = '',
                sequence = 56,
                status = '',
                tenants = [
                    visier_api_data_in.models.tenant.Tenant(
                        sources = [
                            visier_api_data_in.models.source.Source(
                                data_size = '', 
                                message = '', 
                                rows = '', 
                                source_id = '', 
                                source_name = '', 
                                status = '', )
                            ], 
                        status = '', 
                        tenant_code = '', )
                    ],
                transfer_session_id = ''
            )
        else:
            return PushDataResponse(
        )

    def testPushDataResponse(self):
        """Test PushDataResponse"""
        def validate_instance(instance):
            PushDataResponse.model_validate(inst_req_only)
            instance_deserialized = PushDataResponse.from_dict(instance.to_dict())
            assert instance == instance_deserialized

        inst_req_only = self.make_instance(include_optional=False)
        validate_instance(inst_req_only)

        inst_req_and_optional = self.make_instance(include_optional=True)
        validate_instance(inst_req_and_optional)

if __name__ == '__main__':
    unittest.main()
