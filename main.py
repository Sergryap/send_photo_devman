import subprocess
import os
import gzip


def get_zip_archive(file_name, folder_name):
    subprocess.run(['tar', '-cvf', f'{file_name}.tar.gz', f'{folder_name}'])
    with open(f'{file_name}.tar.gz', 'rb') as file_in:
        with gzip.open(f'{file_name}.zip', 'wb') as file_out:
            file_out.writelines(file_in)
    subprocess.run(['rm', f'{file_name}.tar.gz'])


if __name__ == '__main__':
    get_zip_archive('photo', 'original_photo')
