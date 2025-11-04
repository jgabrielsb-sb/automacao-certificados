import pytest
from unittest.mock import Mock

import requests

from automacao_certificados.selenium_automations.adapters.http.requests_client import RequestsClient


class TestRequestsClient:
    """
    Test class for the RequestsClient class.
    """
    def test_if_initializes_with_default_timeout(self):
        """
        Test if the RequestsClient initializes with default timeout.
        """
        client = RequestsClient()
        assert client._client.timeout == 10.0

    def test_if_initializes_with_custom_timeout(self):
        """
        Test if the RequestsClient initializes with custom timeout.
        """
        client = RequestsClient(base_timeout=30.0)
        assert client._client.timeout == 30.0

    def test_if_get_returns_response_with_correct_status_code(self, monkeypatch):
        """
        Test if the get method returns a response with correct status code.
        """
        url = "https://api.example.com/test"
        mock_response_data = {"message": "success"}
        
        def mock_get(*args, **kwargs):
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url)
        
        assert response.status_code == 200
        assert response.json() == mock_response_data

    def test_if_get_passes_params_correctly(self, monkeypatch):
        """
        Test if the get method passes query parameters correctly.
        """
        url = "https://api.example.com/test"
        params = {"key": "value", "page": 1}
        mock_response_data = {"results": []}
        
        def mock_get(url, **kwargs):
            assert kwargs.get("params") == params
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url, params=params)
        
        assert response.status_code == 200
        assert response.json() == mock_response_data

    def test_if_get_passes_headers_correctly(self, monkeypatch):
        """
        Test if the get method passes headers correctly.
        """
        url = "https://api.example.com/test"
        headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
        mock_response_data = {"data": "test"}
        
        def mock_get(url, **kwargs):
            assert kwargs.get("headers") == headers
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url, headers=headers)
        
        assert response.status_code == 200
        assert response.json() == mock_response_data

    def test_if_get_passes_timeout_correctly(self, monkeypatch):
        """
        Test if the get method passes timeout correctly.
        """
        url = "https://api.example.com/test"
        timeout = 5.0
        mock_response_data = {"data": "test"}
        
        def mock_get(url, **kwargs):
            assert kwargs.get("timeout") == timeout
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url, timeout=timeout)
        
        assert response.status_code == 200
        assert response.json() == mock_response_data

    def test_if_get_handles_error_status_codes(self, monkeypatch):
        """
        Test if the get method handles error status codes correctly.
        """
        url = "https://api.example.com/test"
        mock_response_data = {"error": "Not found"}
        
        def mock_get(*args, **kwargs):
            response = Mock(spec=requests.Response)
            response.status_code = 404
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url)
        
        assert response.status_code == 404
        assert response.json() == mock_response_data

    def test_if_post_returns_response_with_correct_status_code(self, monkeypatch):
        """
        Test if the post method returns a response with correct status code.
        """
        url = "https://api.example.com/test"
        json_data = {"name": "test", "value": 123}
        mock_response_data = {"id": 1, "name": "test", "value": 123}
        
        def mock_post(*args, **kwargs):
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

    def test_if_post_passes_json_body_correctly(self, monkeypatch):
        """
        Test if the post method passes JSON body correctly.
        """
        url = "https://api.example.com/test"
        json_data = {"name": "test", "value": 123}
        mock_response_data = {"id": 1, "name": "test", "value": 123}
        
        def mock_post(url, **kwargs):
            assert kwargs.get("json") == json_data
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

    def test_if_post_passes_params_correctly(self, monkeypatch):
        """
        Test if the post method passes query parameters correctly.
        """
        url = "https://api.example.com/test"
        params = {"key": "value"}
        json_data = {"name": "test"}
        mock_response_data = {"id": 1}
        
        def mock_post(url, **kwargs):
            assert kwargs.get("params") == params
            assert kwargs.get("json") == json_data
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, params=params, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

    def test_if_post_passes_headers_correctly(self, monkeypatch):
        """
        Test if the post method passes headers correctly.
        """
        url = "https://api.example.com/test"
        headers = {"Authorization": "Bearer token123"}
        json_data = {"name": "test"}
        mock_response_data = {"id": 1}
        
        def mock_post(url, **kwargs):
            assert kwargs.get("headers") == headers
            assert kwargs.get("json") == json_data
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, headers=headers, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

    def test_if_post_passes_timeout_correctly(self, monkeypatch):
        """
        Test if the post method passes timeout correctly.
        """
        url = "https://api.example.com/test"
        timeout = 5.0
        json_data = {"name": "test"}
        mock_response_data = {"id": 1}
        
        def mock_post(url, **kwargs):
            assert kwargs.get("timeout") == timeout
            assert kwargs.get("json") == json_data
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, timeout=timeout, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

    def test_if_post_handles_error_status_codes(self, monkeypatch):
        """
        Test if the post method handles error status codes correctly.
        """
        url = "https://api.example.com/test"
        json_data = {"name": "test"}
        mock_response_data = {"error": "Bad request"}
        
        def mock_post(*args, **kwargs):
            response = Mock(spec=requests.Response)
            response.status_code = 400
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, json=json_data)
        
        assert response.status_code == 400
        assert response.json() == mock_response_data

    def test_if_post_handles_empty_json_response(self, monkeypatch):
        """
        Test if the post method handles empty JSON response correctly.
        """
        url = "https://api.example.com/test"
        json_data = {"name": "test"}
        
        def mock_post(*args, **kwargs):
            response = Mock(spec=requests.Response)
            response.status_code = 204
            response.json.return_value = {}
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, json=json_data)
        
        assert response.status_code == 204
        assert response.json() == {}

    def test_if_get_passes_all_parameters_together(self, monkeypatch):
        """
        Test if the get method passes all parameters (params, headers, timeout) together correctly.
        """
        url = "https://api.example.com/test"
        params = {"key": "value"}
        headers = {"Authorization": "Bearer token"}
        timeout = 5.0
        mock_response_data = {"data": "test"}
        
        def mock_get(url, **kwargs):
            assert kwargs.get("params") == params
            assert kwargs.get("headers") == headers
            assert kwargs.get("timeout") == timeout
            response = Mock(spec=requests.Response)
            response.status_code = 200
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "get", mock_get)
        
        response = client.get(url=url, params=params, headers=headers, timeout=timeout)
        
        assert response.status_code == 200
        assert response.json() == mock_response_data

    def test_if_post_passes_all_parameters_together(self, monkeypatch):
        """
        Test if the post method passes all parameters (params, headers, timeout, json) together correctly.
        """
        url = "https://api.example.com/test"
        params = {"key": "value"}
        headers = {"Authorization": "Bearer token"}
        timeout = 5.0
        json_data = {"name": "test"}
        mock_response_data = {"id": 1}
        
        def mock_post(url, **kwargs):
            assert kwargs.get("params") == params
            assert kwargs.get("headers") == headers
            assert kwargs.get("timeout") == timeout
            assert kwargs.get("json") == json_data
            response = Mock(spec=requests.Response)
            response.status_code = 201
            response.json.return_value = mock_response_data
            return response
        
        client = RequestsClient()
        monkeypatch.setattr(client._client, "post", mock_post)
        
        response = client.post(url=url, params=params, headers=headers, timeout=timeout, json=json_data)
        
        assert response.status_code == 201
        assert response.json() == mock_response_data

