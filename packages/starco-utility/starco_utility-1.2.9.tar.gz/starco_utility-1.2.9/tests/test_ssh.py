import pytest
from unittest.mock import Mock, patch
from utility.ssh import SSHManager

@pytest.fixture
def ssh_config():
    return {
        'hostname': 'test.server.com',
        'username': 'testuser',
        'password': 'testpass',
        'port': 22
    }

@pytest.fixture
def mock_ssh_client():
    with patch('paramiko.SSHClient') as mock_client:
        yield mock_client

def test_ssh_manager_init(ssh_config):
    manager = SSHManager(**ssh_config)
    assert manager.hostname == ssh_config['hostname']
    assert manager.username == ssh_config['username']
    assert manager.password == ssh_config['password']
    assert manager.port == ssh_config['port']
    assert manager.client is None

def test_connect(mock_ssh_client, ssh_config):
    manager = SSHManager(**ssh_config)
    manager.connect()
    mock_ssh_client.return_value.connect.assert_called_once_with(
        hostname=ssh_config['hostname'],
        username=ssh_config['username'],
        password=ssh_config['password'],
        key_filename=None,
        port=ssh_config['port']
    )

def test_execute_command(mock_ssh_client, ssh_config):
    mock_stdout = Mock()
    mock_stdout.read.return_value = b'command output'
    mock_stdout.channel.recv_exit_status.return_value = 0
    
    mock_stderr = Mock()
    mock_stderr.read.return_value = b''
    
    mock_ssh_client.return_value.exec_command.return_value = (None, mock_stdout, mock_stderr)
    
    manager = SSHManager(**ssh_config)
    result = manager.execute_command('test command')
    
    assert result['output'] == 'command output'
    assert result['error'] == ''
    assert result['status'] == 0

def test_file_operations(mock_ssh_client, ssh_config):
    mock_sftp = Mock()
    mock_ssh_client.return_value.open_sftp.return_value = mock_sftp
    
    manager = SSHManager(**ssh_config)
    
    # Test upload
    manager.upload_file('/local/path', '/remote/path')
    mock_sftp.put.assert_called_once_with('/local/path', '/remote/path')
    
    # Test download
    manager.download_file('/remote/path', '/local/path')
    mock_sftp.get.assert_called_once_with('/remote/path', '/local/path')

def test_context_manager(mock_ssh_client, ssh_config):
    with SSHManager(**ssh_config) as manager:
        assert manager.client is not None
    
    mock_ssh_client.return_value.close.assert_called_once()
