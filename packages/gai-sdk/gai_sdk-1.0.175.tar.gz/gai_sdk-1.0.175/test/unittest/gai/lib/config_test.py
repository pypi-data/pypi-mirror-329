import pytest
from unittest.mock import patch, mock_open, MagicMock,call
from gai.lib.config import GaiConfig

mock_yaml_data= {
    "version": "1.0",
    "gai_url": "http://localhost:8080",
    "logging": {
        "level": "DEBUG",
        "format": "%(levelname)s - %(message)s"
    },
    "clients": {
        "ttt": {
            "type": "ttt",
            "engine": "ollama",
            "model": "llama3.1",
            "name": "llama3.1",
            "client_type": "ollama"
        }
    }
}

### GaiConfig should load from "~/.gai/gai.yml" by default

@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_from_path_default(mock_app_path, mock_file, mock_yaml_load):
    
    # Load GaiConfig from default path
    config = GaiConfig.from_path()
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

### GaiConfig should load from custom path

@patch("yaml.load", return_value=mock_yaml_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_from_path_custom(mock_app_path, mock_file, mock_yaml_load):

    # Load Gaiconfig from a custom file path
    config = GaiConfig.from_path(file_path="/tmp/gai.yml")

    # Ensure only /tmp/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1
    
    
