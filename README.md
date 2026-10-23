# Armadillo

> Ferramenta automatizada de auditoria de *hardening* e conformidade de servidores Linux (Local e Remoto).

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/status-active-success.svg)]()
[![Armadillo CI](https://github.com/blitk/armadillo/actions/workflows/ci.yml/badge.svg)](https://github.com/blitk/armadillo/actions/workflows/ci.yml)


O **Armadillo** é uma ferramenta leve desenvolvida em Python voltada para equipes de **Blue Team, SOC e Engenharia de Segurança**. O seu objetivo é automatizar a verificação de linhas de base de segurança (*Security Baselines*) em servidores Linux, identificando configurações vulneráveis, permissões incorretas e falhas de conformidade de forma rápida.

---

## Funcionalidades

- **Arquitetura Agnóstica de Alvo:** Suporte tanto para auditorias locais quanto remotas de forma transparente via **SSH (Paramiko)**.
- **Módulos de Checagem Abrangentes:**
  -  **SSH Security:** Validação de diretivas críticas (como `PermitRootLogin`).
  -  **File Permissions:** Verificação de permissões sensíveis em arquivos vitais (ex: `/etc/shadow`).
  -  **User Management:** Detecção de contas secundárias com privilégios totais (`UID 0`).
  -  **Network Security:** Monitoramento do estado do firewall (`UFW`).
- **Resumo Gerencial e Compliance Score:** Cálculo automático de pontuação de conformidade com base nos resultados das checagens.
- **Interface Visual Rica:** Relatórios coloridos no terminal baseados na biblioteca `Rich`.
- **Exportação de Relatórios:** Capacidade de gerar relatórios executivos em formatos estruturados (`JSON` e `Markdown`).

---

## Estrutura do Projeto

```text
server-hardening-auditor/
│
├── checks/                  # Regras e módulos de auditoria de segurança
│   ├── __init__.py
│   ├── firewall_audit.py
│   ├── permissions_audit.py
│   ├── ssh_audit.py
│   ├── sysctl_audit.py
│   └── users_audit.py
│
├── reports/                 # Pasta de saída dos relatórios exportados (JSON / MD)
├── target/                 # Camada de abstração de alvos
│   ├── __init__.py
│   ├── local_target.py
│   └── remote_target.py
│
├── tests/
├── utils/                   # Utilitários de formatação e relatórios
│   ├── plugin_loader.py
│   └── reporter.py
│
├── main.py                  # Ponto de entrada da aplicação (CLI)
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação da ferramenta
```

---

## Instalação

Clone o repositório em sua máquina local e instale as dependências necessárias:

```bash
# Clone o repositório
git clone https://github.com/blitk/armadillo.git
cd armadillo

# Instale as dependências
pip install -r requirements.txt
```

---

## Como Utilizar

A ferramenta opera através de uma interface de linha de comando (CLI) intuitiva.

### 1. Auditoria Local
Para auditar a própria máquina onde o script está sendo executado:

```bash
python main.py --target local
```
 **Nota:** Algumas checagens de arquivos críticos exigem privilégios elevados. Utilize `sudo python main.py --target local` se necessário.

### 2. Auditoria Remota (via SSH)
Para conectar e auditar um servidor remoto utilizando uma chave SSH privada:

```bash
python main.py --target remote --host 192.168.1.50 --user ubuntu --key ~/.ssh/id_rsa

```

### 3. Exportando Relatórios
Você pode exportar os resultados da auditoria diretamente para arquivos adicionando a flag `--export`:

* **Exportar para JSON:**
  ```bash
  python main.py --target local --export json
  ```
* **Exportar para Markdown:**
  ```bash
  python main.py --target local --export markdown
  ```

*(Os relatórios serão salvos automaticamente na pasta `reports/`)*.

---

## Exemplo de Saída no Terminal

```text
     _    ____  __  __    _    ____  ___ _      _     _____
    / \  |  _ \|  \/  |  / \  |  _ \|_ _| |    | |   |  _  |
   / _ \ | |_) | |\/| | / _ \ | | | || || |    | |   | | | |
  / ___ \|  _ <| |  | |/ ___ \| |_| || || |___ | |___| |_| |
 /_/   \_\_| \_\_|  |_/_/   \_\____/|___|_____||_____|_____|
    [ Armadillo - Server Hardening Auditor v1.0 ]
    
[*] Iniciando auditoria no ambiente LOCAL...
[+] Conexão estabelecida com sucesso!

[*] Carregando plugins de auditoria...
[+] 5 módulos de checagem carregados com sucesso.

[*] Executando módulos de auditoria...

[+] Auditoria concluída com sucesso! Gerando relatório...

┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Categoria         ┃ Item Auditado                            ┃ Status   ┃ Detalhes / Recomendações                       ┃
┡━━━━━━━━━━━━━━━━━━━╂━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╂━━━━━━━━━━╂━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ SSH Security      │ Desativar Login Direto de Root           │ ✅ PASS  │ Configuração segura: permitrootlogin no        │
├───────────────────┼──────────────────────────────────────────┼──────────┼────────────────────────────────────────────────┤
│ File Permissions  │ Permissões restritas no /etc/shadow      │ ✅ PASS  │ Permissões seguras encontradas: 000            │
├───────────────────┼──────────────────────────────────────────┼──────────┼────────────────────────────────────────────────┤
│ User Management   │ Verificar contas com UID 0 (Root)        │ ✅ PASS  │ Apenas o usuário 'root' possui privilégios     │
├───────────────────┼──────────────────────────────────────────┼──────────┼────────────────────────────────────────────────┤
│ Network Security  │ Status do Firewall UFW                   │ ❌ FAIL  │ O firewall UFW está inativo. Recomenda-se...   │
└───────────────────┴──────────────────────────────────────────┴──────────┴────────────────────────────────────────────────┘

┌───────────────────────────────────────┐
│           Resumo Executivo            │
├───────────────────────────────────────┤
│ Total de Checagens: 5                 │
│ Aprovadas: 4                          │
│ Score de Conformidade: 80.0%          │
└───────────────────────────────────────┘

```

---

## ⚠️ Aviso Legal (Disclaimer)

> O uso do Armadillo para testar sistemas sem autorização prévia é estritamente proibido. Esta ferramenta foi desenvolvida exclusivamente para fins educacionais, de pesquisa em segurança da informação e para auditorias defensivas em ambientes controlados.

---

## Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
