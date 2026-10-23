
import paramiko

class RemoteTarget:
    def __init__(self, host, port=22, username="root", key_path=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path
        self.password = password
        self.ssh_client = None

    def connect(self):
        """Estabelece a conexão SSH com o servidor remoto."""
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connect_kwargs = {
            "hostname": self.host,
            "port": self.port,
            "username": self.username,
            "timeout": 10
        }
        
        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path
        elif self.password:
            connect_kwargs["password"] = self.password

        self.ssh_client.connect(**connect_kwargs)

    def read_file(self, file_path: str) -> str:
        """Lê um arquivo remoto via SFTP de forma segura."""
        try:
            sftp = self.ssh_client.open_sftp()
            with sftp.open(file_path, "r") as f:
                content = f.read().decode("utf-8", errors="ignore")
            sftp.close()
            return content
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo remoto {file_path}: {str(e)}")

    def run_command(self, command: str) -> str:
        """Executa um comando via SSH no servidor remoto."""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status() # Aguarda o término do comando
        
        if exit_status != 0:
            error_msg = stderr.read().decode("utf-8", errors="ignore")
            raise Exception(f"Comando remoto falhou ({command}): {error_msg}")
            
        return stdout.read().decode("utf-8", errors="ignore")

    def close(self):
        if self.ssh_client:
            self.ssh_client.close()
