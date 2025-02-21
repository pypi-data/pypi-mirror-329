# coding: utf-8

"""
    FastAPI

    An API for our smart search engine that provides the agent that best fits your needs.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from agentverse_client.search.models.function import Function

class TestFunction(unittest.TestCase):
    """Function unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Function:
        """Test Function
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Function`
        """
        model = Function()
        if include_optional:
            return Function(
                id = '',
                type = 'function',
                name = '',
                agent = '',
                description = '',
                is_primary = True,
                groups = [
                    ''
                    ],
                total_interactions = 56,
                recent_interactions = 56,
                rating = 1.337,
                featured = True,
                last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return Function(
                id = '',
                type = 'function',
                name = '',
                agent = '',
                description = '',
                is_primary = True,
                total_interactions = 56,
                recent_interactions = 56,
                last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testFunction(self):
        """Test Function"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
