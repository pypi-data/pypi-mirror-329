# coding: utf-8

"""
    FastAPI

    An API for our smart search engine that provides the agent that best fits your needs.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from agentverse_client.search.aio.models.agent_tag import AgentTag

class TestAgentTag(unittest.TestCase):
    """AgentTag unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AgentTag:
        """Test AgentTag
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AgentTag`
        """
        model = AgentTag()
        if include_optional:
            return AgentTag(
                tag = ''
            )
        else:
            return AgentTag(
                tag = '',
        )
        """

    def testAgentTag(self):
        """Test AgentTag"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
