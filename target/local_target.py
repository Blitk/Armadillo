import os
import subprocess

class LocalTarget:
    def connect(self):
        """Para o alvo local, nenhuma conexão de rede é necessária."""
        pass

    def read_file(self, file_path: str) -> str:
        """Lê um arquivo do disco local."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo local não encontrado: {file_path}")
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def run_command(self, command: str) -> str:
        """Executa um comando no shell local e retorna a saída."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erro ao executar comando local '{command}': {e.stderr}")

    def close(self):
        pass
