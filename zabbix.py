import os
from flask import Flask, request, render_template
from zabbix_api import ZabbixAPI
import paramiko

app = Flask(__name__)

# Configuração da API Zabbix
ZABBIX_URL = "http://127.0.0.1/api_jsonrpc.php"
ZABBIX_USERNAME = os.getenv("ZABBIX_USER", "Admin")
ZABBIX_PASSWORD = os.getenv("ZABBIX_PASS", "zabbix")

# Configuração do Servidor SSH
SSH_HOST = os.getenv("SSH_HOST", "192.168.0.108")
SSH_PORT = 22
SSH_USER = os.getenv("SSH_USER", "caique")
SSH_PASSWORD = os.getenv("SSH_PASS", "123")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_host', methods=['POST'])
def add_host():
    hostname = request.form['hostname']
    ip = request.form['ip']
    template_id = request.form['template']
    macro_user = request.form.get('macro_user')
    macro_password = request.form.get('macro_password')

    try:
        zapi = ZabbixAPI(ZABBIX_URL, timeout=150)
        zapi.login(ZABBIX_USERNAME, ZABBIX_PASSWORD)
        print(f'Conectado na API do Zabbix, versão {zapi.api_version()}')

        groups = [{"groupid": groupid} for groupid in ['2', '7']]
        templates = [{"templateid": template_id}]
        macros = []

        if macro_user:
            macros.append({"macro": "{$USER_ID}", "value": macro_user})
        if macro_password:
            macros.append({"macro": "{$PASSWORD}", "value": macro_password})

        interface = {
            "type": 1,  # Agente
            "main": 1,
            "useip": 1,
            "ip": ip,
            "dns": "",
            "port": "10050"
        }

        create_host = zapi.host.create({
            "groups": groups,
            "host": hostname,
            "interfaces": [interface],
            "templates": templates,
            "macros": macros
        })
        return f'Host cadastrado com sucesso: {create_host}'

    except Exception as err:
        return f'Falha ao cadastrar o host: {err}'

@app.route('/configure_odbc', methods=['POST'])
def configure_odbc():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(SSH_HOST, SSH_PORT, SSH_USER, SSH_PASSWORD)

        odbc_config = """
[zabbix-odbc2]
Description=Zabbix ODBC MySQL Connection 2
Driver=MariaDB
Server=127.0.0.1
Database=zabbix_proxy2
User=zabbix
Password=1234
Port=3306
"""
        temp_file = '/tmp/odbc_temp.ini'
        
        # Criar o arquivo temporário
        command = f"echo '{odbc_config}' > {temp_file}"
        client.exec_command(command)
        
        # Adicionar ao odbc.ini com sudo
        command = f"echo '{SSH_PASSWORD}' | sudo -S bash -c 'cat {temp_file} >> /etc/odbc.ini'"
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        stdin.write(SSH_PASSWORD + "\n")
        stdin.flush()
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        client.close()
        return f"Monitoramento ODBC cadastrado com sucesso!\n{output}\n{error}"
    
    except Exception as err:
        return f"Erro ao configurar o ODBC: {err}"

if __name__ == '__main__':
    app.run(debug=True)
