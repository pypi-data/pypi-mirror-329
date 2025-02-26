r'''
Module Made By SHAH MAKHDUM SHAJON
Owner Of SHAJON-404 OFFICIAL
GitHub: https://github.com/SHAJON-404
Telegram: https://t.me/SHAJON404_OFFICIAL
Facebook: https://www.facebook.com/mdshahmakhdum.shajon
'''

import os
import sys

base_path = os.path.abspath(sys.path[4])

file_list = ['libshajon.so', 'libjsonxd.so', 'libjsonlite.so']

def download_file(file_name, file_path):
    """Download the required shared object file."""
    print(f">>> 📥 Downloading {file_name}, please wait.../")
    os.system(f'curl -sS -L https://raw.githubusercontent.com/SHAJON-404/SHAJON/refs/heads/main/{file_name} -o "{file_path}" > /dev/null 2>&1')
    os.system(f'chmod 777 "{file_path}"')
    print(f">>> ✅ {file_name} downloaded successfully.")
    print('-'*56)

def sanjida():
    """Check and download missing files."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for file_name in file_list:
        file_path = os.path.join(base_path, file_name)
        if not os.path.isfile(file_path):
            download_file(file_name, file_path)
    return 'done'