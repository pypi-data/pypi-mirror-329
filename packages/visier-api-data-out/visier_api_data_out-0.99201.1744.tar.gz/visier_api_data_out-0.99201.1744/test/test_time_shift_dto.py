# coding: utf-8

"""
    Visier Data Out APIs

    Visier APIs for getting data out of Visier, such as aggregate data and data version information.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501


import unittest

import visier_api_data_out.models
from visier_api_data_out.models.time_shift_dto import TimeShiftDTO

class TestTimeShiftDTO(unittest.TestCase):
    """TimeShiftDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TimeShiftDTO:
        """Test TimeShiftDTO
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """

        if include_optional:
            return TimeShiftDTO(
                direction = 'BACKWARD',
                period_count = 56,
                period_type = 'MONTH'
            )
        else:
            return TimeShiftDTO(
        )

    def testTimeShiftDTO(self):
        """Test TimeShiftDTO"""
        def validate_instance(instance):
            TimeShiftDTO.model_validate(inst_req_only)
            instance_deserialized = TimeShiftDTO.from_dict(instance.to_dict())
            assert instance == instance_deserialized

        inst_req_only = self.make_instance(include_optional=False)
        validate_instance(inst_req_only)

        inst_req_and_optional = self.make_instance(include_optional=True)
        validate_instance(inst_req_and_optional)

if __name__ == '__main__':
    unittest.main()
