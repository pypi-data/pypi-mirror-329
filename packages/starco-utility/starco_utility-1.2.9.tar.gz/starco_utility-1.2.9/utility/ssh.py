import paramiko
import time

class SSHManager:
    def __init__(self, hostname, username, password=None, key_filename=None, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            key_filename=self.key_filename,
            port=self.port
        )
        return self

    def execute_command(self, command, timeout=30):
        if not self.client:
            self.connect()
            
        stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        return {
            'output': stdout.read().decode('utf-8').strip(),
            'error': stderr.read().decode('utf-8').strip(),
            'status': stdout.channel.recv_exit_status()
        }

    def upload_file(self, local_path, remote_path):
        if not self.client:
            self.connect()
            
        sftp = self.client.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def download_file(self, remote_path, local_path):
        if not self.client:
            self.connect()
            
        sftp = self.client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    def close(self):
        if self.client:
            self.client.close()
