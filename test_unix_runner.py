import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

SSH_HOST = os.getenv('SSH_HOST')
SSH_USER = os.getenv('SSH_USER')
SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')
REMOTE_SCRIPT_PATH = os.getenv('REMOTE_SCRIPT_PATH')


def run_remote_script():
    try:
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=SSH_HOST, username=SSH_USER, pkey=key)
        stdin, stdout, stderr = client.exec_command(f'bash {REMOTE_SCRIPT_PATH}')
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        print('Remote script output:')
        print(output)
        if error:
            print('Errors:')
            print(error)
        # Check job statuses
        if all([line.strip().endswith('status: Pass') for line in output.splitlines() if 'status:' in line]):
            print('All jobs succeeded.')
            return True, output
        else:
            print('Some jobs failed.')
            return False, output
    except Exception as e:
        print(f'Error: {e}')
        return False, str(e)

if __name__ == '__main__':
    status, result = run_remote_script()
    print(f'Job Status: {"Success" if status else "Failed"}')
