import paramiko

# Configurações do servidor
hostname = '192.168.0.108'
port = 22
username = 'caique'
password = '123'  # Coloque a senha correta

# Cria um cliente SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conecta ao servidor
    client.connect(hostname, port, username, password)
    print("Conexão estabelecida com sucesso!")

    # Comando para criar um arquivo temporário com o novo ODBC
    odbc_config = """
    [zabbix-odbc2]
    Description=Zabbix ODBC MySQL Connection 2
    Driver=MariaDB
    Server=127.0.0.1
    Database=zabbix_proxy2
    User=zabbix
    Password=123
    Port=3306"""

    temp_file = '/tmp/odbc_temp.ini'

    # Cria o arquivo temporário
    command = f"echo '{odbc_config}' > {temp_file}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Comando para adicionar o conteúdo do arquivo temporário ao arquivo odbc.ini com sudo
    command = f"echo '{password}' | sudo -S bash -c 'cat {temp_file} >> /etc/odbc.ini'"
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + "\n")
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())

    print("Monitoramento ODBC cadastrado com sucesso!")

finally:
    # Fecha a conexão
    client.close()
    print("Conexão encerrada.")
import paramiko

# Configurações do servidor
hostname = '192.168.0.108'
port = 22
username = 'caique'
password = '123'  # Coloque a senha correta

# Cria um cliente SSH
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conecta ao servidor
    client.connect(hostname, port, username, password)
    print("Conexão estabelecida com sucesso!")

    # Comando para criar um arquivo temporário com o novo ODBC
    odbc_config = """
[zabbix-odbc2]
Description=Zabbix ODBC MySQL Connection 2
Driver=MariaDB
Server=127.0.0.1
Database=zabbix_proxy2
User=zabbix
Password=1234
Port=3306"""

    temp_file = '/tmp/odbc_temp.ini'

    # Cria o arquivo temporário
    command = f"echo '{odbc_config}' > {temp_file}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

    # Comando para adicionar o conteúdo do arquivo temporário ao arquivo odbc.ini com sudo
    command = f"echo '{password}' | sudo -S bash -c 'cat {temp_file} >> /etc/odbc.ini'"
    stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    stdin.write(password + "\n")
    stdin.flush()
    
    print(stdout.read().decode())
    print(stderr.read().decode())

    print("Monitoramento ODBC cadastrado com sucesso!")

finally:
    # Fecha a conexão
    client.close()
    print("Conexão encerrada.")

