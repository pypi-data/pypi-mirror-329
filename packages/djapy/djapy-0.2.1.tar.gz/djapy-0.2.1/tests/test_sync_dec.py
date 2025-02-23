import unittest
from unittest.mock import Mock, patch
from django.http import HttpRequest, HttpResponse
from djapy.core.dec.sync_dec import SyncDjapifyDecorator
from djapy.core.auth import BaseAuthMechanism

class MockAuth(BaseAuthMechanism):
    def __init__(self):
        self.__name__ = 'MockAuth'
    
    def check_auth(self, request):
        return True
    
MockAuth.__name__ = 'MockAuth'

class TestSyncDjapifyDecorator(unittest.TestCase):
    def setUp(self):
        # Create proper auth handler
        self.mock_auth = MockAuth()
        self.mock_auth.__name__ = 'MockAuth'
        
        self.mock_view = Mock(return_value={"key": "value"})
        self.mock_view.__annotations__ = {'return': dict}
        
        # Add response_wrapper as tuple
        self.mock_view.response_wrapper = (200, dict)
        
        # Keep schema and extra_query_dict setup
        self.mock_view.schema = {
            'response': {'200': dict},
            'query': {}
        }
        self.mock_view.extra_query_dict = {}
        
        # Add auth attribute
        self.mock_view.auth = self.mock_auth
        
        self.decorator = SyncDjapifyDecorator(self.mock_view)
        self.request = HttpRequest()
        self.request.method = 'GET'

    @patch('djapy.core.dec.sync_dec.RequestParser')
    @patch('djapy.core.dec.sync_dec.ResponseParser')
    def test_call_method(self, mock_resp_parser_cls, mock_req_parser_cls):
        mock_req_parser = mock_req_parser_cls.return_value
        mock_req_parser.parse_data.return_value = {}

        mock_resp_parser = mock_resp_parser_cls.return_value
        mock_response = {"key": "value"}
        mock_resp_parser.parse_data.return_value = mock_response

        decorated_view = self.decorator(self.mock_view)
        response = decorated_view(self.request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"key": "value"}')

    @patch('djapy.core.dec.sync_dec.RequestParser')
    @patch('djapy.core.dec.sync_dec.ResponseParser')
    def test_call_method_with_exception(self, mock_resp_parser_cls, mock_req_parser_cls):
        self.mock_view.side_effect = Exception("Test exception")
        decorated_view = self.decorator(self.mock_view)
        response = decorated_view(self.request)
        
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Test exception", response.content)

if __name__ == '__main__':
    unittest.main()