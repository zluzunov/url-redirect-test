import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import responses

from test_rewrite_results import check_url, process_urls, main


def test_check_url_success():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://example.com/test", 
                json={}, status=200, 
                headers={"Location": "https://example.com/redirected"})
        
        session = MagicMock()
        final_url, status = check_url(session, "https://example.com/test")
        assert status == 200


def test_check_url_connection_error():
    session = MagicMock()
    session.get.side_effect = Exception("Connection error")
    
    final_url, status = check_url(session, "https://bad.url")
    assert status == 0
    assert "bad.url" in final_url


def test_process_urls_creates_output_dir(tmp_path):
    input_file = tmp_path / "input.tab"
    output_file = tmp_path / "output.tab"
    input_file.write_text("https://example.com/test\n")
    
    with patch('test_rewrite_results.requests.Session') as mock_session:
        mock_session.return_value.get.return_value.status_code = 200
        mock_session.return_value.get.return_value.url = "https://example.com/test"
        
        process_urls(input_file, output_file)
        assert output_file.exists()