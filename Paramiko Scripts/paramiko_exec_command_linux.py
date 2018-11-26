import paramiko
ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect('192.168.31.53', port=22, username='root', password='eve', look_for_keys=False, allow_agent=False)

# stdin, stdout, stderr = ssh_client.exec_command('sudo apt update && sudo apt install nmap', get_pty=True)
stdin, stdout, stderr = ssh_client.exec_command('ifconfig', get_pty=True)
# stdin.write('mypass123\n')

#print(stderr.read().decode())

output = stdout.read().decode()
print(output)

ssh_client.close()